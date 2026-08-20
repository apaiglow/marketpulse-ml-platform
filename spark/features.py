from clean import df_review_clean
from pyspark.sql.functions import col, length

df_features = df_review_clean.withColumn('review_length', length(col('text')))
df_features.select('text', 'review_length').show(10, truncate = False)
