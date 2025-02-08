import findspark

from loguru import logger
from pyspark.sql import SparkSession
from processing.batch.base import BaseBatchProcessing
from processing.utils import get_env_variable
from processing.batch.loan_approval_classification.transforms.utils import *
# from processing.batch.loan_approval_classification.transforms.splitting import stratified_splitting
from processing.batch.loan_approval_classification.transforms.scaling import robust_scaling
from processing.batch.loan_approval_classification.transforms.outliers import log_transformation
from processing.batch.loan_approval_classification.transforms.categorical_data import * 
from processing.batch.loan_approval_classification.transforms.categorical_data import *
# from processing.batch.loan_approval_classification.transforms.correlation import *

findspark.init()
findspark.find()

class LoanApprovalETL(BaseBatchProcessing):
    def __init__(self):
        self.__host = get_env_variable("SILVER_HOST")
        self.__port = get_env_variable("SILVER_PORT")
        self.__db = get_env_variable("SILVER_DB")
        self.__username = get_env_variable("SILVER_USERNAME")
        self.__password = get_env_variable("SILVER_PASSWORD")
        super().__init__()

    def create_spark_session(self, app_name):
        spark = SparkSession \
            .builder \
            .master("spark://spark-master:7077")\
            .appName(f"{app_name}") \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
            .getOrCreate()
        
        return spark

    def extract(self, app_name, table_name):
        try:
            spark = self.create_spark_session(app_name)
            logger.info(spark._jvm.org.apache.hadoop.util.VersionInfo.getVersion())
        except:
            logger.error("Unable to create spark session")
            return 
        # Reading the table from PostgreSQL
        df = spark.read \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{self.__host}:{self.__port}/{self.__db}") \
                .option("user", self.__username) \
                .option("dbtable", table_name) \
                .option("password", self.__password) \
                .option("driver", "org.postgresql.Driver") \
                .load()

        return df

    def transform(self, df):
        
        return 
