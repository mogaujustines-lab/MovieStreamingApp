import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

from recommender import get_all_movies, recommend_for_movie, recommend_for_query, recommend_collaborative, recommend_hybrid

app = Flask(__name__)
app.secret_key = os.environ.get("MOVIEMATE_SECRET_KEY", "moviemate-local-demo-change-before-deploy")
DATABASE_PATH = Path(__file__).resolve().parent / "data" / "moviemate.sqlite3"


@contextmanager
def get_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db():
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS activity (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                movie_id INTEGER NOT NULL,
                favorite INTEGER NOT NULL DEFAULT 0,
                rating INTEGER,
                PRIMARY KEY (user_id, movie_id)
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS search_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                query TEXT NOT NULL,
                matched_movie TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    with get_db() as connection:
        return connection.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()


init_db()


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/styles.css")
def styles():
    return send_from_directory(".", "styles.css")


@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")


@app.route("/api/movies")
def movies_api():
    return jsonify(get_all_movies())


@app.route("/api/recommend")
def recommend_api():
    movie_id = request.args.get("movie_id", default=1, type=int)
    recommendations = recommend_for_movie(movie_id, top_n=4)
    return jsonify(recommendations)


@app.route("/api/recommendations")
def recommendations_api():
    query = request.args.get("q", "").strip()[:120]
    user = current_user()
    favorites = []
    ratings = {}

    if user is not None:
        with get_db() as connection:
            activity = connection.execute(
                "SELECT movie_id, favorite, rating FROM activity WHERE user_id = ?",
                (user["id"],),
            ).fetchall()
            favorites = [row["movie_id"] for row in activity if row["favorite"]]
            ratings = {
                str(row["movie_id"]): row["rating"]
                for row in activity
                if row["rating"] is not None
            }

    result = recommend_for_query(query, favorites=favorites, ratings=ratings)
    if user is not None and query:
        with get_db() as connection:
            connection.execute(
                "INSERT INTO search_events (user_id, query, matched_movie) VALUES (?, ?, ?)",
                (user["id"], query, result["matched_movie"]),
            )
    return jsonify(result)

@app.route("/api/recommend/collaborative")
def recommend_collaborative_api():
    user = current_user()
    if user is None:
        return jsonify({"recommendations": [], "reason": "not_signed_in"})

    with get_db() as connection:
        rows = connection.execute(
            "SELECT user_id, movie_id, rating FROM activity WHERE rating IS NOT NULL"
        ).fetchall()

    all_ratings = [{"user_id": row["user_id"], "movie_id": row["movie_id"], "rating": row["rating"]} for row in rows]
    result = recommend_collaborative(user["id"], all_ratings)
    return jsonify(result)

@app.route("/api/recommend/hybrid")
def recommend_hybrid_api():
    user = current_user()
    if user is None:
        return jsonify({"recommendations": [], "algorithm": "signed_out"})

    with get_db() as connection:
        activity = connection.execute(
            "SELECT movie_id, favorite, rating FROM activity WHERE user_id = ?", (user["id"],)
        ).fetchall()
        all_rows = connection.execute(
            "SELECT user_id, movie_id, rating FROM activity WHERE rating IS NOT NULL"
        ).fetchall()

    favorites = [row["movie_id"] for row in activity if row["favorite"]]
    ratings = {row["movie_id"]: row["rating"] for row in activity if row["rating"] is not None}
    all_ratings = [
        {"user_id": row["user_id"], "movie_id": row["movie_id"], "rating": row["rating"]}
        for row in all_rows
    ]

    result = recommend_hybrid(user["id"], favorites, ratings, all_ratings)
    return jsonify(result)


@app.route("/api/auth/register", methods=["POST"])
def register_api():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))
    if not name or "@" not in email or len(password) < 8:
        return jsonify({"error": "Enter a name, valid email, and password with at least 8 characters."}), 400

    try:
        with get_db() as connection:
            cursor = connection.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password)),
            )
            session["user_id"] = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({"error": "An account with that email already exists. Sign in instead."}), 409

    return jsonify({"user": {"name": name, "email": email}, "favorites": [], "ratings": {}}), 201


@app.route("/api/auth/login", methods=["POST"])
def login_api():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))
    with get_db() as connection:
        user = connection.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Email or password is incorrect."}), 401
        session["user_id"] = user["id"]
        activity = connection.execute(
            "SELECT movie_id, favorite, rating FROM activity WHERE user_id = ?", (user["id"],)
        ).fetchall()

    return jsonify({
        "user": {"name": user["name"], "email": user["email"]},
        "favorites": [row["movie_id"] for row in activity if row["favorite"]],
        "ratings": {str(row["movie_id"]): row["rating"] for row in activity if row["rating"] is not None},
    })


@app.route("/api/auth/logout", methods=["POST"])
def logout_api():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/profile", methods=["GET", "PUT"])
def profile_api():
    user = current_user()
    if user is None:
        if request.method == "GET":
            return jsonify({"user": None, "favorites": [], "ratings": {}})
        return jsonify({"error": "Sign in to save your profile."}), 401

    if request.method == "PUT":
        payload = request.get_json(silent=True) or {}
        favorites = {int(item) for item in payload.get("favorites", []) if str(item).isdigit()}
        ratings = {
            int(movie_id): int(rating)
            for movie_id, rating in payload.get("ratings", {}).items()
            if str(movie_id).isdigit() and str(rating).isdigit() and 1 <= int(rating) <= 5
        }
        with get_db() as connection:
            connection.execute("DELETE FROM activity WHERE user_id = ?", (user["id"],))
            movie_ids = favorites | ratings.keys()
            connection.executemany(
                "INSERT INTO activity (user_id, movie_id, favorite, rating) VALUES (?, ?, ?, ?)",
                [(user["id"], movie_id, int(movie_id in favorites), ratings.get(movie_id)) for movie_id in movie_ids],
            )
        return jsonify({"ok": True})

    with get_db() as connection:
        activity = connection.execute(
            "SELECT movie_id, favorite, rating FROM activity WHERE user_id = ?", (user["id"],)
        ).fetchall()
    return jsonify({
        "user": {"name": user["name"], "email": user["email"]},
        "favorites": [row["movie_id"] for row in activity if row["favorite"]],
        "ratings": {str(row["movie_id"]): row["rating"] for row in activity if row["rating"] is not None},
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
