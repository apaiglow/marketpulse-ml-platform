from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200

def test_sentiment():
    response = client.post('/sentiment', json = {'text' : 'This product is excellent.'})
    assert response.status_code == 200
    data = response.json()
    assert data['sentiment'] in ['positive', 'negative']
    assert data['label'] in [0, 1]

def test_sentiment_validation():
    response = client.post('/sentiment', json = {})
    assert response.status_code == 422