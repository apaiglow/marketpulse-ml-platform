from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import normalize_text
from sklearn.linear_model import LogisticRegression


text_pipeline = Pipeline([
    ('normalize', FunctionTransformer(normalize_text)),
    ('tfidf', TfidfVectorizer(max_features=10000)),
    ('model', LogisticRegression(max_iter = 1000))
])