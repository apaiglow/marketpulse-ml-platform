FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p models

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L \
    -o models/sentiment_model.joblib \
    "https://github.com/apaiglow/marketpulse-ml-platform/releases/download/model-assets-v1/sentiment_model.joblib"

RUN curl -L \
    -o models/recommendation_model.joblib \
    "https://github.com/apaiglow/marketpulse-ml-platform/releases/download/model-assets-v1/recommendation_model.joblib"

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]