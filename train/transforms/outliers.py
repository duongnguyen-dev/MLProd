from pyspark.sql.functions import log1p

def log_transformation(spark_df):
    """Transform columns with high outlier using log transformation."""
    for col in spark_df.columns:
        spark_df = spark_df.withColumn(col, log1p(spark_df[col]))