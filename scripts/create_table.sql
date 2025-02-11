---Create a new table in the newly created schema
CREATE TABLE IF NOT EXISTS mle.my_bucket.loan (
    id VARCHAR,
    person_age VARCHAR,
    person_gender VARCHAR,
    person_education VARCHAR,
    person_income VARCHAR,
    person_emp_exp VARCHAR,
    person_home_ownership VARCHAR,
    loan_amnt VARCHAR,
    loan_intent VARCHAR,
    loan_int_rate VARCHAR,
    loan_percent_income VARCHAR,
    cb_person_cred_hist_length VARCHAR,
    credit_score VARCHAR,
    previous_loan_defaults_on_file VARCHAR,
    loan_status VARCHAR
) WITH (
  external_location = 's3://my-bucket/loan',
  format = 'CSV'
);