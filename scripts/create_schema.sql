---Create a new schema to store tables
CREATE SCHEMA IF NOT exists mle.my_bucket
WITH (location = 's3://my-bucket/');