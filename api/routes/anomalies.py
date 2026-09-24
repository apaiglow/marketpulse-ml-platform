from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from api.dependencies import get_db

router = APIRouter(prefix = '/anomalies', tags = ['Anomalies'])

@router.get('/{product_id}')
def get_product_anomaly(product_id : str, db : Session = Depends(get_db)):
    query = text("""
    SELECT
        parent_asin,
        anomaly_prediction,
        anomaly_score
    FROM anomalies
    WHERE parent_asin = :product_id
    """)
    result = db.execute(query, {'product_id' : product_id}).mappings().first()
    if result is None:
        raise HTTPException(status_code = 404, detail = 'Anomaly result not found!')
    return dict(result)