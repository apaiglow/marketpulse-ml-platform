from pyspark.sql import SparkSession
from clean import df_review_clean, df_meta_clean
from pyspark.sql.functions import col, length, dayofmonth, month, year, count, avg, stddev, sum, when, countDistinct, min, max
from pyspark.sql.functions import datediff, weekofyear

spark = SparkSession.builder.appName('MarketPulse Features').master('local[*]').getOrCreate()

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

product_features = df_features.groupBy('parent_asin').agg(count('*').alias('review_count'),
                                                          avg('rating').alias('average_rating'),
                                                          stddev('rating').alias('rating_std'),
                                                          (sum(when(col('rating') >= 3.5, 1).otherwise(0)) / count('*')).alias('positive_ratio'),
                                                          (1 - (sum(when(col('rating') >= 3.5, 1).otherwise(0)) / count('*'))).alias('negative_ratio'),
                                                          avg('helpful_vote').alias('average_helpful_votes'),
                                                          countDistinct('user_id').alias('unique_user_count'),
                                                          min('review_timestamp').alias('first_review'),
                                                          max('review_timestamp').alias('last_review'))

product_features = product_features.withColumn('active_days', datediff(col('last_review'), col('first_review')))
product_features = product_features.withColumn('review_velocity', when(col('active_days') > 0, col('review_count')/col('active_days')).otherwise(col('review_count')))
product_features = product_features.drop('first_review', 'last_review', 'active_days')

user_features = df_features.groupBy('user_id').agg(
    count('*').alias('user_review_count'),
    avg('rating').alias('user_average_rating'),
    stddev('rating').alias('user_rating_std')
)

daily_reviews = df_features.groupBy('review_year', 'review_month', 'review_day').agg(
    count('*').alias('reviews_per_day')
)
df_features = df_features.join(daily_reviews, on = ['review_year', 'review_month', 'review_day'], how = 'left')
df_features = df_features.withColumn('review_week', weekofyear(col('review_timestamp')))
weekly_reviews = df_features.groupBy('review_year', 'review_week').agg(
    count('*').alias('reviews_per_week')
)
df_features = df_features.join(weekly_reviews, on = ['review_year', 'review_week'], how = 'left')
monthly_reviews = df_features.groupBy("review_year", "review_month").agg(
    count("*").alias("reviews_per_month")
)
df_features = df_features.join(monthly_reviews, on = ['review_year', 'review_month'], how = 'left')

df_features.write.mode('overwrite').parquet('data/processed/reviews_processed.parquet')
df_meta_clean.write.mode('overwrite').parquet('data/processed/products.parquet')
product_features.write.mode('overwrite').parquet('data/processed/product_features.parquet')
user_features.write.mode('overwrite').parquet('data/processed/user_features.parquet')

# Checking that Spark can read the parquets
reviews_check = spark.read.parquet('data/processed/reviews_processed.parquet')
products_check = spark.read.parquet('data/processed/products.parquet')
user_check = spark.read.parquet('data/processed/user_features.parquet')
print('Processed review count : ', reviews_check.count())
print('Processed product count : ', products_check.count())
print('User features count : ', user_check.count())

reviews_check.printSchema()
products_check.printSchema()
user_check.printSchema()
