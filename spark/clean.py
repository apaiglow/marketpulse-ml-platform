from ingest import df_review, df_meta
from pyspark.sql.functions import col, from_unixtime

df_review = df_review.withColumn(
    'review_timestamp',
    from_unixtime(col('timestamp') / 1000).cast('timestamp')
)

df_review.select('timestamp', 'review_timestamp').show(10, truncate = False)

review_columns = ['asin', 'helpful_vote', 'images', 'parent_asin', 'rating',
                  'text', 'timestamp', 'title', 'user_id', 'verified_purchase']

for column in review_columns:
    null_count = df_review.filter(col(column).isNull()).count()
    print(f'{column} : {null_count} nulls')

# Data analysing

print('Invalid ratings : \n')
df_review.filter((col('rating') < 0) | (col('rating') > 5)).show()

print('Negative helpful votes : ')
df_review.filter(col('helpful_vote') < 0).show()

print('Sample price values : ')
df_meta.select('price').distinct().show(30, truncate = False)

metadata_columns = ['parent_asin', 'title', 'main_category', 'categories', 'features',
                    'description', 'average_rating', 'rating_number', 'price', 'store']

for column in metadata_columns:
    val_absent = df_meta.filter(col(column).isNull()).count()
    val_present = df_meta.filter(col(column).isNotNull()).count()
    print(f'Null {column} : {val_absent}')
    print(f'Non Null {column} : {val_present}')

# Data Engineering

df_meta = df_meta.withColumn('price', col('price').cast('double'))
print('Non null prices after conversion : ', df_meta.filter(col('price').isNotNull()).count())

df_review_clean = df_review.select('asin', 'parent_asin', 'user_id', 'rating', 'helpful_vote',
                                   'title', 'text', 'timestamp', 'review_timestamp', 'verified_purchase')
df_meta_clean = df_meta.select('parent_asin', 'title', 'main_category', 'categories', 'features', 'description',
                               'average_rating', 'rating_number', 'price', 'store')

