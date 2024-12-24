import matplotlib.pyplot as plt

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
        pandas_df = df.toPandas()
        pandas_df.to_hdf(output_dir, key=key, mode=mode)  
    except FileNotFoundError as e:
        print(e)