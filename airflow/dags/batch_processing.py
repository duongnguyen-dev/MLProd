from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from processing.batch.loan_approval_classification.loan_etl import LoanApprovalETL

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="loan_etl", 
         start_date=datetime(2025, 2, 7), 
         schedule="0 0 * * *" # Equivalent to "@daily"
        ) as dag:
    
    
    def etl_dwh_to_feature_store():
        etl = LoanApprovalETL()
        etl.execute(table_name="loan")
        
    processing_task = PythonOperator(task_id="dwh_to_feature_store", python_callable=etl_dwh_to_feature_store)