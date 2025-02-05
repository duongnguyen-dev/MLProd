import os
import psycopg2
import pandas as pd
import json

from time import sleep
from psycopg2.extras import Json
from loguru import logger
from dotenv import load_dotenv
from postgresql_client import PostgresSQLClient

load_dotenv()

TABLE_NAME = "loan"

def insert():
    pc = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Get all columns from the devices table
    try:
        columns = pc.get_columns(table_name=TABLE_NAME)
        print(columns)
    except Exception as e:
        print(f"Failed to get schema for table with error: {e}")

    data = pd.read_csv("data/loan_data.csv")
    data = data.where(pd.notnull(data), None)  # Replace NaN with None

    for index, row in data.iterrows():
        inserted_data = (index, 
                         row["person_age"], 
                         row["person_gender"], 
                         row["person_education"], 
                         row["person_income"], 
                         row["person_emp_exp"], 
                         row["person_home_ownership"], 
                         row["loan_amnt"],
                         row["loan_intent"],
                         row["loan_int_rate"],
                         row["loan_percent_income"],
                         row["cb_person_cred_hist_length"],
                         row["credit_score"],
                         row["previous_loan_defaults_on_file"],
                         row["loan_status"]
                        )
        print(inserted_data)
        pc.execute_query(f"""
            insert into {TABLE_NAME} ({",".join(columns)})
            values {inserted_data}
        """)
        logger.info(f"A new record has been inserted successfully!")

if __name__ == "__main__":
    insert()