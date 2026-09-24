from sqlalchemy import text
import pandas as pd
import joblib
from db import engine
from ml.recommendations import build_recommendation_model

query = text("""
    SELECT
        parent_asin,
        title,
        main_category
    FROM products
    WHERE title IS NOT NULL
""")

with engine.connect() as connection:
    products = pd.read_sql(query, connection)

print(f'Loaded {len(products)} products')

model = build_recommendation_model(products)

print('Recommendation model built successfully')
print('Saved to models/recommendation_model.joblib')