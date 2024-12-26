from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks
import pandas as pd

def over_splitting(df, test_size: float=0.1, val_size: float=0.1, target_column="loan_status", random_state=42):
    """
        Perform oversampling by duplicating samples of the minority class and splitting into train, test, and val.
        Arguments:
            - df: Dataset
            - test_size: Test set proportion
            - val_size: Validation set proportion
            - target_column: Target column to balance
            - random_state
    """
    majority_class = df[df[target_column] == df[target_column].value_counts().idxmax()]
    minority_class = df[df[target_column] != df[target_column].value_counts().idxmax()]

    minority_class_oversampled = resample(minority_class, 
                                          replace=True, 
                                          n_samples=len(majority_class), 
                                          random_state=random_state)

    balanced_df = pd.concat([majority_class, minority_class_oversampled])
    train_df, temp_df = train_test_split(balanced_df, test_size=test_size + val_size, stratify=balanced_df[target_column], random_state=random_state)
    test_df, val_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df[target_column], random_state=random_state)

    return train_df, test_df, val_df

def smote_splitting(df, test_size: float=0.1, val_size: float=0.1, target_column="loan_status", random_state=42):
    """
        Perform oversampling using SMOTE and splitting into train, test, and val.
        Arguments:
            - df: Dataset
            - test_size: Test set proportion
            - val_size: Validation set proportion
            - target_column: Target column to balance
            - random_state
    """
    smote = SMOTE(random_state=random_state)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_smote, y_smote = smote.fit_resample(X, y)

    balanced_df = pd.concat([X_smote, y_smote], axis=1)
    train_df, temp_df = train_test_split(balanced_df, test_size=test_size + val_size, stratify=balanced_df[target_column], random_state=random_state)
    test_df, val_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df[target_column], random_state=random_state)

    return train_df, test_df, val_df

def under_splitting(df, test_size: float=0.1, val_size: float=0.1, target_column="loan_status", random_state=42):
    """
        Perform undersampling by removing samples from the majority class and splitting into train, test, and val.
        Arguments:
            - df: Dataset
            - test_size: Test set proportion
            - val_size: Validation set proportion
            - target_column: Target column to balance
            - random_state
    """
    majority_class = df[df[target_column] == df[target_column].value_counts().idxmax()]
    minority_class = df[df[target_column] != df[target_column].value_counts().idxmax()]

    majority_class_downsampled = resample(majority_class, 
                                          replace=False, 
                                          n_samples=len(minority_class), 
                                          random_state=random_state)

    balanced_df = pd.concat([majority_class_downsampled, minority_class])
    train_df, temp_df = train_test_split(balanced_df, test_size=test_size + val_size, stratify=balanced_df[target_column], random_state=random_state)
    test_df, val_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df[target_column], random_state=random_state)

    return train_df, test_df, val_df

def tomek_splitting(df, test_size: float=0.1, val_size: float=0.1, target_column="loan_status", random_state=42):
    """
        Perform undersampling using Tomek Links and splitting into train, test, and val.
        Arguments:
            - df: Dataset
            - test_size: Test set proportion
            - val_size: Validation set proportion
            - target_column: Target column to balance
            - random_state
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    tomek = TomekLinks()
    X_resampled, y_resampled = tomek.fit_resample(X, y)

    balanced_df = pd.concat([X_resampled, y_resampled], axis=1)
    train_df, temp_df = train_test_split(balanced_df, test_size=test_size + val_size, stratify=balanced_df[target_column], random_state=random_state)
    test_df, val_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df[target_column], random_state=random_state)

    return train_df, test_df, val_df
