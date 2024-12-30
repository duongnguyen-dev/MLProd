# Loan approval classification 

This folder stores all notebooks for this classification problem, including: EDA, Feature Engineering, Training and Evaluation.

**Feature Engineering / Feature Extraction / Data preparation:**
- There are many feature engineering experiments that will be made on the data
    - **feature_engineering_1.ipynb** will cover the following:
        - *Stratifed sampling* to split data 
        - *Log transformation* to handle outliers

**Feature Scaling:**
- When the data is normally distributed, then we would use the mean because it captures the central tendancy. Also we would use Standardization or (Z-score scaling)
- When the data is skewed, the median is more robust because it is less sensitive to extreme values. In this case we would use Robust Scaling (Subtracting the median and dividing by the interquartile range (IQR) is a common approach.)

**Training**
- **training_experiment_1.ipynb**: We used Linear Support Vector Machine in this notebook and trained on data that was prepared in **feature_engineering_1.ipynb**