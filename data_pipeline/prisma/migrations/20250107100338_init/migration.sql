/*
  Warnings:

  - The primary key for the `Loan` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "Loan" DROP CONSTRAINT "Loan_pkey",
ADD COLUMN     "id" SERIAL NOT NULL,
ALTER COLUMN "person_age" DROP DEFAULT,
ADD CONSTRAINT "Loan_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "Loan_person_age_seq";
