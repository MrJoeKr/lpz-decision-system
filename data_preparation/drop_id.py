import pandas as pd

from lib.column_names import DATA_COLUMNS


def drop_id_from_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Drop the ID column from the data.

    Parameters:
        data: pd.DataFrame
            Data to remove the ID column from

    Returns:
        tuple[pd.DataFrame, pd.Series]
            Data without the ID column, and the ID column
    """
    assert hasattr(DATA_COLUMNS, "patient_id")

    return (
        data.drop(DATA_COLUMNS.patient_id, axis=1),
        data[DATA_COLUMNS.patient_id].copy(),
    )
