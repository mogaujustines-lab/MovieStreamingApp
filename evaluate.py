import random
from recommender import _get_model, _content_scores, _collaborative_scores, _serialize

random.seed(42)

K = 4  # top-K recommendations evaluated
NUM_SIMULATED_USERS = 40


def build_simulated_users(movies):
    all_genres = sorted({genre for movie in movies for genre in movie["genres"]})
    users = []

    for user_id in range(1, NUM_SIMULATED_USERS + 1):
        preferred_genres = random.sample(all_genres, k=random.choice([1, 2]))
        liked_movies = [
            movie for movie in movies
            if any(genre in preferred_genres for genre in movie["genres"])
        ]
        disliked_movies = [
            movie for movie in movies
            if not any(genre in preferred_genres for genre in movie["genres"])
        ]
        random.shuffle(liked_movies)
        random.shuffle(disliked_movies)

        liked_sample = liked_movies[:8] if len(liked_movies) >= 8 else liked_movies
        disliked_sample = disliked_movies[:3] if len(disliked_movies) >= 3 else disliked_movies

        if len(liked_sample) < 4:
            continue  # not enough signal to build a meaningful train/test split

        split_point = max(1, int(len(liked_sample) * 0.7))
        train_liked = liked_sample[:split_point]
        test_liked = liked_sample[split_point:]
        if not test_liked:
            continue

        users.append({
            "user_id": user_id,
            "train_ratings": {movie["id"]: 5 for movie in train_liked}
                              | {movie["id"]: 2 for movie in disliked_sample},
            "test_relevant_ids": {movie["id"] for movie in test_liked},
        })

    return users


def precision_recall_f1(recommended_ids, relevant_ids, k):
    top_k = recommended_ids[:k]
    hits = len(set(top_k) & relevant_ids)
    precision = hits / k if k else 0
    recall = hits / len(relevant_ids) if relevant_ids else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0
    return precision, recall, f1


def evaluate_content(users, model):
    movies = model["movies"]
    totals = {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    for user in users:
        scores = _content_scores(model, favorites=[], ratings=user["train_ratings"])
        if scores is None:
            continue
        excluded = set(user["train_ratings"].keys())
        ranked = sorted(
            [(movies[i]["id"], score) for i, score in enumerate(scores) if movies[i]["id"] not in excluded],
            key=lambda item: item[1], reverse=True,
        )
        recommended_ids = [movie_id for movie_id, _ in ranked]
        p, r, f1 = precision_recall_f1(recommended_ids, user["test_relevant_ids"], K)
        totals["precision"] += p
        totals["recall"] += r
        totals["f1"] += f1

    count = len(users)
    return {key: value / count for key, value in totals.items()}


def evaluate_collaborative(users, model):
    movies = model["movies"]
    all_ratings = [
        {"user_id": user["user_id"], "movie_id": movie_id, "rating": rating}
        for user in users
        for movie_id, rating in user["train_ratings"].items()
    ]
    totals = {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    for user in users:
        scores = _collaborative_scores(user["user_id"], all_ratings, model)
        if scores is None:
            continue
        excluded = set(user["train_ratings"].keys())
        ranked = sorted(
            [(movies[i]["id"], score) for i, score in enumerate(scores) if movies[i]["id"] not in excluded],
            key=lambda item: item[1], reverse=True,
        )
        recommended_ids = [movie_id for movie_id, _ in ranked]
        p, r, f1 = precision_recall_f1(recommended_ids, user["test_relevant_ids"], K)
        totals["precision"] += p
        totals["recall"] += r
        totals["f1"] += f1

    count = len(users)
    return {key: value / count for key, value in totals.items()}


def evaluate_hybrid(users, model, content_weight=0.7, collaborative_weight=0.3):
    movies = model["movies"]
    all_ratings = [
        {"user_id": user["user_id"], "movie_id": movie_id, "rating": rating}
        for user in users
        for movie_id, rating in user["train_ratings"].items()
    ]
    totals = {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    for user in users:
        content_scores = _content_scores(model, favorites=[], ratings=user["train_ratings"])
        collaborative_scores = _collaborative_scores(user["user_id"], all_ratings, model)
        if content_scores is None or collaborative_scores is None:
            continue

        excluded = set(user["train_ratings"].keys())
        blended = [
            (movies[i]["id"], content_scores[i] * content_weight + collaborative_scores[i] * collaborative_weight)
            for i in range(len(movies)) if movies[i]["id"] not in excluded
        ]
        blended.sort(key=lambda item: item[1], reverse=True)
        recommended_ids = [movie_id for movie_id, _ in blended]
        p, r, f1 = precision_recall_f1(recommended_ids, user["test_relevant_ids"], K)
        totals["precision"] += p
        totals["recall"] += r
        totals["f1"] += f1

    count = len(users)
    return {key: value / count for key, value in totals.items()}

def sweep_hybrid_weights(users, model):
    print("\nHybrid weight experiment")
    print(f"{'Content':<10}{'Collab':<10}{'Precision@4':<14}{'Recall@4':<12}{'F1@4':<10}")
    print("-" * 56)
    best = None
    for step in range(0, 11):
        content_weight = step / 10
        collaborative_weight = round(1 - content_weight, 1)
        scores = evaluate_hybrid(users, model, content_weight, collaborative_weight)
        print(
            f"{content_weight:<10.1f}{collaborative_weight:<10.1f}"
            f"{scores['precision']*100:<14.1f}{scores['recall']*100:<12.1f}{scores['f1']*100:<10.1f}"
        )
        if best is None or scores["f1"] > best[1]["f1"]:
            best = (content_weight, scores)
    print(
        f"\nBest blend: {best[0]:.1f} content / {1 - best[0]:.1f} collaborative "
        f"(F1 {best[1]['f1']*100:.1f}%)"
    )    


def main():
    model = _get_model()
    users = build_simulated_users(model["movies"])
    print(f"Evaluating with {len(users)} simulated users, top-{K} recommendations\n")

    results = {
        "Content-Based": evaluate_content(users, model),
        "Collaborative": evaluate_collaborative(users, model),
        "Hybrid": evaluate_hybrid(users, model),
    }

    print(f"{'Model':<15}{'Precision@' + str(K):<15}{'Recall@' + str(K):<15}{'F1@' + str(K):<15}")
    print("-" * 60)
    for name, scores in results.items():
        print(f"{name:<15}{scores['precision']*100:>6.1f}%       {scores['recall']*100:>6.1f}%       {scores['f1']*100:>6.1f}%")
    sweep_hybrid_weights(users, model)

if __name__ == "__main__":
    main()