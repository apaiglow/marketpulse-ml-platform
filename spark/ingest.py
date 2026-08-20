from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    DoubleType,
    BooleanType,
    ArrayType
)

review_schema = StructType([
    StructField("asin", StringType(), True),
    StructField("helpful_vote", LongType(), True),
    StructField("images", ArrayType(StringType()), True),
    StructField("parent_asin", StringType(), True),
    StructField("rating", DoubleType(), True),
    StructField("text", StringType(), True),
    StructField("timestamp", LongType(), True),
    StructField("title", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("verified_purchase", BooleanType(), True)
])

metadata_schema = StructType([
    StructField("parent_asin", StringType(), True),
    StructField("title", StringType(), True),
    StructField("main_category", StringType(), True),
    StructField("categories", ArrayType(StringType()), True),
    StructField("features", ArrayType(StringType()), True),
    StructField("description", ArrayType(StringType()), True),
    StructField("average_rating", DoubleType(), True),
    StructField("rating_number", LongType(), True),
    StructField("price", StringType(), True),
    StructField("store", StringType(), True)
])

spark = SparkSession.builder \
    .appName("MarketPulse") \
    .master("local[*]") \
    .getOrCreate()

df_review = spark.read.schema(review_schema).json('data/raw/reviews/All_Beauty.jsonl.gz')
df_meta = spark.read.schema(metadata_schema).json('data/raw/metadata/meta_All_Beauty.jsonl.gz')

print("\nReview Schema")
df_review.printSchema()
print("\nMetadata Schema")
df_meta.printSchema()

print("Total number of reviews : ", df_review.count())
print("Total number of metadata records : ", df_meta.count())

print("Review Columns : ", df_review.columns)
print("Metadata Columns : ", df_meta.columns)

# spark.stop()