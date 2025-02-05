import os

from dotenv import load_dotenv
from postgresql_client import PostgresSQLClient

load_dotenv()


def main():
    pc = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Create devices table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS loan (
            id INT PRIMARY KEY,
            person_age FLOAT,
            person_gender VARCHAR(30),
            person_education VARCHAR(30),
            person_income FLOAT,
            person_emp_exp INT,
            person_home_ownership VARCHAR(30),
            loan_amnt FLOAT,
            loan_intent VARCHAR(30),
            loan_int_rate FLOAT,
            loan_percent_income FLOAT,
            cb_person_cred_hist_length FLOAT,
            credit_score INT,
            previous_loan_defaults_on_file VARCHAR(30),
            loan_status INT
        );
    """
    try:
        pc.execute_query(create_table_query)
    except Exception as e:
        print(f"Failed to create table with error: {e}")


if __name__ == "__main__":
    main()
