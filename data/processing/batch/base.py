from pyspark.sql import SparkSession

class BaseBatchProcessing:
    def __init__(self):
        pass

    def create_spark_session(self, app_name: str) -> SparkSession:
        pass

    def extract(self):
        pass

    def transform(self):
        pass

    def load(self):
        pass