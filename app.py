import os
import sqlite3
import requests
from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

USERS_DB = "users.db"
MOVIES_DB = "movies.db"
OMDB_API_KEY = "9b7f8d79"

def get_users_db():
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    return conn

def get_movies_db():
    conn = sqlite3.connect(MOVIES_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_users_db():
    with get_users_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

def init_movies_db():
    with get_movies_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imdb_id TEXT UNIQUE,
                title TEXT NOT NULL,
                genre TEXT,
                year TEXT,
                description TEXT,
                rating TEXT,
                poster TEXT,
                imdb_rating TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                user_id INTEGER,
                movie_id INTEGER,
                rating TEXT,
                note TEXT,
                PRIMARY KEY (user_id, movie_id)
            )
        """)

init_users_db()
init_movies_db()

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    with get_movies_db() as conn:
        rated = conn.execute("""
            SELECT m.*, r.rating AS user_rating, r.note
            FROM movies m
            JOIN ratings r ON m.id = r.movie_id
            WHERE r.user_id = ? AND r.rating IS NOT NULL
        """, (session["user_id"],)).fetchall()
    return render_template("index.html", rated_movies=rated)

@app.route("/watchlist")
def watchlist():
    if "user_id" not in session:
        return redirect("/login")
    with get_movies_db() as conn:
        watchlist = conn.execute("""
            SELECT m.*, r.rating AS user_rating, r.note
            FROM movies m
            JOIN ratings r ON m.id = r.movie_id
            WHERE r.user_id = ? AND (r.rating IS NULL OR r.rating = 'N/A')
        """, (session["user_id"],)).fetchall()
    return render_template("watchlist.html", watchlist_movies=watchlist)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Passwords do not match.")
            return redirect("/register")

        hashed = generate_password_hash(password)

        try:
            with get_users_db() as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
                flash("Registration successful. Please log in.")
                return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Username already taken.")
            return redirect("/register")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with get_users_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect("/")
            else:
                flash("Invalid credentials.")
                return redirect("/login")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect("/login")

@app.route("/search", methods=["POST"])
def search():
    title = request.form.get("title")
    response = requests.get(f"http://www.omdbapi.com/?s={title}&apikey={OMDB_API_KEY}")
    data = response.json()

    if data["Response"] == "True":
        results = data["Search"]
        return render_template("search_results.html", results=results)
    else:
        flash("No results found.")
        return redirect("/")

@app.route("/add/<imdb_id>")
def add_movie(imdb_id):
    if "user_id" not in session:
        return redirect("/login")

    response = requests.get(f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}")
    data = response.json()

    if data["Response"] == "True":
        with get_movies_db() as conn:
            movie = conn.execute("SELECT * FROM movies WHERE imdb_id = ?", (imdb_id,)).fetchone()
            if not movie:
                conn.execute("""
                    INSERT INTO movies (imdb_id, title, genre, year, description, rating, poster, imdb_rating)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    imdb_id,
                    data.get("Title"),
                    data.get("Genre"),
                    data.get("Year"),
                    data.get("Plot"),
                    data.get("Rated"),
                    data.get("Poster"),
                    data.get("imdbRating")
                ))
                movie_id = conn.execute("SELECT id FROM movies WHERE imdb_id = ?", (imdb_id,)).fetchone()["id"]
            else:
                movie_id = movie["id"]

            conn.execute("INSERT OR IGNORE INTO ratings (user_id, movie_id, rating, note) VALUES (?, ?, NULL, '')",
                         (session["user_id"], movie_id))

    return redirect("/")

@app.route("/rate/<int:movie_id>", methods=["POST"])
def rate(movie_id):
    if "user_id" not in session:
        return redirect("/login")

    new_rating = request.form.get("new_rating")

    with get_movies_db() as conn:
        conn.execute("""
            UPDATE ratings SET rating = ?
            WHERE user_id = ? AND movie_id = ?
        """, (new_rating, session["user_id"], movie_id))

    return redirect("/")

@app.route("/note/<int:movie_id>", methods=["POST"])
def note(movie_id):
    if "user_id" not in session:
        return redirect("/login")

    new_note = request.form.get("new_note")

    with get_movies_db() as conn:
        conn.execute("""
            UPDATE ratings SET note = ?
            WHERE user_id = ? AND movie_id = ?
        """, (new_note, session["user_id"], movie_id))

    return redirect(request.referrer or "/")

@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    if "user_id" not in session:
        return redirect("/login")

    with get_movies_db() as conn:
        conn.execute("DELETE FROM ratings WHERE user_id = ? AND movie_id = ?", (session["user_id"], movie_id))
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
