import pandas as pd

from loguru import logger
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType
from trino.dbapi import connect
from processing.batch.base import BaseBatchProcessing
from processing.utils import get_env_variable
from processing.batch.loan_approval_classification.transforms.scaling import robust_scaling
from processing.batch.loan_approval_classification.transforms.outliers import log_transformation

load_dotenv('/opt/airflow/.env.airflow')

class LoanApprovalETL(BaseBatchProcessing):
    def __init__(self):
        super().__init__()
        self.__host = get_env_variable("TRINO_HOST")
        self.__port = get_env_variable("TRINO_PORT")
        self.__catalog = get_env_variable("TRINO_CATALOG")
        self.__user = get_env_variable("TRINO_USER")
        self.__schema = get_env_variable("TRINO_SCHEMA")

        self.__fs_host = get_env_variable("FS_HOST")
        self.__fs_port = get_env_variable("FS_PORT")
        self.__fs_db = get_env_variable("FS_DB")
        self.__fs_user = get_env_variable("FS_USER")
        self.__fs_password = get_env_variable("FS_PASSWORD")

    def create_trino_connection(self):
        conn = connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            catalog=self.__catalog,
            schema=self.__schema
        )
        
        return conn
    
    def create_spark_session(self, app_name):
        spark = SparkSession \
            .builder \
            .master("spark://spark-master:7077")\
            .appName(f"{app_name}") \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
            .getOrCreate()
        return spark

    def extract(self, conn, spark, table_name):
        # Create a cursor object
        cur = conn.cursor()

        # Execute a SQL query
        cur.execute(f'SELECT * FROM {table_name}')

        # Fetch and print the results
        rows = cur.fetchall()

        header = rows[0]
        data = rows[1:]

        schema = StructType([
            StructField(header[1], DoubleType(), True),
            StructField(header[2], StringType(), True),
            StructField(header[3], StringType(), True),
            StructField(header[4], DoubleType(), True),
            StructField(header[5], IntegerType(), True),
            StructField(header[6], StringType(), True),
            StructField(header[7], DoubleType(), True),
            StructField(header[8], StringType(), True),
            StructField(header[9], DoubleType(), True),
            StructField(header[10], DoubleType(), True),
            StructField(header[11], DoubleType(), True),
            StructField(header[12], IntegerType(), True),
            StructField(header[13], StringType(), True),
            StructField(header[14], IntegerType(), True)
        ])   

        converted_data = [
            (
                float(row[1]),
                row[2],
                row[3],
                float(row[4]),
                int(row[5]),
                row[6],
                float(row[7]),
                row[8],
                float(row[9]),
                float(row[10]),
                float(row[11]),
                int(row[12]),
                row[13],
                int(row[14])
            )
            for row in data
        ]
        
        # Create DataFrame
        df = spark.createDataFrame(converted_data, schema)

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

    def execute(self, table_name):
        try:
            conn = self.create_trino_connection()
        except:
            logger.error("Unable to connect trino")
            return 

        try:
            spark = self.create_spark_session()
        except:
            logger.error("Unable to create spark session")
            return 
        
        df = self.extract(conn, spark, table_name)    
        df = self.transform(df)
        df = self.load(df)