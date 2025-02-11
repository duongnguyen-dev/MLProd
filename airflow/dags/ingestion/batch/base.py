from pyspark.sql import SparkSession, DataFrame

class BaseBatchIngestion:
    def __init__(self):
        pass

    def create_spark_session(self, app_name: str) -> SparkSession:
        pass

    def read(self, table_name: str) -> DataFrame:
        pass
    
    def transform(self):
        pass

    def action(self):
        pass