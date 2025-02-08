from pyspark.ml.feature import RobustScaler
from pyspark.ml import Pipeline

def robust_scaling(spark_df, target_cols):
    for col in target_cols:
        median = spark_df.approxQuantile(col, [0.5], 0.05)[0]
        q1 = spark_df.approxQuantile(col, [0.25], 0.05)[0]
        q3 = spark_df.approxQuantile(col, [0.75], 0.05)[0]
        iqr = q3 - q1

        spark_df = spark_df.withColumn(col, (spark_df[col] - median) / iqr)

    return spark_df