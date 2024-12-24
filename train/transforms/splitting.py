from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks
import pandas as pd

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

def over_splitting(df, target_column="loan_status"):
    """
        Perform oversampling by duplicating samples of the minority class.
        Arguments:
            - df: Dataset
            - target_column: Target column to balance
    """
    majority_class = df[df[target_column] == df[target_column].value_counts().idxmax()]
    minority_class = df[df[target_column] != df[target_column].value_counts().idxmax()]

    minority_class_oversampled = resample(minority_class, 
                                          replace=True, 
                                          n_samples=len(majority_class), 
                                          random_state=42)

    balanced_df = pd.concat([majority_class, minority_class_oversampled])
    return balanced_df

def smote_splitting(df, target_column="loan_status"):
    """
        Perform oversampling using SMOTE.
        Arguments:
            - df: Dataset
            - target_column: Target column to balance
    """
    smote = SMOTE(random_state=42)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_smote, y_smote = smote.fit_resample(X, y)

    balanced_df = pd.concat([X_smote, y_smote], axis=1)
    return balanced_df

def under_splitting(df, target_column="loan_status"):
    """
        Perform undersampling by removing samples from the majority class.
        Arguments:
            - df: Dataset
            - target_column: Target column to balance
    """
    majority_class = df[df[target_column] == df[target_column].value_counts().idxmax()]
    minority_class = df[df[target_column] != df[target_column].value_counts().idxmax()]

    majority_class_downsampled = resample(majority_class, 
                                          replace=False, 
                                          n_samples=len(minority_class), 
                                          random_state=42)

    balanced_df = pd.concat([majority_class_downsampled, minority_class])
    return balanced_df

def tomek_splitting(df, target_column="loan_status"):
    """
        Perform undersampling using Tomek Links.
        Arguments:
            - df: Dataset
            - target_column: Target column to balance
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    tomek = TomekLinks()
    X_resampled, y_resampled = tomek.fit_resample(X, y)

    balanced_df = pd.concat([X_resampled, y_resampled], axis=1)
    return balanced_df
