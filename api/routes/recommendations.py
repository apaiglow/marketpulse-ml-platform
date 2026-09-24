from pathlib import Path

import joblib
from fastapi import APIRouter, HTTPException, Query
from sklearn.metrics.pairwise import cosine_similarity


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


MODEL_PATH = (Path(__file__).resolve().parents[2] / "models" / "recommendation_model.joblib")

model = joblib.load(MODEL_PATH)

products = model["products"]
tfidf_matrix = model["tfidf_matrix"]

@router.get("/{product_id}")
def get_recommendations(product_id: str, limit: int = Query(default=5, ge=1, le=20)):
    matches = products.index[products["parent_asin"] == product_id].tolist()

    if not matches:
        raise HTTPException(status_code=404, detail="Product not found!")

    product_index = matches[0]

    similarities = cosine_similarity(tfidf_matrix[product_index], tfidf_matrix).flatten()
    similar_indices = similarities.argsort()[::-1]

    recommendations = []

    for index in similar_indices:
        if index == product_index:
            continue

        recommendations.append({
            "parent_asin": products.iloc[index]["parent_asin"],
            "title": products.iloc[index]["title"],
            "main_category": products.iloc[index]["main_category"],
            "similarity_score": float(similarities[index])
        })

        if len(recommendations) == limit:
            break

    return {
        "product_id": product_id,
        "recommendations": recommendations
    }