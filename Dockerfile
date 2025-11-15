FROM python:3.10-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# spaCy model (redundant but safe)
RUN python -m spacy download en_core_web_sm

# Copy application files
COPY . .

# Cloud Run expects service on $PORT
ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
