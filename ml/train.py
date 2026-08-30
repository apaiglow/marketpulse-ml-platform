from pyspark.sql import SparkSession
from preprocessing import prepare_sentiment_data
from sentiment import text_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from anomaly import anomaly_pipeline

spark = SparkSession.builder.appName('MarketPulse Sentiment Training').master('local[*]').getOrCreate()

df_reviews = spark.read.parquet('data/processed/reviews_processed.parquet')
df_sentiment = prepare_sentiment_data(df_reviews)
df_sentiment_sample = df_sentiment.sample(withReplacement = False, fraction = 0.15, seed = 42)
df_pd = df_sentiment_sample.toPandas()

X = df_pd['text']
y = df_pd['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)
text_pipeline.fit(X_train, y_train)
y_pred = text_pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print('Accuracy : ', accuracy)
print('\nClassification Report : ')
print(classification_report(y_test, y_pred))

df_products = spark.read.parquet('data/processed/product_features.parquet')
product_pd = df_products.toPandas()
feature_columns = ['review_count', 'average_rating', 'rating_std', 'positive_ratio', 'negative_ratio', 'average_helpful_votes', 'review_velocity', 'unique_user_count']
X_products = product_pd[feature_columns]
anomaly_pipeline.fit(X_products)
anomaly_predictions = anomaly_pipeline.predict(X_products)
product_pd['anomaly'] = anomaly_predictions

df_anomaly = spark.createDataFrame(product_pd)
df_anomaly.write.mode('overwrite').parquet('data/processed/product_anomalies.parquet')

joblib.dump(text_pipeline, 'models/sentiment_pipeline.joblib')
joblib.dump(anomaly_pipeline, 'models/anomaly_pipeline.joblib')

print(product_pd['anomaly'].value_counts())