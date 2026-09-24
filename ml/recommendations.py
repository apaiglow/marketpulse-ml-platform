from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL_PATH = (Path(__file__).resolve().parents[1] / "models" / "recommendation_model.joblib")

def build_recommendation_model(products: pd.DataFrame):

    products = products.copy()
    products["title"] = products["title"].fillna("")
    products["main_category"] = products["main_category"].fillna("")
    products["content"] = (products["title"] + " " + products["main_category"])

    vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(products["content"])

    model = {
        "products": products[
            ["parent_asin", "title", "main_category"]
        ].reset_index(drop=True),
        "tfidf_matrix": tfidf_matrix,
        "vectorizer": vectorizer
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model