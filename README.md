# 🎬 CineMatch — Movie Recommendation System
### S.Y.B.Sc. Computer Science | Mini Project CS-281-FP | Semester IV

---

## 📌 Project Overview

**CineMatch** is a content-based movie recommendation system built using Python and Flask. It uses **TF-IDF Vectorization** and **Cosine Similarity** to find movies similar to a user's input.

**Course:** CS-281-FP Mini Project  
**Algorithm:** Content-Based Filtering (TF-IDF + Cosine Similarity)  
**Dataset:** 30 popular movies with genres, cast, director, and description  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask |
| ML Algorithm | TF-IDF Vectorizer, Cosine Similarity |
| Libraries | scikit-learn, pandas, numpy |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Deployment | Render (free) |

---

## 🧠 How It Works

1. Each movie's **genres + director + cast + description** are combined into a single text string (called "tags")
2. **TF-IDF Vectorizer** converts these tags into numerical feature vectors
3. **Cosine Similarity** measures how similar any two movie vectors are
4. When a user searches a movie, the system finds the top 6 most similar movies

---

## 🚀 Deploy on Render (Free) — Step by Step

### Step 1: Create GitHub Repository
1. Go to [github.com](https://github.com) → Sign in
2. Click **"New Repository"**
3. Name it: `movie-recommender`
4. Keep it **Public** → Click **Create repository**

### Step 2: Upload Your Files
Upload these files to your GitHub repo:
```
movie-recommender/
├── app.py               ← Main Python backend
├── requirements.txt     ← Python dependencies
├── Procfile             ← Server start command
├── render.yaml          ← Render config
└── templates/
    └── index.html       ← Frontend UI
```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com) → Sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `movie-recommender` repository
5. Fill in:
   - **Name:** `cinematch`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click **"Create Web Service"**
7. Wait 2-3 minutes → Your live URL will be: `https://cinematch.onrender.com`

---

## 💻 Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
# Go to: http://localhost:5000
```

---

## 📂 File Structure

```
movie-recommender/
│
├── app.py                  # Flask backend + recommendation engine
│   ├── movies_data[]       # Dataset of 30 movies
│   ├── build_tags()        # Combines movie features into text
│   ├── TfidfVectorizer     # Converts text to vectors
│   ├── cosine_similarity   # Computes similarity scores
│   └── get_recommendations()  # Core recommendation function
│
├── templates/
│   └── index.html          # Full frontend (HTML + CSS + JS)
│       ├── Search input with autocomplete
│       ├── Quick-pick movie pills
│       ├── Results display with similarity %
│       └── Analysis Report section
│
├── requirements.txt        # Flask, scikit-learn, pandas, numpy, gunicorn
├── Procfile                # Gunicorn start command for deployment
└── render.yaml             # Render.com deployment configuration
```

---

## 🎯 Features

- ✅ Search any movie from the dataset
- ✅ Autocomplete suggestions while typing
- ✅ Shows top 6 similar movies with similarity %
- ✅ Analysis report (avg similarity, algorithm used)
- ✅ Click any recommendation to get its recommendations
- ✅ Fully responsive (works on mobile)
- ✅ Free online deployment

---

## 📊 Algorithm Details

### TF-IDF (Term Frequency-Inverse Document Frequency)
- Converts movie descriptions into numerical vectors
- Words that appear often in one movie but rarely in others get higher weight
- Captures what makes each movie unique

### Cosine Similarity
- Measures the angle between two movie vectors
- Value between 0 (completely different) and 1 (identical)
- Displayed as percentage in the UI

---

*Built for S.Y.B.Sc. Computer Science, Savitribai Phule Pune University*
