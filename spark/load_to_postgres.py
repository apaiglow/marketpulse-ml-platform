import os
from pyspark.sql import SparkSession

POSTGRES_URL = 'jdbc:postgresql://localhost:5432/marketpulse'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = os.environ['MARKETPULSE_DB_PASSWORD']

spark = (SparkSession.builder.appName('MarketPulse PostgresSQL Loader')
         .master('local[*]').config('spark.jars.packages', 'org.postgresql:postgresql:42.7.7')
         .getOrCreate())

jdbc_properties = {
    'user' : POSTGRES_USER,
    'password' : POSTGRES_PASSWORD,
    'driver' : 'org.postgresql.Driver'
}

reviews = spark.read.parquet('data/processed/reviews_processed.parquet')
products = spark.read.parquet('data/processed/products.parquet')
product_metrics = spark.read.parquet('data/processed/product_features.parquet')
users = spark.read.parquet('data/processed/user_features.parquet')

users = users.select('user_id')
products = products.select(
    'parent_asin',
    'title',
    'main_category',
    'description',
    'price',
    'average_rating',
    'rating_number'
)
reviews = reviews.select(
    'parent_asin',
    'user_id',
    'rating',
    'text',
    'helpful_vote',
    'verified_purchase',
    'review_timestamp'
)
product_metrics = product_metrics.select(
    'parent_asin',
    'review_count',
    'average_rating',
    'rating_std',
    'positive_ratio',
    'negative_ratio',
    'average_helpful_votes',
    'review_velocity',
    'unique_user_count'
)

users.write.jdbc(
    url=POSTGRES_URL,
    table="users",
    mode="append",
    properties=jdbc_properties
)
products.write.jdbc(
    url=POSTGRES_URL,
    table="products",
    mode="append",
    properties=jdbc_properties
)
product_metrics.write.jdbc(
    url=POSTGRES_URL,
    table="product_metrics",
    mode="append",
    properties=jdbc_properties
)
reviews.write.jdbc(
    url=POSTGRES_URL,
    table="reviews",
    mode="append",
    properties=jdbc_properties
)