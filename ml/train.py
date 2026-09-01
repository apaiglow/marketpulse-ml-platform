from pyspark.sql import SparkSession
from preprocessing import prepare_sentiment_data
from sentiment import text_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report, precision_score,
    recall_score, f1_score, confusion_matrix
    )
import joblib
from anomaly import anomaly_pipeline
import os
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn

spark = SparkSession.builder.appName('MarketPulse Sentiment Training').master('local[*]').getOrCreate()

df_reviews = spark.read.parquet('data/processed/reviews_processed.parquet')
df_sentiment = prepare_sentiment_data(df_reviews)
df_sentiment_sample = df_sentiment.sample(withReplacement = False, fraction = 0.15, seed = 42)
df_pd = df_sentiment_sample.toPandas()

X = df_pd['text']
y = df_pd['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)

mlflow.set_experiment('MarketPulse Sentiment')
with mlflow.start_run(run_name = 'sentiment_model'):
    mlflow.sklearn.autolog()
    text_pipeline.fit(X_train, y_train)
    y_pred = text_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average = "weighted")
    recall = recall_score(y_test, y_pred, average = "weighted")
    f1 = f1_score(y_test, y_pred, average = "weighted")
    confusion = confusion_matrix(y_test, y_pred)
    print("Accuracy : ", accuracy)
    print("Precision : ", precision)
    print("Recall : ", recall)
    print("F1 Score : ", f1)
    print('Confusion Matrix : ')
    print(confusion)

os.makedirs('artifacts/sentiment', exist_ok = True)
report = classification_report(y_test, y_pred)
with open('artifacts/sentiment/classification_report.txt', 'w') as file:
    file.write(report)

plt.figure(figsize = (6, 5))
plt.imshow(confusion)
plt.title('MarketPulse Sentiment Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')
plt.xticks([0, 1], ['Negative', 'Positive'])
plt.yticks([0, 1], ['Negative', 'Positive'])
for i in range(confusion.shape[0]):
    for j in range(confusion.shape[1]):
        plt.text(j, i, confusion[i, j], ha = 'center', va = 'center')
plt.tight_layout()
plt.savefig('artifacts/sentiment/confusion_matrix.png', dpi = 300)
plt.close()

df_products = spark.read.parquet('data/processed/product_features.parquet')
product_pd = df_products.toPandas()
feature_columns = ['review_count', 'average_rating', 'rating_std', 'positive_ratio', 'negative_ratio', 'average_helpful_votes', 'review_velocity', 'unique_user_count']
X_products = product_pd[feature_columns]

mlflow.set_experiment('MarketPulse Anomaly Detection')
with mlflow.start_run(run_name = 'anomaly_model'):
    mlflow.sklearn.autolog()
    
    anomaly_pipeline.fit(X_products)
    anomaly_predictions = anomaly_pipeline.predict(X_products)
    product_pd['anomaly'] = anomaly_predictions

    total_products =  len(product_pd)
    total_anomalies = (product_pd['anomaly'] == -1).sum()
    anomaly_rate = total_anomalies / total_products
    anomalies = product_pd[product_pd['anomaly'] == -1]

    print('\nAnomaly Detection Results')
    print('Total Products : ', total_products)
    print('Total Anomalies : ', total_anomalies)
    print('Anomaly Rate : ', anomaly_rate)
    print('\nSample Anomalies : ')
    print(anomalies[['parent_asin'] + feature_columns].head(5))

df_anomaly = spark.createDataFrame(product_pd)
df_anomaly.write.mode('overwrite').parquet('data/processed/product_anomalies.parquet')

os.makedirs('models', exist_ok = True)
joblib.dump(text_pipeline, 'models/sentiment_model.joblib')
joblib.dump(anomaly_pipeline, 'models/anomaly_model.joblib')

print(product_pd['anomaly'].value_counts())