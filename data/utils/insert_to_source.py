import os
import psycopg2
import pandas as pd
import json

from psycopg2.extras import Json
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

def insert():
    conn = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"), 
        port=os.getenv("POSTGRES_PORT"), 
        user=os.getenv("POSTGRES_USER"), 
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cur = conn.cursor()
    logger.info("Successfully connect to database.")

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

        cur.execute("""
            INSERT INTO "Loan" (
                id,
                person_age,
                person_gender,
                person_education,
                person_income,
                person_emp_exp,
                person_home_ownership,
                loan_amnt,
                loan_intent,
                loan_int_rate,
                loan_percent_income,
                cb_person_cred_hist_length,
                credit_score,
                previous_loan_defaults_on_file,
                loan_status
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, inserted_data)
        logger.info(f"A new record has been inserted successfully!")
        conn.commit()
    conn.close()

if __name__ == "__main__":
    insert()