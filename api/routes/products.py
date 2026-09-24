from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from api.dependencies import get_db

router = APIRouter(prefix = '/products', tags = ['Products'])

@router.get('/{product_id}')
def get_product(product_id : str, db : Session = Depends(get_db)):
    query = text("""
    SELECT parent_asin, title, main_category, average_rating, rating_number, price
    FROM products
    WHERE parent_asin = :product_id
    """)

    result = db.execute(query, {'product_id' : product_id}).mappings().first()

    if result is None:
        raise HTTPException(status_code = 404, detail = 'Product not found!')

    return dict(result)

@router.get('/{product_id}/analytics')
def get_product_analytics(product_id : str, db : Session = Depends(get_db)):
    query = text("""
    SELECT
        parent_asin,
        review_count,
        average_rating,
        rating_std,
        positive_ratio,
        negative_ratio,
        average_helpful_votes,
        review_velocity,
        unique_user_count
    FROM product_metrics
    WHERE parent_asin = :product_id
    """)

    result = db.execute(query, {'product_id' : product_id}).mappings().first()

    if result is None:
        raise HTTPException(status_code = 404, detail = 'Product analytics not found!')

    return dict(result)