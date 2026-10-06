import csv
import math
import re
from collections import Counter
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "movies.csv"

_model_cache = {
    "mtime": None,
    "movies": None,
    "matrix": None,
    "similarity": None,
    "vectorizer": None,
}

# Small built-in English stop-word list so the project has no ML-library dependency.
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "but", "by",
    "for", "from", "had", "has", "have", "he", "her", "hers", "him", "his",
    "i", "in", "into", "is", "it", "its", "of", "on", "or", "our", "she",
    "that", "the", "their", "them", "they", "this", "to", "was", "we", "were",
    "what", "when", "where", "which", "who", "with", "you", "your"
}


def _safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def load_movies():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Movie data was not found at {DATA_PATH}. "
            "Make sure data/movies.csv is included in the repository."
        )

    movies = []
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_id = row.get("id")
            if not raw_id:
                continue

            movie = {
                "id": _safe_int(raw_id),
                "title": str(row.get("title", "")).strip(),
                "genres": [
                    item.strip()
                    for item in str(row.get("genres", "")).split("|")
                    if item.strip()
                ],
                "year": _safe_int(row.get("year")),
                "rating": _safe_float(row.get("rating")),
                "director": str(row.get("director", "")).strip(),
                "cast": [
                    item.strip()
                    for item in str(row.get("cast", "")).split("|")
                    if item.strip()
                ],
                "keywords": [
                    item.strip()
                    for item in str(row.get("keywords", "")).split("|")
                    if item.strip()
                ],
                "description": str(row.get("description", "")).strip(),
                "poster_url": str(row.get("poster_url", "")).strip(),
            }
            movies.append(movie)

    return sorted(movies, key=lambda item: item["rating"], reverse=True)


def build_feature_text(movie):
    # Repeating important metadata gives it more influence, just like the
    # previous TF-IDF implementation.
    parts = [
        (" ".join(movie.get("genres", [])) + " ") * 3,
        (" ".join(movie.get("keywords", [])) + " ") * 3,
        (movie.get("director", "") + " ") * 2,
        " ".join(movie.get("cast", [])),
        movie.get("description", ""),
    ]
    return " ".join(part for part in parts if part)


def _tokenize(text):
    return [
        token
        for token in re.findall(r"[a-z0-9]+", str(text).lower())
        if token not in STOP_WORDS and len(token) > 1
    ]


def _build_tfidf_vectors(texts):
    tokenized = [_tokenize(text) for text in texts]
    document_count = len(tokenized)

    document_frequency = Counter()
    for tokens in tokenized:
        document_frequency.update(set(tokens))

    idf = {
        term: math.log((1 + document_count) / (1 + frequency)) + 1.0
        for term, frequency in document_frequency.items()
    }

    vectors = []
    for tokens in tokenized:
        counts = Counter(tokens)
        total = sum(counts.values()) or 1
        raw = {
            term: (count / total) * idf.get(term, 1.0)
            for term, count in counts.items()
        }
        norm = math.sqrt(sum(value * value for value in raw.values())) or 1.0
        vectors.append({term: value / norm for term, value in raw.items()})

    return vectors, idf


def _vectorize_query(text, idf):
    tokens = _tokenize(text)
    counts = Counter(token for token in tokens if token in idf)
    total = sum(counts.values())
    if not total:
        return {}

    raw = {
        term: (count / total) * idf[term]
        for term, count in counts.items()
    }
    norm = math.sqrt(sum(value * value for value in raw.values())) or 1.0
    return {term: value / norm for term, value in raw.items()}


def _cosine_sparse(left, right):
    if not left or not right:
        return 0.0

    if len(left) > len(right):
        left, right = right, left

    return sum(value * right.get(term, 0.0) for term, value in left.items())


def _build_similarity_matrix(vectors):
    size = len(vectors)
    similarity = [[0.0] * size for _ in range(size)]

    for i in range(size):
        similarity[i][i] = 1.0
        for j in range(i + 1, size):
            score = _cosine_sparse(vectors[i], vectors[j])
            similarity[i][j] = score
            similarity[j][i] = score

    return similarity


def _get_model():
    """Build and cache a pure-Python TF-IDF/cosine model for movies.csv."""
    mtime = DATA_PATH.stat().st_mtime

    if _model_cache["mtime"] == mtime:
        return _model_cache

    movies = load_movies()
    feature_texts = [build_feature_text(movie) for movie in movies]
    vectors, idf = _build_tfidf_vectors(feature_texts)
    similarity = _build_similarity_matrix(vectors)

    _model_cache.update({
        "mtime": mtime,
        "movies": movies,
        "matrix": vectors,
        "similarity": similarity,
        "vectorizer": {"idf": idf},
    })
    return _model_cache


def _movie_index(movies, movie_id):
    for index, movie in enumerate(movies):
        if movie["id"] == movie_id:
            return index
    return None


def _serialize(movie, similarity=None):
    payload = {
        "id": movie["id"],
        "title": movie["title"],
        "genres": "|".join(movie["genres"]),
        "year": movie["year"],
        "rating": movie["rating"],
        "director": movie["director"],
        "cast": movie["cast"],
        "keywords": movie["keywords"],
        "description": movie["description"],
        "poster_url": movie["poster_url"],
    }
    if similarity is not None:
        payload["similarity"] = round(max(0.0, min(1.0, similarity)) * 100, 1)
    return payload


def recommend_for_movie(movie_id, top_n=4):
    model = _get_model()
    movies = model["movies"]
    similarity = model["similarity"]

    index = _movie_index(movies, movie_id)
    if index is None:
        return []

    scores = [
        (i, score)
        for i, score in enumerate(similarity[index])
        if i != index
    ]
    scores.sort(key=lambda item: item[1], reverse=True)

    return [_serialize(movies[i], score) for i, score in scores[:top_n]]


def recommend_for_query(query="", favorites=None, ratings=None, top_n=4):
    model = _get_model()
    movies = model["movies"]
    vectors = model["matrix"]
    similarity = model["similarity"]
    idf = model["vectorizer"]["idf"]

    favorites = {int(movie_id) for movie_id in (favorites or [])}
    ratings = {
        int(movie_id): int(rating)
        for movie_id, rating in (ratings or {}).items()
    }
    search = str(query or "").strip().lower()

    matched_movie = None
    matched_index = None

    if search:
        title_matches = [
            (i, movie)
            for i, movie in enumerate(movies)
            if search in movie["title"].lower()
        ]

        if title_matches:
            matched_index, matched_movie = max(
                title_matches,
                key=lambda pair: (
                    pair[1]["title"].lower() == search,
                    pair[1]["rating"],
                ),
            )
        else:
            query_vector = _vectorize_query(search, idf)
            if query_vector:
                query_scores = [
                    _cosine_sparse(query_vector, movie_vector)
                    for movie_vector in vectors
                ]
                best_index = max(
                    range(len(query_scores)),
                    key=query_scores.__getitem__,
                    default=None,
                )
                if best_index is not None and query_scores[best_index] > 0:
                    matched_index = best_index
                    matched_movie = movies[best_index]

    preference_rows = []
    preference_weights = []

    for i, movie in enumerate(movies):
        movie_id = movie["id"]
        rating = ratings.get(movie_id)

        if movie_id in favorites:
            preference_rows.append(i)
            preference_weights.append(1.5)

        if rating is not None and rating >= 3:
            preference_rows.append(i)
            preference_weights.append(rating / 3)

    scores = [0.0] * len(movies)

    if matched_index is not None:
        for i, value in enumerate(similarity[matched_index]):
            scores[i] += value * 1.8

    for i, weight in zip(preference_rows, preference_weights):
        for j, value in enumerate(similarity[i]):
            scores[j] += value * weight

    if matched_index is None and not preference_rows:
        for i, movie in enumerate(movies):
            scores[i] = movie["rating"]

    excluded = favorites | set(ratings.keys())
    if matched_movie:
        excluded.add(matched_movie["id"])

    ranked = [
        (i, score)
        for i, score in enumerate(scores)
        if movies[i]["id"] not in excluded
    ]
    ranked.sort(key=lambda item: item[1], reverse=True)

    max_score = max((score for _, score in ranked), default=1.0) or 1.0
    recommendations = []

    for i, score in ranked[:top_n]:
        movie = movies[i]
        recommendations.append({
            **_serialize(movie),
            "similarity": round(min(99.0, max(0.0, score / max_score * 100)), 1),
            "match_reason": (
                f"Similar to {matched_movie['title']}"
                if matched_movie
                else "Matches your saved preferences"
                if preference_rows
                else "Popular with MovieMate viewers"
            ),
        })

    return {
        "query": search,
        "matched_movie": matched_movie["title"] if matched_movie else None,
        "recommendations": recommendations,
    }


def get_all_movies():
    model = _get_model()
    return [_serialize(movie) for movie in model["movies"]]


def _content_scores(model, favorites, ratings):
    movies = model["movies"]
    similarity = model["similarity"]
    scores = [0.0] * len(movies)
    weight_total = 0.0
    index_by_id = {movie["id"]: i for i, movie in enumerate(movies)}

    for movie_id in favorites:
        i = index_by_id.get(movie_id)
        if i is None:
            continue

        for j, value in enumerate(similarity[i]):
            scores[j] += value * 1.5
        weight_total += 1.5

    for movie_id, rating in ratings.items():
        if rating < 3:
            continue

        i = index_by_id.get(movie_id)
        if i is None:
            continue

        weight = rating / 3
        for j, value in enumerate(similarity[i]):
            scores[j] += value * weight
        weight_total += weight

    if weight_total == 0:
        return None

    max_score = max(scores) or 1.0
    return [score / max_score for score in scores]


def _ratings_by_user(all_ratings):
    users = {}
    for row in all_ratings:
        try:
            user_id = int(row["user_id"])
            movie_id = int(row["movie_id"])
            rating = float(row["rating"])
        except (KeyError, TypeError, ValueError):
            continue
        users.setdefault(user_id, {})[movie_id] = rating
    return users


def _user_cosine(left, right):
    if not left or not right:
        return 0.0

    common = set(left) & set(right)
    if not common:
        return 0.0

    dot = sum(left[movie_id] * right[movie_id] for movie_id in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    denominator = left_norm * right_norm

    return dot / denominator if denominator else 0.0


def recommend_collaborative(target_user_id, all_ratings, top_n=4):
    model = _get_model()
    movies = model["movies"]
    movie_ids = {movie["id"] for movie in movies}
    users = _ratings_by_user(all_ratings)

    target_user_id = int(target_user_id)
    target_ratings = users.get(target_user_id)

    if not target_ratings or len(users) < 2:
        return {"recommendations": [], "reason": "not_enough_data"}

    weighted_scores = {}
    weight_totals = {}

    for other_id, other_ratings in users.items():
        if other_id == target_user_id:
            continue

        similarity = _user_cosine(target_ratings, other_ratings)
        if similarity <= 0:
            continue

        for movie_id, rating in other_ratings.items():
            if movie_id not in movie_ids or movie_id in target_ratings:
                continue

            weighted_scores[movie_id] = (
                weighted_scores.get(movie_id, 0.0) + rating * similarity
            )
            weight_totals[movie_id] = (
                weight_totals.get(movie_id, 0.0) + similarity
            )

    predicted = {
        movie_id: weighted_scores[movie_id] / weight_totals[movie_id]
        for movie_id in weighted_scores
        if weight_totals[movie_id] > 0
    }

    ranked_ids = sorted(
        predicted,
        key=lambda movie_id: predicted[movie_id],
        reverse=True,
   )[:top_n]

    movie_by_id = {movie["id"]: movie for movie in movies}
    recommendations = [
        _serialize(movie_by_movie_id[movie_id], predicted[movie_id] / 5.0)
        for movie_id in ranked_ids
        if movie_id in movie_by_id and predicted[movie_id] > 0
    ]

    return {
        "recommendations": recommendations,
        "reason": "ok" if recommendations else "no_overlap",
    }


def _collaborative_scores(target_user_id, all_ratings, model):
    movies = model["movies"]
    index_by_id = {movie["id"]: i for i, movie in enumerate(movies)}
    users = _ratings_by_user(all_ratings)

    target_user_id = int(target_user_id)
    target_ratings = users.get(target_user_id)

    if not target_ratings or len(users) < 2:
        return None

    scores = [0.0] * len(movies)

    for other_id, other_ratings in users.items():
        if other_id == target_user_id:
            continue

        similarity = _user_cosine(target_ratings, other_ratings)
        if similarity <= 0:
            continue

        for movie_id, rating in other_ratings.items():
            if rating < 3:
                continue

            i = index_by_id.get(movie_id)
            if i is not None:
                scores[i] += similarity * rating

    peak = max(scores, default=0.0)
    if peak <= 0:
        return None

    return [score / peak for score in scores]


def recommend_hybrid(
    target_user_id,
    favorites,
    ratings,
    all_ratings,
    top_n=4,
    content_weight=0.7,
    collaborative_weight=0.3,
):
    model = _get_model()
    movies = model["movies"]
    favorites = {int(movie_id) for movie_id in (favorites or [])}
    ratings = {
        int(movie_id): int(rating)
        for movie_id, rating in (ratings or {}).items()
    }
    excluded = favorites | set(ratings.keys())

    content_scores = _content_scores(model, favorites, ratings)
    collaborative_scores = _collaborative_scores(
        target_user_id,
        all_ratings,
        model,
    )

    if content_scores is None and collaborative_scores is None:
        ranked = sorted(
            [
                (i, movie["rating"])
                for i, movie in enumerate(movies)
                if movie["id"] not in excluded
            ],
            key=lambda item: item[1],
            reverse=True,
        )
        algorithm = "popularity"

    elif collaborative_scores is None:
        ranked = sorted(
            [
                (i, content_scores[i])
                for i, movie in enumerate(movies)
                if movie["id"] not in excluded
            ],
            key=lambda item: item[1],
            reverse=True,
        )
        algorithm = "content"

    else:
        blended = [
            (
                i,
                (content_scores[i] if content_scores else 0.0) * content_weight
                + collaborative_scores[i] * collaborative_weight,
            )
            for i, movie in enumerate(movies)
            if movie["id"] not in excluded
        ]
        ranked = sorted(blended, key=lambda item: item[1], reverse=True)
        algorithm = "hybrid"

    top = ranked[:top_n]
    max_score = max((score for _, score in top), default=1.0) or 1.0
    recommendations = [
        _serialize(movies[i], score / max_score)
        for i, score in top
    ]

    return {
        "recommendations": recommendations,
        "algorithm": algorithm,
    }
