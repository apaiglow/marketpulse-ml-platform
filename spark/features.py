from pyspark.sql import SparkSession
from clean import df_review_clean, df_meta_clean
from pyspark.sql.functions import col, length, max, dayofmonth, month, year

spark = SparkSession.builder.appName('MarketPulse Features').master(['local[*]']).getOrCreate()

df_features = df_review_clean.withColumn('review_length', length(col('text')))
df_features.select('text', 'review_length').show(10, truncate = False)

df_features = df_features.withColumn('rating_numeric', col('rating').cast('double'))

max_helpful_vote = df_features.select(max('helpful_vote')).collect()[0][0]
df_features = df_features.withColumn('helpful_vote_normalized', col('helpful_vote') / max_helpful_vote)
df_features.select('helpful_vote', 'helpful_vote_normalized').show(10)

df_features = df_features.withColumn('review_year', year(col('review_timestamp')))
df_features = df_features.withColumn('review_month', month(col('review_timestamp')))
df_features = df_features.withColumn('review_day', dayofmonth(col('review_timestamp')))
df_features.select('review_timestamp', 'review_year', 'review_month', 'review_day').show(10)

df_features.write.mode('overwrite').parquet('data/processed/reviews_processed.parquet')
df_meta_clean.write.mode('overwrite').parquet('data/processed/products.parquet')

# Checking that Spark can read the parquets
reviews_check = spark.read.parquet('data/processed/reviews_processed.parquet')
products_check = spark.read.parquet('data/processed/products.parquet')
print('Processed review count : ', reviews_check.count())
print('Processed product count : ', products_check.count())

reviews_check.printSchema()
products_check.printSchema()
