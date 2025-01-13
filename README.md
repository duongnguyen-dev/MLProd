# End-to-end Machine Learning system

# Table of contents
1. [Data pipeline]()
   1. [Overall data architecture]()
   2. [Approach and concepts]()
       1. [Data source]()
       2. [Lake house]()
       3. [Change Data Capture]()
       4. [Stream and Batch processing]()
       5. [Feature Store]()
       6. [Data orchestration]()
   3. [Technology]()
       1. [Source (Loan Approval dataset)]()
       2. [Ingestion (CDC, Batch ingestion)]()
       3. [Storage (Minio on k8s)]()
       4. [Batch processing (PySpark)]()
       5. [Stream processing (Flink)]()
       6. [Orchestration (Airflow)]()
       7. [Feature store (Feast)]()
       8. [Infras (Terraform, Helm)]()
2. Training pipeline
3. Serving pipeline

## 1. Data pipeline

## Installation and Usage for training purpose only:
- **Step 1**: Install and create conda environment
    - Required Python >= 3.10
    - For **Windows**: Strictly follow this repo https://github.com/conda-forge/miniforge
    - For MacOS, run the following command:
        ```bash
        brew install miniforge
        ```
    - Then:
        ```bash
        conda create -n <REPLACE_THIS_WITH_YOUR_DESIRED_NAME> python==3.12
        conda activate 
        ```
- **Step 2**: Install prerequisite packages
    ```
    pip install -e .
    ```
