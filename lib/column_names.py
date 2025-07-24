from dataclasses import dataclass, fields


@dataclass(frozen=True)
class RawDataColumns:
    patient_id: str = "IDLPZ"
    date_of_diagnosis: str = "DatumStanoveniDg"
    lpz_diagnosis: str = "Chyb_DG"
    nor_diagnosis: str = "DgKod"
    target: str = "Stav"


@dataclass(frozen=True)
class ProcessedDataColumns:
    year: str = "Rok"


RAW_DATA_COLUMNS = RawDataColumns()
PROCESSED_DATA_COLUMNS = ProcessedDataColumns()


def get_column_names(
    dataclass_instance: RawDataColumns | ProcessedDataColumns,
) -> list[str]:
    """Get the column names from a dataclass instance."""
    return [
        getattr(dataclass_instance, field.name) for field in fields(dataclass_instance)
    ]
