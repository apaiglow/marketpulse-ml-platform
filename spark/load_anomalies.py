import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

POSTGRES_URL = "jdbc:postgresql://localhost:5432/marketpulse"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = os.environ["MARKETPULSE_DB_PASSWORD"]

spark = (
    SparkSession.builder
    .appName("MarketPulse Anomaly Loader")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.postgresql:postgresql:42.7.7"
    )
    .getOrCreate()
)

jdbc_properties = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver"
}

anomalies = spark.read.parquet(
    "data/processed/product_anomalies.parquet"
)

anomalies = anomalies.select(
    "parent_asin",
    col("anomaly").alias("anomaly_prediction")
)

anomalies = anomalies.coalesce(1)

anomalies.write.jdbc(
    url=POSTGRES_URL,
    table="anomalies",
    mode="append",
    properties=jdbc_properties
)

print(f"Loaded {anomalies.count()} anomaly records")

spark.stop()