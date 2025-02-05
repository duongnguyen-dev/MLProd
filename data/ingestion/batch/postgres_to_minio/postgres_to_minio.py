from pyspark.sql import SparkSession
from dotenv import load_dotenv
from data.ingestion.batch.base import BaseBatchIngestion
from data.ingestion.utils import get_env_variable

load_dotenv()

class PostgresToMinio(BaseBatchIngestion):
    def __init__(self):
        super().__init__()
        self.__host_address = get_env_variable("MINIO_HOST_ADDRESS")
        self.__port = get_env_variable("POSTGRES_PORT")
        self.__minio_access_key = get_env_variable("MINIO_ACCESS_KEY")
        self.__minio_secret_key = get_env_variable("MINIO_SECRET_KEY")
        self.__user_name = get_env_variable("POSTGRES_USER")
        self.__password = get_env_variable("POSTGRES_PASSWORD")
        self.__db_name = get_env_variable("POSTGRES_DB")
    
    def create_spark_session(self, app_name):
        # Create a Spark session with specific configurations for PostgreSQL and Minio
        spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.hadoop.fs.s3a.endpoint", f"http://{self.__host_address}:9000") \
            .config("spark.hadoop.fs.s3a.access.key", self.__minio_access_key) \
            .config("spark.hadoop.fs.s3a.secret.key", self.__minio_secret_key) \
            .config("spark.hadoop.fs.s3a.path.style.access", True) \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
            .config("hive.metastore.uris", "thrift://metastore:9083") \
            .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0,org.postgresql:postgresql:42.6.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .getOrCreate()
        
        return spark
    
    def read(self, table_name, app_name):
        spark = self.create_spark_session(app_name)
        # Reading the table from PostgreSQL
        df = spark.read \
                .format("jdbc") \
                .option("url", f"jdbc:postgresql://{self.__host_address}:{self.__port}/{self.__db_name}") \
                .option("user", self.__user_name) \
                .option("dbtable", table_name) \
                .option("password", self.__password) \
                .option("driver", "org.postgresql.Driver") \
                .load()
        print(df)
    
if __name__ == "__main__":
    ptm = PostgresToMinio()
    ptm.read(table_name="loan", app_name="Batch ingestion from PostgreSQL to Minio")