import matplotlib.pyplot as plt
import pyspark.sql.functions as F
import pyspark.sql.types as T

from pyspark.ml.linalg import Vectors

def find_categorical_cols(df):
    categorical_columns = [
        field.name for field in df.schema.fields if str(field.dataType) in ['StringType()', 'BooleanType()'] and field.name != "loan_status"
    ]
    return categorical_columns

def find_numerical_cols(df):
    numerical_columns = [
        field.name for field in df.schema.fields if str(field.dataType) in ["IntegerType()", "DoubleType()", "FloatType()", "LongType()"] and field.name != "loan_status"
    ]
    return numerical_columns

def plot_distribution(df, target_cols):
    for col_name in target_cols:
        plt.figure(figsize=(8, 6))
        # Convert the PySpark DataFrame column to a pandas Series for plotting
        pd_series = df.select(col_name).toPandas()[col_name]
        pd_series.dropna().hist(bins=30, grid=False, color='blue', alpha=0.7)
        plt.title(f'Distribution of {col_name}', fontsize=14)
        plt.xlabel(col_name, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(False)
        plt.show()

def save_to_parquet(df, output_dir, key, mode=None):
    try:
        df.to_hdf(output_dir, key=key, mode=mode)  
    except FileNotFoundError as e:
        print(e)
    
def cast_incorrect_column_type(df):
    # Danh sách các cột cần chuyển đổi thành số
    numerical_columns = [
        'person_age',
        'person_income',
        'person_emp_exp',
        'loan_amnt',
        'loan_int_rate',
        'loan_percent_income',
        'cb_person_cred_hist_length',
        'credit_score'
    ]

    numerical_columns = [col for col in numerical_columns if col in df.columns]

    # Chuyển đổi các cột sang kiểu float, xử lý lỗi nếu có giá trị không hợp lệ
    for col in numerical_columns:
        if col in df.columns:
            # Use PySpark's cast function to convert the column type
            df = df.withColumn(col, F.col(col).cast(T.DoubleType()))
    
    return df

def test_stratified_sampling(source_df, 
                             train_df,
                             test_df,
                             val_df
                            ):
    source_df_class_proportion = source_df['loan_status'].value_counts()[0] / source_df['loan_status'].value_counts()[1]
    train_df_class_proportion = train_df['loan_status'].value_counts()[0] / train_df['loan_status'].value_counts()[1]
    val_df_class_proportion = val_df['loan_status'].value_counts()[0] / val_df['loan_status'].value_counts()[1]
    test_df_class_proportion = test_df['loan_status'].value_counts()[0] / test_df['loan_status'].value_counts()[1]

    if source_df_class_proportion == train_df_class_proportion == val_df_class_proportion == test_df_class_proportion:
        print("The proportion of class in each set are the same")