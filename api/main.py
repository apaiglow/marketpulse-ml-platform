from fastapi import FastAPI
from api.routes.products import router as products_router
from api.routes.sentiment import router as sentiment_router
from api.routes.recommendations import router as recommendations_router
from api.routes.anomalies import router as anomalies_router
import logging

logging.basicConfig(level = logging.INFO, format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s")

logger = logging.getLogger(__name__)

app = FastAPI(
    title = 'MarketPulse API',
    description = 'API for E-Commerce Intelligence and ML',
    version = '1.0.0'
)

@app.middleware('http')
async def log_requests(request, call_next):
    logger.info('Request : %s %s', request.method, request.url.path)
    response = await call_next(request)
    logger.info('Response : %s %s', response.status_code, request.url.path)
    return response

app.include_router(products_router)
app.include_router(sentiment_router)
app.include_router(recommendations_router)
app.include_router(anomalies_router)

@app.get('/health')
def health_check():
    return {'status' : 'healthy'}