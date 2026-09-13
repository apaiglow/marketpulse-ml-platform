from pathlib import Path
import joblib
from fastapi import APIRouter
from api.schemas import SentimentRequest

router = APIRouter(prefix = '/sentiment', tags = ['Sentiment'])

MODEL_PATH = Path(__file__).resolve().parents[2] / 'models' / 'sentiment_model.joblib'
model = joblib.load(MODEL_PATH)

@router.post("")
def predict_sentiment(request : SentimentRequest):
    prediction = model.predict([request.text])[0]
    sentiment = 'positive' if prediction == 1 else 'negative'
    return {
        'text' : request.text,
        'sentiment' : sentiment,
        'label' : int(prediction)
    }