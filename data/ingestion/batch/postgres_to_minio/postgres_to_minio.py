from pyspark.sql import SparkSession
from dotenv import load_dotenv
from data.ingestion.batch.base import BaseBatchIngestion
from data.ingestion.utils import get_env_variable
from loguru import logger

load_dotenv()

class PostgresToMinio(BaseBatchIngestion):
    def __init__(self):
        super().__init__()
        self.__endpoint = get_env_variable("MINIO_ENDPOINT")
        self.__minio_access_key = get_env_variable("MINIO_ACCESS_KEY")
        self.__minio_secret_key = get_env_variable("MINIO_SECRET_KEY")
        self.__bucket = get_env_variable("MINIO_BUCKET")
        self.__object = get_env_variable("MINIO_OBJECT")

        self.__host = get_env_variable("POSTGRES_HOST")
        self.__port = get_env_variable("POSTGRES_PORT")
        self.__user_name = get_env_variable("POSTGRES_USER")
        self.__password = get_env_variable("POSTGRES_PASSWORD")
        self.__db_name = get_env_variable("POSTGRES_DB")
    
    def create_spark_session(self, app_name):
        # Create a Spark session with specific configurations for PostgreSQL and Minio

        # Remember to set org.apache.hadoop:hadoop-aws:<version> in spark.jars.packages and the <version> should match
        # the hadoop version in spark container. Reference from this blog: https://davidlindelof.com/reading-s3-data-from-a-local-pyspark-session/

        spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.hadoop.fs.s3a.endpoint", f"{self.__endpoint}") \
            .config("spark.hadoop.fs.s3a.access.key", self.__minio_access_key) \
            .config("spark.hadoop.fs.s3a.secret.key", self.__minio_secret_key) \
            .config("spark.hadoop.fs.s3a.path.style.access", True) \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
            .config("hive.metastore.uris", "thrift://metastore:9083") \
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-core_2.12:2.4.0,org.postgresql:postgresql:42.6.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .getOrCreate()
        
        return spark
    
    def read(self, table_name, app_name):
        try:
            spark = self.create_spark_session(app_name)
            logger.info(spark._jvm.org.apache.hadoop.util.VersionInfo.getVersion())
        except:
            logger.error("Unable to create spark session")
            return 
        # Reading the table from PostgreSQL
        df = spark.read \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{self.__host}:{self.__port}/{self.__db_name}") \
                .option("user", self.__user_name) \
                .option("dbtable", table_name) \
                .option("password", self.__password) \
                .option("driver", "org.postgresql.Driver") \
                .load()
        
        # Write Data to MinIO in CSV format
        try:
            df.write \
                .mode("overwrite") \
                .option("header", "true") \
                .csv(f"s3a://{self.__bucket}/{self.__object}.csv")
            logger.info(f"File '{self.__object}' uploaded successfully to bucket '{self.__bucket}'.")
        except:
            logger.error("Cannot ingest data from Postgres to Minio")
        
if __name__ == "__main__":
    ptm = PostgresToMinio()
    ptm.read(table_name="loan", app_name="Batch ingestion from PostgreSQL to Minio")