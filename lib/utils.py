import pandas as pd


def get_dir_path(year: int) -> str:
    """
    Get the directory path for the data of a given year.

    Parameters:
        year: int
            The year of the data.

    Returns:
        str
            The directory path.
    """
    return f"data/{year}"


def get_file_path(year: int) -> str:
    """
    Get the file path for the data of a given year.

    Parameters:
        year: int
            The year of the data.

    Returns:
        str
            The file path.
    """
    return f"{get_dir_path(year)}/nnch_{year}.xlsx"


def get_preprocessed_file_path(year: int) -> str:
    """
    Get the file path for the preprocessed data of a given year.

    Parameters:
        year: int
            The year of the data.

    Returns:
        str
            The file path.
    """
    return f"{get_dir_path(year)}/nnch_{year}_preprocessed.csv"


def read_raw_dataset(year: int, header: int = 0) -> pd.DataFrame:
    """
    Read the raw dataset of a given year.

    Parameters:
        year: int
            The year of the data.
        header: int
            The row number to use as the column names.

    Returns:
        pd.DataFrame
            The raw dataset.
    """
    data = pd.read_excel(get_file_path(year), header=header)

    return data


def read_preprocessed_dataset(year: int) -> pd.DataFrame:
    """
    Read the preprocessed dataset of a given year.

    Parameters:
        year: int
            The year of the data.
        
    Returns:
        pd.DataFrame
            The preprocessed dataset.
    """
    data = pd.read_csv(get_preprocessed_file_path(year))

    return data
