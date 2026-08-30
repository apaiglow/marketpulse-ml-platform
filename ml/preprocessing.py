import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def prepare_sentiment_data(df):

    df = df.select('text', 'rating')
    df = df.dropna(subset = ['text', 'rating'])
    df = df.withColumn('sentiment', (df['rating'] >= 3.5).cast('int'))
    return df.select('text', 'sentiment')

def normalize_text(text):
    return text.str.lower()