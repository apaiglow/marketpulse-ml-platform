from pathlib import Path
import joblib

MODEL_PATH = (Path(__file__).resolve().parents[1] / 'models' / 'sentiment_model.joblib')

def test_sentiment_model_loads():
    model = joblib.load(MODEL_PATH)
    prediction = model.predict(['This product is excellent and I love it.'])
    assert prediction[0] in [0, 1]