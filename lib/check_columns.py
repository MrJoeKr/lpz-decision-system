import logging

import pandas as pd

from lib.column_names import RAW_DATA_COLUMNS, get_column_names


logger = logging.getLogger(__name__)


def check_data_columns(data: pd.DataFrame) -> None:
    """Check if all required columns are present in the data.

    Parameters:
        data: pd.DataFrame
            Data to check

    Raises:
        ValueError: If a required column is missing
    """
    missing_cols = [
        col for col in get_column_names(RAW_DATA_COLUMNS) if col not in data.columns
    ]

    if RAW_DATA_COLUMNS.target in missing_cols:
        logger.warning(
            "The target column is missing. This is expected if the data is intended for prediction."
        )
        missing_cols.remove(RAW_DATA_COLUMNS.target)

    if missing_cols:
        raise ValueError(f"Missing columns in the data: {missing_cols}")
