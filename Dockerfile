# ==========================================================
# STAGE 1 — Base image with Python
# ==========================================================
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ==========================================================
# STAGE 2 — Install Python dependencies
# ==========================================================
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================================
# STAGE 3 — Copy application code
# ==========================================================
COPY . /app/

# Download spaCy model at build time
RUN python -m spacy download en_core_web_sm

# Expose port
EXPOSE 8000

# ==========================================================
# STAGE 4 — Start Gunicorn + Uvicorn Workers
# ==========================================================
CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120"]
