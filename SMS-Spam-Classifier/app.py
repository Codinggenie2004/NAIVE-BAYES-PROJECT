"""
SMS Spam Classifier — Flask Web Server
Serves a premium web UI and exposes prediction + stats API endpoints.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from model import predict, get_stats

# Configure stdout logging for production observability
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)

app = Flask(__name__)

# Apply ProxyFix middleware if running behind a reverse proxy (Render, Heroku, etc.)
if os.environ.get("FLASK_ENV") == "production" or os.environ.get("HTTP_X_FORWARDED_FOR"):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Preload/train model on startup to make the first request instant
logging.info("Initializing Naive Bayes model...")
get_stats()
logging.info("Model initialization complete.")


@app.route("/")
def index():
    """Serve the main web UI."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_message():
    """Predict spam/ham for a given SMS message."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Please enter a message"}), 400

    logging.info(f"Classifying message: {message[:50]}...")
    result = predict(message)
    return jsonify(result)


@app.route("/stats")
def model_stats():
    """Return model performance metrics."""
    return jsonify(get_stats())


if __name__ == "__main__":
    # Configure host, port, and debug dynamically from environment variables
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "true").lower() in ("true", "1", "yes")
    
    if os.environ.get("FLASK_ENV") == "production":
        debug = False
        host = "0.0.0.0"

    logging.info(f"Starting server on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)

