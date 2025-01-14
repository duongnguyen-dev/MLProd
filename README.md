# End-to-end Machine Learning system in production

# Table of contents
1. [Data pipeline](#1-data-pipeline)
   1. [Overall data architecture](#11-overall-data-architecture)
   2. [Approach and concepts](#12-approach-and-concepts)
       1. [Data source](#121-data-source)
       2. [Data lake house architecture](#122-data-lake-house-architecture)
       3. [Stream and batch ingestion](#123-stream-and-batch-ingestion)
       4. [Stream and batch processing](#124-stream-and-batch-processing)
       5. [Pipeline orchestration](#125-pipeline-orchestration)
   3. [Technology](#13-technology)
      1. [Orchestration (Airflow)]()
      2. [Storage (Minio on k8s)]()
      3. [Ingestion (CDC, Batch ingestion)]()
      4. [Batch processing (PySpark on k8s)]()
      5. [Stream processing (Flink)]()
      6. [Feature store (Feast)]()

2. Training pipeline
3. Serving pipeline

## 1. Data pipeline
### 1.1. Overall data architecture
<p align="center">
  <img src="https://github.com/duongnguyen-dev/AutoMLFlow/blob/main/assets/data_architecture.png" />
</p>

### 1.2. Approach and concepts
#### 1.2.1. Data source
- In this repo, i will use a public data named [Loan Approval Classification Dataset](https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data) from Kaggle with 45.000 samples and 14 attributes. This datasets will be stored in PostgreSQL database.
#### 1.2.2. Data lake house architecture
- **Data Lake** can **store many types of data at low cost**, but doesn't include a query engine therefore it is not fit for analytics.
- **Data warehouse** aggregates data from various sources which is mostly structured data and stores on a relational database. Because a data warehouse stores data in a structured, relational schema, it **supports high-performance structured query language (SQL)** queries. On the other hand, because the storage and compute are tightly coupled, therefore it is very *expensive to scale*. Additionally, the data must be transformed before it is loaded into warehouse therefore the *performance (latency)* may be affected   
- This architecture merges all the benefits of Data lake and Data warehouse into it, in other words **Data lake house = Data lake + Data warehouse**. From my perspective, It includes 4 main layers:
   - Ingestion layer: This layer **gathers both batch and stream ingestion** from a data source. It **mainly utilizes ELT (Extract-Load-Transform)** where the data is loaded into the storage and transformed later when it is needed.
   - Storage layer (Like data lake): We can call this layer is **Bronze zone**. This is typically an object storage. In this repo, I will use Minio S3.
   - Metadata layer (Like data warehouse): This is **Silver zone**. It centralized all data sources and the metadata for each source into a structured and relational schema therefore we can use a high-performance structured query language.
   - Consumption layer (Like data mart): Typically this is called **Gold Zone**. In this repo, my problem is about ML therefore data mart is a **feature store**.
- Key advantages:
   - Scalable
   - Low-cost
   - Accessible
   - Quality and Reliable
Based on the advantages mentioned above, I choose **Data lakehouse** for the data pipeline. You can read more from this blog [Data warehouses vs Data lakes vs Data lake houses](https://www.ibm.com/think/topics/data-warehouse-vs-data-lake-vs-data-lakehouse)

#### 1.2.3. Stream and batch ingestion
- **Batch ingestion**: This is an ingestion model where you want to get data at a specific interval or simply say you know the starting and ending point.
- **Stream ingestion**: This ingestion model ensures that the data in your lakehouse is up to date with every change in the data source.
- **Hybrid ingestion**: Mixed both batch and stream ingestion.
In this repo, I use a **Hybrid ingestion** model to load data from data source to the lakehouse. You can read more here [Your data ingestion strategy is a key factor in data quality](https://www.ibm.com/think/insights/data-ingestion-strategy#:~:text=Generally%2C%20there%20are%20three%20modes%20of%20data%20ingestion%3A,a%20daily%2C%20weekly%2C%20monthly%20or%20other%20time-based%20schedule.) 

#### 1.2.4. Stream and batch processing
- Similar to ingestion but it is applied when transforming data between each zone in a lakehouse. Another way to call a hybrid processing model is **Lambda architecture**

#### 1.2.5. Pipeline orchestration
- The need for pipeline orchestration:
   - It ensures all the steps run in the desired order.
   - Dependencies between each step are manageable.
- When there is no orchestration:
   - A small change in the upstream/downstream can cause the whole system to break.
   - Cronjob is hard to set up, maintain, and debug.

### 1.3. Technology


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
