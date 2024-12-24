from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks
import pandas as pd

def split_dataset(X, y, train_size: float=0.8, test_size: float=0.1, val_size: float=0.1, random_state=42):
    """
        Split features (X) and target (y) into train, test, and val sets.
        Arguments:
            - X: Features
            - y: Target labels
            - train_size: Training set proportion
            - test_size: Test set proportion
            - val_size: Validation set proportion
            - random_state
    """
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=test_size + val_size, random_state=random_state)
    X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5, random_state=random_state)

    return (X_train, y_train), (X_test, y_test), (X_val, y_val)

def over_splitting(df, target_column="loan_status", random_state=42):
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
                                          random_state=random_state)

    balanced_df = pd.concat([majority_class, minority_class_oversampled])
    X = balanced_df.drop(columns=[target_column])
    y = balanced_df[target_column]
    return split_dataset(X, y, random_state=random_state)

def smote_splitting(df, target_column="loan_status", random_state=42):
    """
        Perform oversampling using SMOTE.
        Arguments:
            - df: Dataset
            - target_column: Target column to balance
    """
    smote = SMOTE(random_state=random_state)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_smote, y_smote = smote.fit_resample(X, y)
    return split_dataset(X_smote, y_smote, random_state=random_state)

def under_splitting(df, target_column="loan_status", random_state=42):
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
                                          random_state=random_state)

    balanced_df = pd.concat([majority_class_downsampled, minority_class])
    X = balanced_df.drop(columns=[target_column])
    y = balanced_df[target_column]
    return split_dataset(X, y, random_state=random_state)

def tomek_splitting(df, target_column="loan_status", random_state=42):
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
    return split_dataset(X_resampled, y_resampled, random_state=random_state)
