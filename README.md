# 🔥 FitFlix — Gym Exercise Recommendation System

> A Netflix-inspired workout recommender built with Streamlit, Machine Learning & Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📸 Preview

> Dark Netflix-style UI with horizontal navigation, hero banner, exercise cards, and AI-powered predictions.

---

## ✨ Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Hero banner, key stats, Top Picks, and Trending by Muscle section |
| 📊 **Analytics** | Interactive charts — body part distribution, difficulty pie, rating histogram, heatmap |
| 🎯 **Recommendations** | Content-based filtering using TF-IDF + Cosine Similarity |
| 🤖 **Difficulty Predictor** | ML model predicts Beginner / Intermediate / Expert from your inputs |

---

## 🗂️ Project Structure

```
fitflix/
│
├── app.py                  # Main Streamlit application
├── gym.ipynb               # Data preprocessing & model training notebook
├── megaGymDataset.csv      # Raw dataset
│
├── gym_data.pkl            # Cleaned DataFrame
├── similarity.pkl          # Cosine similarity matrix
├── difficulty_model.pkl    # Trained classification model
├── tfidf.pkl               # TF-IDF vectorizer
├── label_encoder.pkl       # Label encoder for difficulty levels
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fitflix.git
cd fitflix
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 📦 Requirements

Create a `requirements.txt` with:

```
streamlit
pandas
numpy
scikit-learn
matplotlib
seaborn
scipy
pickle5
```

---

## 🧠 How It Works

### Recommendation Engine
- Exercises are vectorized using **TF-IDF** on their type, body part, and equipment fields
- **Cosine Similarity** is computed across all exercises
- Given a selected exercise, the top 10 most similar are returned

### Difficulty Predictor
- Input: Exercise Type + Body Part + Equipment
- A trained **classification model** (e.g. Random Forest / Logistic Regression) predicts the difficulty level
- Output: `Beginner`, `Intermediate`, or `Expert`

---

## 📊 Dataset

**megaGymDataset.csv** — contains gym exercises with:
- `Title` — exercise name
- `BodyPart` — target muscle group
- `Equipment` — required equipment
- `Level` — difficulty (Beginner / Intermediate / Expert)
- `Type` — exercise category (Strength, Cardio, etc.)
- `Rating` — community rating

---

## 🎨 UI Design

- **Theme:** Netflix-inspired dark UI (`#0f1117` background, `#e50914` red accents)
- **Fonts:** Bebas Neue (display) + Barlow (body)
- **Navigation:** Horizontal pill-style navbar with active state highlighting
- **Cards:** Hover animations with red underline reveal effect

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Arpit**  
[![GitHub](https://img.shields.io/badge/GitHub-follow-black?style=flat&logo=github)](https://github.com/your-username)
