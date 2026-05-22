# Stage 1: Build and Train Model
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY SMS-Spam-Classifier/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy dataset and model files
COPY SMS-Spam-Classifier/data ./data
COPY SMS-Spam-Classifier/model.py ./
COPY SMS-Spam-Classifier/train.py ./

# Train and serialize the model
RUN python train.py

# Stage 2: Final Runtime Image
FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies (including gunicorn)
COPY SMS-Spam-Classifier/requirements-prod.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and static/template files
COPY SMS-Spam-Classifier/app.py ./
COPY SMS-Spam-Classifier/model.py ./
COPY SMS-Spam-Classifier/templates ./templates
COPY SMS-Spam-Classifier/static ./static

# Copy trained model artifacts from the builder stage
COPY --from=builder /app/model.pkl ./
COPY --from=builder /app/vectorizer.pkl ./

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=5000

# Expose port
EXPOSE 5000

# Run the app with gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT app:app
