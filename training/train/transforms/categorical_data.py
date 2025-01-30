from pyspark.ml.feature import OneHotEncoder, StringIndexer
from pyspark.ml import Pipeline

def onehot_encoding_pipeline(train_df, categorical_columns):
    """
    Xử lý dữ liệu phân loại bằng cách sử dụng One-hot encoding.

    Args:
        df: Train PySpark DataFrame.
        categorical_columns: Danh sách các cột phân loại cần xử lý.

    Returns:
        Encoded pipeline
    """

    stages = []

    for categorical_col in categorical_columns:
        # Tạo StringIndexer để chuyển đổi các giá trị chuỗi thành chỉ mục số
        indexer = StringIndexer(inputCol=categorical_col, outputCol=categorical_col + "_index")
        indexer.setHandleInvalid("skip")  
        stages.append(indexer)
        # Tạo OneHotEncoder để chuyển đổi chỉ mục số thành vectơ 
        encoder = OneHotEncoder(inputCol=categorical_col + "_index", outputCol=categorical_col + "_encoded")
        stages.append(encoder)

    pipeline = Pipeline(stages=stages)
    pipeline = pipeline.fit(train_df)

    return pipeline