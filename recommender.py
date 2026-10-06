import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = Path(__file__).resolve().parent / "data" / "movies.csv"

_model_cache = {"mtime": None, "movies": None, "matrix": None, "similarity": None, "vectorizer": None}


def load_movies():
    movies = []
    with DATA_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            movie = {
                "id": int(row["id"]),
                "title": row["title"],
                "genres": row["genres"].split("|") if row.get("genres") else [],
                "year": int(row["year"]),
                "rating": float(row["rating"]),
                "director": row["director"],
                "cast": [item.strip() for item in str(row.get("cast", "")).split("|") if item.strip()],
                "keywords": [item.strip() for item in str(row.get("keywords", "")).split("|") if item.strip()],
                "description": row["description"],
                "poster_url": row["poster_url"],
            }
            movies.append(movie)
    return sorted(movies, key=lambda item: item["rating"], reverse=True)


def build_feature_text(movie):
    # Genres, keywords, director and cast are repeated to weight them
    # more heavily than the free-text description in the TF-IDF model.
    parts = [
        (" ".join(movie.get("genres", [])) + " ") * 3,
        (" ".join(movie.get("keywords", [])) + " ") * 3,
        (movie.get("director", "") + " ") * 2,
        " ".join(movie.get("cast", [])),
        movie.get("description", ""),
    ]
    return " ".join(part for part in parts if part)


def _get_model():
    """Builds (and caches) the TF-IDF matrix and cosine similarity matrix
    for the current movies.csv. Rebuilds automatically if the file changes."""
    mtime = DATA_PATH.stat().st_mtime
    if _model_cache["mtime"] == mtime:
        return _model_cache

    movies = load_movies()
    feature_texts = [build_feature_text(movie) for movie in movies]

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(feature_texts)
    similarity = cosine_similarity(matrix)

    _model_cache.update({
        "mtime": mtime,
        "movies": movies,
        "matrix": matrix,
        "similarity": similarity,
        "vectorizer": vectorizer,
    })
    return _model_cache

def recommend_collaborative(target_user_id, all_ratings, top_n=4):
    """
    all_ratings: list of dicts like {"user_id": int, "movie_id": int, "rating": int}
    covering every user's ratings, not just the target user's.
    """
    model = _get_model()
    movies = model["movies"]
    movie_ids = [movie["id"] for movie in movies]
    movie_index = {movie_id: i for i, movie_id in enumerate(movie_ids)}

    user_ids = sorted({row["user_id"] for row in all_ratings})
    if target_user_id not in user_ids or len(user_ids) < 2:
        return {"recommendations": [], "reason": "not_enough_data"}

    user_index = {user_id: i for i, user_id in enumerate(user_ids)}

    import numpy as np
    matrix = np.zeros((len(user_ids), len(movie_ids)))
    for row in all_ratings:
        if row["movie_id"] in movie_index:
            matrix[user_index[row["user_id"]], movie_index[row["movie_id"]]] = row["rating"]

    target_row = matrix[user_index[target_user_id]]
    if not target_row.any():
        return {"recommendations": [], "reason": "target_has_no_ratings"}

    similarities = cosine_similarity(matrix)[user_index[target_user_id]]

    scores = np.zeros(len(movie_ids))
    weight_totals = np.zeros(len(movie_ids))
    for other_id, other_index in user_index.items():
        if other_id == target_user_id:
            continue
        similarity = similarities[other_index]
        if similarity <= 0:
            continue
        other_row = matrix[other_index]
        rated_mask = other_row > 0
        scores[rated_mask] += other_row[rated_mask] * similarity
        weight_totals[rated_mask] += similarity

    already_rated = target_row > 0
    with np.errstate(invalid="ignore", divide="ignore"):
        predicted = np.where(weight_totals > 0, scores / weight_totals, 0)
    predicted[already_rated] = -1

    ranked_indices = predicted.argsort()[::-1][:top_n]
    recommendations = [
        _serialize(movies[i], predicted[i] / 5)
        for i in ranked_indices
        if predicted[i] > 0
    ]

    return {"recommendations": recommendations, "reason": "ok" if recommendations else "no_overlap"}


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
        payload["similarity"] = round(similarity * 100, 1)
    return payload


def recommend_for_movie(movie_id, top_n=4):
    model = _get_model()
    movies = model["movies"]
    similarity = model["similarity"]

    index = _movie_index(movies, movie_id)
    if index is None:
        return []

    scores = [item for item in enumerate(similarity[index]) if item[0] != index]
    scores.sort(key=lambda item: item[1], reverse=True)

    return [_serialize(movies[i], score) for i, score in scores[:top_n]]


def recommend_for_query(query="", favorites=None, ratings=None, top_n=4):
    model = _get_model()
    movies = model["movies"]
    matrix = model["matrix"]
    similarity = model["similarity"]
    vectorizer = model["vectorizer"]

    favorites = {int(movie_id) for movie_id in (favorites or [])}
    ratings = {int(movie_id): int(rating) for movie_id, rating in (ratings or {}).items()}
    search = str(query or "").strip().lower()

    matched_movie = None
    matched_index = None
    if search:
        title_matches = [
            (i, movie) for i, movie in enumerate(movies) if search in movie["title"].lower()
        ]
        if title_matches:
            matched_index, matched_movie = max(
                title_matches,
                key=lambda pair: (pair[1]["title"].lower() == search, pair[1]["rating"]),
            )
        else:
            # No title contains the query text — fall back to the TF-IDF
            # model itself: vectorize the typed text and compare it against
            # every movie the same way movies are compared to each other.
            query_vector = vectorizer.transform([search])
            query_similarity = cosine_similarity(query_vector, matrix)[0]
            best_index = int(query_similarity.argmax())
            if query_similarity[best_index] > 0:
                matched_index, matched_movie = best_index, movies[best_index]

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

    excluded = favorites | ratings.keys()
    if matched_movie:
        excluded.add(matched_movie["id"])

    ranked = [(i, score) for i, score in enumerate(scores) if movies[i]["id"] not in excluded]
    ranked.sort(key=lambda item: item[1], reverse=True)

    max_score = max((score for _, score in ranked), default=1) or 1
    recommendations = []
    for i, score in ranked[:top_n]:
        movie = movies[i]
        recommendations.append({
            **_serialize(movie),
            "similarity": round(min(99, max(0, score / max_score * 100)), 1),
            "match_reason": (
                f"Similar to {matched_movie['title']}"
                if matched_movie
                else "Matches your saved preferences" if preference_rows else "Popular with MovieMate viewers"
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
    max_score = max(scores) or 1
    return [score / max_score for score in scores]


def _collaborative_scores(target_user_id, all_ratings, model):
    import numpy as np
    movies = model["movies"]
    movie_ids = [movie["id"] for movie in movies]
    movie_index = {movie_id: i for i, movie_id in enumerate(movie_ids)}

    user_ids = sorted({row["user_id"] for row in all_ratings})
    if target_user_id not in user_ids or len(user_ids) < 2:
        return None

    user_index = {user_id: i for i, user_id in enumerate(user_ids)}
    matrix = np.zeros((len(user_ids), len(movie_ids)))
    for row in all_ratings:
        if row["movie_id"] in movie_index:
            matrix[user_index[row["user_id"]], movie_index[row["movie_id"]]] = row["rating"]

    if not matrix[user_index[target_user_id]].any():
        return None

    similarities = cosine_similarity(matrix)[user_index[target_user_id]]
    liked = matrix >= 3  # only neighbours' positive ratings count as votes

    scores = np.zeros(len(movie_ids))
    for other_id, other_index in user_index.items():
        if other_id == target_user_id:
            continue
        similarity = similarities[other_index]
        if similarity <= 0:
            continue
        mask = liked[other_index]
        scores[mask] += similarity * matrix[other_index][mask]

    peak = scores.max()
    if peak <= 0:
        return None
    return (scores / peak).tolist()


def recommend_hybrid(target_user_id, favorites, ratings, all_ratings, top_n=4,
                      content_weight=0.7, collaborative_weight=0.3):
    model = _get_model()
    movies = model["movies"]
    excluded = set(favorites) | set(ratings.keys())

    content_scores = _content_scores(model, favorites, ratings)
    collaborative_scores = _collaborative_scores(target_user_id, all_ratings, model)

    if content_scores is None and collaborative_scores is None:
        ranked = sorted(
            [(i, movie["rating"]) for i, movie in enumerate(movies) if movie["id"] not in excluded],
            key=lambda item: item[1], reverse=True,
        )
        algorithm = "popularity"
    elif collaborative_scores is None:
        ranked = sorted(
            [(i, content_scores[i]) for i, movie in enumerate(movies) if movie["id"] not in excluded],
            key=lambda item: item[1], reverse=True,
        )
        algorithm = "content"
    else:
        blended = [
            (i, (content_scores[i] if content_scores else 0) * content_weight
                + collaborative_scores[i] * collaborative_weight)
            for i, movie in enumerate(movies) if movie["id"] not in excluded
        ]
        ranked = sorted(blended, key=lambda item: item[1], reverse=True)
        algorithm = "hybrid"

    top = ranked[:top_n]
    max_score = max((score for _, score in top), default=1) or 1
    recommendations = [_serialize(movies[i], score / max_score) for i, score in top]
    return {"recommendations": recommendations, "algorithm": algorithm}