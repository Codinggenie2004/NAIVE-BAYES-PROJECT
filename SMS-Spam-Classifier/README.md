# 🛡️ SMS Spam Classifier

A web-based SMS spam detection application powered by a **Multinomial Naive Bayes** machine learning model, built with **Flask** and **scikit-learn**. It classifies SMS messages as **Spam** or **Ham** (not spam) in real-time with confidence scores.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)

---

## ✨ Features

- **Real-time Classification** — Type or paste any SMS and get instant spam/ham predictions
- **Confidence Scores** — View spam & ham probability breakdowns with animated progress bars
- **Model Performance Dashboard** — Live accuracy, precision, recall, and F1 score metrics
- **Confusion Matrix** — Visual confusion matrix for model evaluation
- **Sample Messages** — Pre-loaded spam and ham examples for quick testing
- **Premium Dark UI** — Glassmorphism design with smooth animations and responsive layout
- **Keyboard Shortcut** — Press `Enter` to classify instantly

---

## 🧠 How It Works

1. The **SMS Spam Collection** dataset (5,574 real messages from UCI) is loaded on startup
2. Messages are tokenized and vectorized using `CountVectorizer`
3. A **Multinomial Naive Bayes** classifier is trained on a 70/30 train-test split
4. The Flask server exposes REST API endpoints for predictions and model statistics
5. The frontend sends messages via `fetch()` and renders results dynamically

---

## 📁 Project Structure

```
SMS-Spam-Classifier/
├── app.py                 # Flask web server (routes & API endpoints)
├── model.py               # ML model — training, prediction, evaluation
├── requirements.txt       # Python dependencies
├── data/
│   └── SMSSpamCollection  # UCI SMS Spam Collection dataset (tab-separated)
├── templates/
│   └── index.html         # Main web UI (Jinja2 template)
└── static/
    ├── style.css           # Premium dark glassmorphism styles
    └── script.js           # Frontend logic (classify, stats, samples)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/SMS-Spam-Classifier.git
   cd SMS-Spam-Classifier
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 📦 Production Deployment

To prepare the application for production, we have added configurations that support containerization, fast start times through model serialization, and industrial-grade web server processes.

### 1. Model Pre-Training (Recommended)
Before launching the production server, pre-train and serialize the Naive Bayes model to disk. This prevents the server from needing to train on startup and speeds up process initialization (especially under multi-worker environments like Gunicorn).

From the repository root, run:
```bash
python SMS-Spam-Classifier/train.py
```
This generates `model.pkl`, `vectorizer.pkl`, and `metrics.json` inside the `SMS-Spam-Classifier` folder. The web server will automatically load these files on startup in less than 5ms.

### 2. Deploying to Render (One-Click Blueprint)
This repository includes a `render.yaml` configuration.
1. Push this repository to your GitHub account.
2. Go to the [Render Dashboard](https://dashboard.render.com/).
3. Click **New** > **Blueprint**.
4. Connect your GitHub repository.
5. Render will automatically detect `render.yaml` and configure the Web Service, environment variables, build steps, and pre-training steps.

### 3. Deploying to Heroku / Railway (via Procfile)
The included `Procfile` is placed at the project root to support platforms that detect process files.
- **Build Command / Nixpacks**: Ensure you install the production-ready packages using:
  ```bash
  pip install -r SMS-Spam-Classifier/requirements-prod.txt && python SMS-Spam-Classifier/train.py
  ```
- **Process Entry**: The system will automatically spin up Gunicorn using the `web` process in the `Procfile`:
  ```bash
  gunicorn --bind 0.0.0.0:$PORT --chdir SMS-Spam-Classifier app:app
  ```

### 4. Deploying via Docker (Containerization)
A multi-stage `Dockerfile` is provided in the project root. It handles both model training and lightweight runtime isolation.

1. **Build the Docker Image**:
   ```bash
   docker build -t sms-spam-classifier .
   ```
2. **Run the Container**:
   ```bash
   docker run -d -p 5000:5000 -e PORT=5000 sms-spam-classifier
   ```

### 5. Running Production Server Locally
If you want to test the production setup locally:

- **Linux / macOS (using Gunicorn)**:
  ```bash
  pip install -r SMS-Spam-Classifier/requirements-prod.txt
  export FLASK_ENV=production
  gunicorn --bind 0.0.0.0:5000 --chdir SMS-Spam-Classifier app:app
  ```
- **Windows (using Waitress)**:
  Gunicorn is not supported on Windows. Use `waitress` instead:
  ```bash
  pip install waitress
  set FLASK_ENV=production
  waitress-serve --port=5000 SMS-Spam-Classifier.app:app
  ```

---


## 🔌 API Endpoints

| Method | Endpoint    | Description                       |
|--------|-------------|-----------------------------------|
| GET    | `/`         | Serves the main web UI            |
| POST   | `/predict`  | Classify a message as spam or ham |
| GET    | `/stats`    | Returns model performance metrics |

### Example — Classify a message

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! You won a free iPhone. Call now!"}'
```

**Response:**
```json
{
  "prediction": "spam",
  "confidence": 99.85,
  "spam_probability": 99.85,
  "ham_probability": 0.15
}
```

---

## 📊 Model Details

| Parameter          | Value                           |
|--------------------|---------------------------------|
| Algorithm          | Multinomial Naive Bayes         |
| Vectorizer         | CountVectorizer (min_df=2)      |
| Train / Test Split | 70% / 30%                       |
| Smoothing (alpha)  | 1.0                             |
| Dataset            | SMS Spam Collection (UCI)       |
| Total Samples      | 5,574                           |

---

## 🛠️ Tech Stack

- **Backend** — Python, Flask
- **ML** — scikit-learn (MultinomialNB), pandas, NumPy
- **Frontend** — HTML5, CSS3 (glassmorphism), vanilla JavaScript
- **Font** — [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [SMS Spam Collection Dataset](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection) — UCI Machine Learning Repository
- [scikit-learn](https://scikit-learn.org/) — Machine Learning in Python
- [Flask](https://flask.palletsprojects.com/) — Lightweight WSGI web framework
