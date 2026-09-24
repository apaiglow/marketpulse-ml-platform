from fastapi import FastAPI
from api.routes.products import router as products_router
from api.routes.sentiment import router as sentiment_router
from api.routes.recommendations import router as recommendations_router
from api.routes.anomalies import router as anomalies_router

app = FastAPI(
    title = 'MarketPulse API',
    description = 'API for E-Commerce Intelligence and ML',
    version = '1.0.0'
)

app.include_router(products_router)
app.include_router(sentiment_router)
app.include_router(recommendations_router)
app.include_router(anomalies_router)

@app.get('/health')
def health_check():
    return {'status' : 'healthy'}