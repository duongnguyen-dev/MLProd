# End-to-end Machine Learning system

## Overall architecture

## Table of contents
1. Data pipeline
    1. Data source
    2. ETL
    3. Feature store
2. Training pipeline
3. Serving pipeline

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
