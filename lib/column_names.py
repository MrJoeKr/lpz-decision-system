from lib._col_name_class import ColumnName, ColumnVariableMap, VariableName

# Column names in the data that are required before data processing
# Variable names can be used in the code
_REQUIRED_COLUMNS: dict[VariableName, ColumnName] = {
    # Variable name: Column name
    # DO NOT change the variable names of the columns below,
    # only the column names
    "patient_id": "IDLPZ",
    "date_of_diagnosis": "DatumStanoveniDg",
    "lpz_diagnosis": "Chyb_DG",
    "nor_diagnosis": "DgKod",
    "target": "Stav",
    # Add the column names that are required for the model here
}

_AFTER_PREPROCESSING_COLUMNS: dict[VariableName, ColumnName] = {
    "year": "Rok",
}

DATA_COLUMNS = ColumnVariableMap(
    _REQUIRED_COLUMNS | _AFTER_PREPROCESSING_COLUMNS
)
