-- CreateTable
CREATE TABLE "Loan" (
    "person_age" SERIAL NOT NULL,
    "person_gender" TEXT NOT NULL,
    "person_education" TEXT NOT NULL,
    "person_income" INTEGER NOT NULL,
    "person_emp_exp" INTEGER NOT NULL,
    "person_home_ownership" TEXT NOT NULL,
    "loan_amnt" INTEGER NOT NULL,
    "loan_intent" TEXT NOT NULL,
    "loan_int_rate" DOUBLE PRECISION NOT NULL,
    "loan_percent_income" DOUBLE PRECISION NOT NULL,
    "cb_person_cred_hist_length" INTEGER NOT NULL,
    "credit_score" INTEGER NOT NULL,
    "previous_loan_defaults_on_file" BOOLEAN NOT NULL,
    "loan_status" INTEGER NOT NULL,

    CONSTRAINT "Loan_pkey" PRIMARY KEY ("person_age")
);
