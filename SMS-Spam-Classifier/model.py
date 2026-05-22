"""
SMS Spam Classifier — Model Module
Uses scikit-learn's MultinomialNB (Naive Bayes) to classify SMS messages as spam or ham.
Mirrors the approach from the PySpark Naive Bayes Spam Classifier notebook.
"""

import os
import pickle
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# ── Paths ────────────────────────────────────────────────────────────────────
_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(_DIR, "vectorizer.pkl")
METRICS_PATH = os.path.join(_DIR, "metrics.json")
DATA_PATH = os.path.join(_DIR, "data", "SMSSpamCollection")

# ── Globals ──────────────────────────────────────────────────────────────────
_model = None
_vectorizer = None
_stats = {}


def load_model() -> bool:
    """Attempt to load the serialized model, vectorizer, and metrics from disk."""
    global _model, _vectorizer, _stats
    
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH) and os.path.exists(METRICS_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                _vectorizer = pickle.load(f)
            with open(METRICS_PATH, "r") as f:
                _stats = json.load(f)
            print("🚀 Loaded pre-trained model and metrics from disk.")
            return True
        except Exception as e:
            print(f"⚠️ Warning: Failed to load pre-trained model ({e}). Re-training...")
            _model = None
            _vectorizer = None
            _stats = {}
    return False


def train_model():
    """Load dataset, vectorize text, train Naive Bayes, and store metrics."""
    global _model, _vectorizer, _stats

    # 1. Load dataset  (tab-separated, no header — same as PySpark notebook)
    df = pd.read_csv(DATA_PATH, sep="\t", header=None, names=["label", "message"])

    # 2. Encode labels: ham → 0, spam → 1
    df["label_num"] = df["label"].map({"ham": 0, "spam": 1})

    # 3. Train / test split (70/30, same ratio as notebook)
    X_train, X_test, y_train, y_test = train_test_split(
        df["message"], df["label_num"], test_size=0.3, random_state=2018
    )

    # 4. CountVectorizer  (mirrors RegexTokenizer + CountVectorizer in PySpark)
    _vectorizer = CountVectorizer(token_pattern=r"\w+", min_df=2)
    X_train_vec = _vectorizer.fit_transform(X_train)
    X_test_vec = _vectorizer.transform(X_test)

    # 5. Multinomial Naive Bayes  (smoothing=1.0, same as notebook)
    _model = MultinomialNB(alpha=1.0)
    _model.fit(X_train_vec, y_train)

    # 6. Evaluate
    y_pred = _model.predict(X_test_vec)
    cm = confusion_matrix(y_test, y_pred).tolist()

    _stats = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred) * 100, 2),
        "recall": round(recall_score(y_test, y_pred) * 100, 2),
        "f1": round(f1_score(y_test, y_pred) * 100, 2),
        "confusion_matrix": cm,
        "total_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "spam_count": int(df["label_num"].sum()),
        "ham_count": int((df["label_num"] == 0).sum()),
        "vocab_size": len(_vectorizer.vocabulary_),
    }

    # Save to disk for production deployment readiness
    try:
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(_model, f)
        with open(VECTORIZER_PATH, "wb") as f:
            pickle.dump(_vectorizer, f)
        with open(METRICS_PATH, "w") as f:
            json.dump(_stats, f)
        print("💾 Serialized model, vectorizer, and metrics to disk.")
    except Exception as e:
        print(f"⚠️ Warning: Could not save model to disk ({e})")

    print(f"✅  Model trained — Accuracy: {_stats['accuracy']}%")
    return _stats


def predict(message: str) -> dict:
    """Predict whether a single SMS message is spam or ham."""
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not load_model():
            train_model()

    vec = _vectorizer.transform([message])
    prediction = _model.predict(vec)[0]
    probabilities = _model.predict_proba(vec)[0]

    return {
        "prediction": "spam" if prediction == 1 else "ham",
        "confidence": round(float(max(probabilities)) * 100, 2),
        "spam_probability": round(float(probabilities[1]) * 100, 2),
        "ham_probability": round(float(probabilities[0]) * 100, 2),
    }


def get_stats() -> dict:
    """Return cached model performance stats."""
    global _stats
    if not _stats:
        if not load_model():
            train_model()
    return _stats

