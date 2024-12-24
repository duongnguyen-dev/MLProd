from pyspark.ml.feature import OneHotEncoder, StringIndexer

def handle_categorical_data(df, categorical_columns):
    """
    Xử lý dữ liệu phân loại bằng cách sử dụng One-hot encoding.

    Args:
        df: PySpark DataFrame.
        categorical_columns: Danh sách các cột phân loại cần xử lý.

    Returns:
        PySpark DataFrame với các cột phân loại đã được mã hóa.
    """

    for categorical_col in categorical_columns:
        # Tạo StringIndexer để chuyển đổi các giá trị chuỗi thành chỉ mục số
        stringIndexer = StringIndexer(inputCol=categorical_col, outputCol=categorical_col + "_index")

        # Tạo OneHotEncoder để chuyển đổi chỉ mục số thành vectơ 
        encoder = OneHotEncoder(inputCols=[stringIndexer.getOutputCol()], outputCols=[categorical_col + "_encoded"])

        # Khớp và chuyển đổi DataFrame
        df = stringIndexer.fit(df).transform(df)
        df = encoder.fit(df).transform(df)

    return df