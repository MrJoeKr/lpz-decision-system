import pandas as pd

from lib.column_names import _REQUIRED_COLUMNS


def check_data_columns(data: pd.DataFrame) -> None:
    """
    Check if all required columns are present in the data.

    Parameters:
        data: pd.DataFrame
            Data to check

    Raises:
        ValueError: If a required column is missing
    """
    missing_cols = [
        col for col in _REQUIRED_COLUMNS.values() if col not in data.columns
    ]
    if missing_cols:
        raise ValueError(f"Missing columns in the data: {missing_cols}")
