import pandas as pd

from lib import check_data_columns
from lib.column_names import DATA_COLUMNS

# Pattern for ICD-10 code
ICD_PATTERN_REGEX = r"([DC]\d{2,3})"


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess data for the analysis

    Parameters:
        data: pd.DataFrame
            Raw data to be preprocessed

    Returns:
        pd.DataFrame
            Preprocessed data
    """
    check_data_columns(data)

    assert hasattr(DATA_COLUMNS, "target")
    assert hasattr(DATA_COLUMNS, "patient_id")
    assert hasattr(DATA_COLUMNS, "lpz_diagnosis")
    assert hasattr(DATA_COLUMNS, "date_of_diagnosis")

    # Copy data to not modify original data
    data = data.copy()[DATA_COLUMNS.values()]

    # Forward fill patient ID and new diagnosis
    # Rows are expected to be grouped by Patient ID, so missing values
    # are filled with the previous value
    ffill_cols = [DATA_COLUMNS.patient_id, DATA_COLUMNS.lpz_diagnosis]
    data[ffill_cols] = data[ffill_cols].ffill()

    # Date to year
    # Transform to date
    data[DATA_COLUMNS.date_of_diagnosis] = pd.to_datetime(
        data[DATA_COLUMNS.date_of_diagnosis], errors="coerce"
    )
    # Extract year
    data["Rok"] = data[DATA_COLUMNS.date_of_diagnosis].dt.year
    # Drop Date column
    data = data.drop(DATA_COLUMNS.date_of_diagnosis, axis=1)

    # Fill missing year with 10 years before the minimum year
    fill_year = data["Rok"].min() - 10
    data["Rok"] = data["Rok"].fillna(fill_year).astype(int)

    # Set categorical columns
    # data[["Chyb_DG", "DgKod"]] = data[["Chyb_DG", "DgKod"]].astype("category")

    data = update_target_col(data)

    # Transform diagnosis codes to numbers
    data = transform_dg_codes_to_num(data)

    # Move target column to the end
    data = data[
        [col for col in data.columns if col != DATA_COLUMNS.target]
        + [DATA_COLUMNS.target]
    ]

    return data


def transform_dg_codes_to_num(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform diagnosis codes to numbers
    """
    assert hasattr(DATA_COLUMNS, "lpz_diagnosis")
    assert hasattr(DATA_COLUMNS, "nor_diagnosis")

    data = data.copy()
    # Transform NOR diagnosis to number
    data[DATA_COLUMNS.nor_diagnosis] = diagnosis_to_number(
        data[DATA_COLUMNS.nor_diagnosis]
    )

    # Check there are no missing values in new diagnosis
    if data[DATA_COLUMNS.lpz_diagnosis].isnull().sum() > 0:
        raise ValueError(
            f"There are missing values in {DATA_COLUMNS.lpz_diagnosis}"
        )

    data[DATA_COLUMNS.lpz_diagnosis] = diagnosis_to_number(
        data[DATA_COLUMNS.lpz_diagnosis]
    )
    return data


def diagnosis_to_number(data: pd.Series) -> pd.Series:
    """
    Transform diagnosis to number in the following way:
        - If starts with "D" then add 1000
        - Else (C) add 0
        - Impute missing values with -1
    Other numbers are left as they are.
    """
    data = data.copy()

    data = data.fillna(-1).astype(str)
    # Add zero to DgKod if the length is 3 (e.g., C64 -> C640)
    data = data.apply(lambda x: x + "0" if len(x) == 3 else x)

    def transform(x):
        # Skip missing values
        if x == "-1":
            return int(x)

        out = str(x)[1:]

        if len(out) == 1 or len(out) > 3:
            raise ValueError(f"Invalid diagnosis code: {x}")

        out = int(out)

        if str(x).startswith("D"):
            out += 1000

        if not str(x).startswith("D") and not str(x).startswith("C"):
            raise ValueError(f"Invalid diagnosis code: {x}")

        return out

    return data.apply(transform)


def fix_dgkod_target_col(data: pd.DataFrame) -> pd.DataFrame:
    assert hasattr(DATA_COLUMNS, "target")
    data = data.copy()
    data[DATA_COLUMNS.target] = data[DATA_COLUMNS.target].astype(str)

    # Strip
    data[DATA_COLUMNS.target] = data[DATA_COLUMNS.target].str.strip()

    # Extract from target col the pattern "D" or "C" followed by 2 or 3 digits
    data[DATA_COLUMNS.target] = (
        data[DATA_COLUMNS.target].str.extract(ICD_PATTERN_REGEX).fillna("0")
    )

    # Add zero to diagnosis if the length is 3 (e.g., C64 -> C640)
    update_cols = ["DgKod", DATA_COLUMNS.target]
    data[update_cols] = data[update_cols].apply(
        lambda x: x + "0" if len(x) == 3 else x
    )

    data = _fill_diagnoses_target_col(data)

    return data


def _fill_diagnoses_target_col(data: pd.DataFrame) -> pd.DataFrame:
    """
    For each group by IDLPZ, fill the TARGET_COL with the diagnosis of TARGET_COL
    if there is at least one present matching the pattern of ICD-10 code.
    Target column is expected to be in the format of ICD-10 code and with no missing values.

    Parameters:
        data: pd.DataFrame
            Data to be processed

    Returns:
        pd.DataFrame
            Processed data
    """
    data = data.copy()

    assert hasattr(DATA_COLUMNS, "target")

    # Group by IDLPZ
    for _, group in data.groupby("IDLPZ"):
        # Find matching diagnosis according to the pattern of ICD-10 code
        matching_diagnosis = (
            group[DATA_COLUMNS.target]
            .str.extract(ICD_PATTERN_REGEX)
            .dropna()
            .drop_duplicates()
        )

        if len(matching_diagnosis) == 0:
            continue

        # if len(matching_diagnosis) > 1:
        #     print(
        #         f"Warning: More than one diagnosis found in the group, taking the first one:\n{group}"
        #     )

        fill_diagnosis = matching_diagnosis.iloc[0].values[0]
        # Fill only the values that are missing
        group.loc[group[DATA_COLUMNS.target] == "0", DATA_COLUMNS.target] = (
            fill_diagnosis
        )

        assert (
            group[DATA_COLUMNS.target].isnull().sum() == 0
        ), f"There are missing values in a group:\n{group}"

    return data


def update_target_col(data: pd.DataFrame) -> pd.DataFrame:
    """
    Process TARGET_COL (Y) by updating values according to the following rules:
      - For each row, set value `1` to all rows which have Y = DgKod
      (i.e., if there is a changed diagnosis, then set only the record with the given
      diagnosis to 1, else set to 0)

    Parameters:
        data: pd.DataFrame
            Data to be processed

    Returns:
        pd.DataFrame
            Processed data
    """
    data = data.copy()
    data = fix_dgkod_target_col(data)

    assert hasattr(DATA_COLUMNS, "target")

    data[DATA_COLUMNS.target] = data.apply(
        lambda x: 1 if x[DATA_COLUMNS.target] == x["DgKod"] else 0, axis=1
    )
    return data
