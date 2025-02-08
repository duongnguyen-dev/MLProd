from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from ingestion.batch.postgres_to_minio.postgres_to_minio import PostgresToMinio

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="batch_ingestion", 
         start_date=datetime(2025, 2, 7), 
         schedule="0 0 * * *" # Equivalent to "@daily"
        ) as dag:
    
    
    def ingest_postgres_to_minio():
        ptm = PostgresToMinio()
        ptm.read(table_name="loan", app_name="Batch ingestion from PostgreSQL to Minio")
        
    ingestion_task = PythonOperator(task_id="ingest_postgres_to_minio", python_callable=ingest_postgres_to_minio)