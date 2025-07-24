import pandas as pd

from lib.column_names import PROCESSED_DATA_COLUMNS, RAW_DATA_COLUMNS


def deduplicate_data_by_dgkod(
    data: pd.DataFrame,
    id_col: str | None = None,
    year_col: str | None = None,
) -> pd.DataFrame:
    """Deduplicate the data by the `RAW_DATA_COLUMNS.patient_id` and `RAW_DATA_COLUMNS.nor_diagnosis` columns.

    The deduplication is done by in the following way:
      - The records of `data` are grouped by the `id_col` and `DgKod` columns.
      - For each group, the record with the highest value in the `year_col` column is kept.
      - The rest of the records are removed. If the other records have different value in `TARGET_COL`,
        then the ones with the highest value in `TARGET_COL` are kept.
    """
    if id_col is None:
        # Add assert for mypy check
        id_col = RAW_DATA_COLUMNS.patient_id
    if year_col is None:
        year_col = PROCESSED_DATA_COLUMNS.year

    new_data: list[pd.DataFrame] = []

    for _, group in data.groupby([id_col, RAW_DATA_COLUMNS.nor_diagnosis]):
        if len(group) == 1:
            new_data.append(group)
            continue

        group = group.sort_values([RAW_DATA_COLUMNS.target, year_col], ascending=False)

        new_data.append(group.head(1))

    return pd.concat(new_data)
