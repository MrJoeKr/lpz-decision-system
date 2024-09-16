"""
Class for column names.
"""

VariableName = str
ColumnName = str


class ColumnVariableMap:
    """
    For each `VariableName` there is a corresponding variable in the class with the name
    in `ColumnName` that is the column name in the data.
    """

    def __init__(self, dictionary: dict[VariableName, ColumnName]):
        self._dict = dictionary
        # Create the variables in the class
        for var_name, col_name in dictionary.items():
            setattr(self, var_name, col_name)

    def __getitem__(self, key: VariableName) -> ColumnName:
        return self._dict[key]

    def __contains__(self, key: VariableName) -> bool:
        return key in self._dict

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()
