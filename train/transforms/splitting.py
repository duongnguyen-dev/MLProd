from sklearn.model_selection import train_test_split

def stratified_splitting(df, 
                         train_size: float=0.8, 
                         test_size: float=0.1, 
                         val_size: float=0.1,
                         random_state=42
                        ):
    """
        Split the dataset to train, test, and val sets using Stratified Sampling method
        Arguments:
            - df: Dataset
            - train_size: Size of training set, the default size 80% of total dataset size
            - test_size: Size of test set, the default size 10% of total dataset size
            - val_size: Size of val set, the default size 10% of total dataset size
            - random_state
    """

    train_df, temp_df = train_test_split(df, test_size=test_size + val_size, stratify=df["loan_status"], random_state=random_state)
    test_df, val_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df["loan_status"], random_state=random_state)

    return train_df, test_df, val_df

def over_splitting():
    pass

def smote_splitting():
    pass

def under_splitting():
    pass

def tomek_splitting():
    pass
