from loguru import logger
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from processing.batch.base import BaseBatchProcessing
from processing.utils import get_env_variable
from processing.batch.loan_approval_classification.transforms.scaling import robust_scaling
from processing.batch.loan_approval_classification.transforms.outliers import log_transformation

load_dotenv('/opt/airflow/.env')

class LoanApprovalETL(BaseBatchProcessing):
    def __init__(self):
        super().__init__()
        self.__host = get_env_variable("SILVER_HOST")
        self.__port = get_env_variable("SILVER_PORT")
        self.__db = get_env_variable("SILVER_DB")
        self.__username = get_env_variable("SILVER_USER")
        self.__password = get_env_variable("SILVER_PASSWORD")

        self.__fs_host = get_env_variable("FS_HOST")
        self.__fs_port = get_env_variable("FS_PORT")
        self.__fs_db = get_env_variable("FS_DB")
        self.__fs_user = get_env_variable("FS_USER")
        self.__fs_password = get_env_variable("FS_PASSWORD")

    def create_spark_session(self, app_name):
        spark = SparkSession \
            .builder \
            .master("spark://spark-master:7077")\
            .appName(f"{app_name}") \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
            .getOrCreate()
        
        return spark

    def extract(self, spark, table_name):
        # Reading the table from PostgreSQL
        df = spark.read \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{self.__host}:{self.__port}/{self.__db}") \
                .option("user", self.__username) \
                .option("password", self.__password) \
                .option("driver", "org.postgresql.Driver") \
                .option("query", "SHOW TABLES;") \
                .load()
        return df

    def transform(self, df):
        df = log_transformation(df)
        df = robust_scaling(df)
        return df

    def load(self, df):
        properties = {
            "user": self.__fs_user,
            "password": self.__fs_password,
            "driver": "org.postgresql.Driver"
        }
        df.write.jdbc(url=f"jdbc:postgresql://{self.__fs_host}:{self.__fs_port}/{self.__fs_db}", table="loan_feature", mode="overwrite", properties=properties)

    def execute(self, app_name, table_name):
        try:
            spark = self.create_spark_session(app_name)
        except:
            logger.error("Unable to create spark session")
            return 

        df = self.extract(spark, table_name)
        # df = self.transform(df)
        # df = self.load(df)