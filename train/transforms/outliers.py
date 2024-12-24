from pyspark.sql.functions import log1p

def log_transformation(spark_df, target_cols: str | list):
    """Transform columns with high outlier using log transformation."""
    for col in target_cols:
        spark_df = spark_df.withColumn(col, log1p(spark_df[col]))
    return spark_df