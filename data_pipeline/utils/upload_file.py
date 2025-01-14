import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from io import BytesIO
from minio import Minio

load_dotenv()

def upload_file_to_minio():
    # Connect to PostgresQL server
    conn = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"), 
        port=os.getenv("POSTGRES_PORT"), 
        user=os.getenv("POSTGRES_USER"), 
        password=os.getenv("POSTGRES_PASSWORD")
    )
    
    # Connect to Minio storage
    minio_client = Minio(
        endpoint=os.getenv("ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False  # Set to True if using HTTPS
    )
    
    # Query data from database and prepare csv file
    query = 'SELECT * FROM "Loan"'
    df = pd.read_sql(query, conn)
    conn.close()
    
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    bucket_name = os.getenv("BUCKET_NAME")
    object_name = os.getenv("OBJECT_NAME")

    # Ensure the bucket exists
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # Upload the CSV file
    minio_client.put_object(
        bucket_name,
        object_name,
        data=csv_buffer,
        length=csv_buffer.getbuffer().nbytes,
        content_type='application/csv'
    )

    print(f"File '{object_name}' uploaded successfully to bucket '{bucket_name}'.")

if __name__ == "__main__":
    upload_file_to_minio()