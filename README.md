# CineCue 🎬
**CS50x Final Project Submission**

🎥 **Video Demo:** [https://your-demo-link-here](https://your-demo-link-here)

---

## 📜 Description

CineCue is a personalized movie rating web application built as the final project for CS50x. It allows users to add movies simply by name, and automatically fetches metadata from the OMDb API, including:

- IMDb rating
- Plot
- Poster
- Release year

Users can assign their own personal ratings and keep track of their movie-watching history in a secure, private, and intuitive interface.

---

## 🚀 Features

- 🔐 **User Authentication**
  Secure login and registration using password hashing and session-based login.

- 🎞️ **Smart Movie Adding**
  Just type a movie title — AutoRate will pull the rest from the OMDb API.

- ⭐ **Personal Ratings**
  Rate movies from 0–10 and update your score at any time.

- 🧠 **Normalized Database Schema**
  Separate `ratings` table lets multiple users rate the same movie independently.

- 🧹 **User-Specific Lists**
  Each user has a private list of movies and ratings — no crossover.

- 🗑️ **Delete Movies**
  Users can remove a movie from their list with one click.

---

## 🧰 Technologies Used

- **Python** with Flask – backend server
- **SQLite** – relational database engine
- **Jinja2** – HTML templating
- **Bootstrap 5** – responsive styling
- **OMDb API** – movie data source
- **Werkzeug** – password hashing and secure sessions

---

## 📁 Project Structure

```
CineCue/
├── app.py
├── requirements.txt
├── schema.sql
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── watchlist.html
│   └── movie_card.html
├── static/
│   └── style.css
└── README.md
```

---

## ⚙️ How to Run

1. **Clone or download** the repository:

```bash
git clone https://github.com/PranavXD1/CineCue.git
cd CineCue
```

2. **Set up a virtual environment** (optional but recommended):

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Initialize the database**:

```bash
sqlite3 movies.db < schema.sql
```

5. **Run the app**:

```bash
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
flask run
```

6. **Visit in browser**:
   http://127.0.0.1:5000

---

## 🎬 OMDb API

This app uses the [OMDb API](https://www.omdbapi.com/) to fetch movie details.

- **API Key Used**: `9b7f8d79`
- You can get your own key here: [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

---

## 🧠 Design Decisions

- 🔗 **Normalized Schema**:
    - `users` — stores registered users
    - `movies` — stores movies globally (title, plot, genre, year, rating)
    - `ratings` — stores each user's rating for a movie (`user_id`, `movie_id`, `rating`)

- 🔒 **Security**:
    - Passwords are hashed using `werkzeug.security`.
    - Sessions protect user-specific views.

- 📸 **Poster Handling**:
    - Poster URLs are automatically upgraded to HTTPS to prevent browser blocks.

- 🎭 **Genre Support**:
    - Movie genre is fetched and displayed with title, plot, and ratings.

---

## ✅ Testing

The app has been tested for:

- ✅ Invalid or missing titles
- ✅ Missing poster/genre data from API
- ✅ User rating updates
- ✅ Flash messages and form validation
- ✅ Private data per user session
- ✅ Schema enforcement (no duplicate ratings per user/movie)

---

## 🎓 Final Thoughts

AutoRate combines everything I learned in **CS50x**, from backend development and databases to API integration and frontend styling. It’s a strong foundation for building more features like:

- Social movie sharing
- Watchlist reminders
- Collaborative recommendations

---

## 👨‍💻 Author Info

- **Name**: Pranav
- **GitHub**: [https://github.com/PranavXD1](https://github.com/PranavXD1)
- **edX Username**: pranav1080
- **Location**: New Delhi, India
- **Recorded On**: July 4, 2025

---

## 🏫 Course Info

- **CS50x Final Project** – Harvard University
- **Instructor**: David J. Malan

---

## 📽️ Demo Video

Insert your 3-minute unlisted YouTube video link below:
**Demo**: [https://your-demo-link-here](https://your-demo-link-here)
