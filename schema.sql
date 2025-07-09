DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS ratings;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imdb_id TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    genre TEXT,
    year TEXT,
    description TEXT,
    rating TEXT,
    poster TEXT,
    imdb_rating TEXT
);

CREATE TABLE ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating TEXT,
    note TEXT,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
)
