"""GUI window for preprocessing data and saving it."""

import logging
import tkinter.filedialog
from pathlib import Path

import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, YES, N, X
from ttkbootstrap.dialogs import Messagebox

from data_preparation import preprocess_data
from gui.error_wrapper import on_event_error_wrapper


logger = logging.getLogger(__name__)


class PrepDataFrame(ttk.Frame):
    """PrepDataFrame class for preprocessing data and saving it.

    Consists of the following widgets:
    - Title label
    - Choose raw dataset path button
    - Number of rows to skip
    - Save preprocessed data path
    - Preprocess and save button
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, padding=15, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        master.title("Preprocess Data")

        self.title_label = ttk.Label(
            self, text="Preprocess Data", style="primary.TLabel"
        )
        self.title_label.pack(pady=10)

        # Default path to the data directory
        self.default_path = Path(Path().absolute(), "data")

        # Path to the RAW data
        self.raw_data_path_var = ttk.StringVar(value=self.default_path)

        # Number of rows to skip from the raw data
        self.skip_var = ttk.IntVar(value=0)

        # Path to save preprocessed data
        self.prep_data_path_var = ttk.StringVar(value=self.default_path)

        # header and labelframe option container
        option_text = "Data Preprocessing Options"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_raw_data_path_row()
        self.create_number_of_rows_skip()
        self.create_save_prep_data_row()
        self.create_preprocess_button()

    def create_raw_data_path_row(self):
        """Add raw data path row to labelframe."""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES, pady=(5, 10))

        path_lbl = ttk.Label(path_row, text="Raw dataset path:", width=20)
        path_lbl.pack(side=LEFT, padx=(15, 0))

        path_ent = ttk.Entry(path_row, textvariable=self.raw_data_path_var, width=40)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        browse_btn = ttk.Button(
            master=path_row,
            text="Browse",
            command=self.on_browse_raw_data,
            width=8,
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_number_of_rows_skip(self):
        """Add number of rows to skip row to labelframe."""
        skip_row = ttk.Frame(self.option_lf)
        skip_row.pack(fill=X, expand=YES, pady=10)

        skip_lbl = ttk.Label(skip_row, text="Number of rows to skip:", width=20)
        skip_lbl.pack(side=LEFT, padx=(15, 0))

        skip_ent = ttk.Entry(skip_row, textvariable=self.skip_var, width=5)
        skip_ent.pack(side=LEFT, padx=5)

    def create_save_prep_data_row(self):
        """Add save preprocessed data path row to labelframe."""
        save_prep_row = ttk.Frame(self.option_lf)
        save_prep_row.pack(fill=X, expand=YES, pady=10)

        save_prep_lbl = ttk.Label(
            save_prep_row, text="Save processed data to:", width=20
        )
        save_prep_lbl.pack(side=LEFT, padx=(15, 0))

        save_prep_ent = ttk.Entry(
            save_prep_row, textvariable=self.prep_data_path_var, width=40
        )
        save_prep_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        browse_btn = ttk.Button(
            master=save_prep_row,
            text="Browse",
            command=self.on_browse_save_prep_data,
            width=8,
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_preprocess_button(self):
        """Add preprocess button to labelframe."""
        preprocess_btn = ttk.Button(
            self.option_lf,
            text="Preprocess and save data",
            command=self.on_preprocess,
        )
        preprocess_btn.pack(pady=10)

    def on_browse_raw_data(self):
        """Open file dialog to select raw data."""
        path = tkinter.filedialog.askopenfilename(
            initialdir=self.default_path,
            title="Select raw dataset",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.raw_data_path_var.set(path)

    def on_browse_save_prep_data(self):
        """Open file dialog to select save preprocessed data path."""
        path = tkinter.filedialog.asksaveasfilename(
            initialdir=self.default_path,
            title="Save preprocessed data to",
            filetypes=[("CSV files", "*.csv")],
            defaultextension=".csv",
        )
        if path:
            self.prep_data_path_var.set(path)

    def _validate_file_format(self, file_path: Path) -> None:
        """Validate that the file format is supported (xlsx or csv)."""
        suffix = file_path.suffix.lower()
        if suffix not in [".xlsx", ".csv"]:
            raise ValueError(
                f"Invalid file format: {suffix}. Only .xlsx and .csv files are supported."
            )

    def _validate_paths_different(self, raw_path: Path, prep_path: Path) -> None:
        """Validate that raw and preprocessed paths are different."""
        if raw_path.resolve() == prep_path.resolve():
            raise ValueError(
                "Raw dataset path and preprocessed dataset path cannot be the same."
            )

    def _read_data(self, file_path: Path, skip_rows: int) -> pd.DataFrame:
        """Read data from file based on its extension."""
        suffix = file_path.suffix.lower()

        if suffix == ".xlsx":
            return pd.read_excel(file_path, skiprows=skip_rows)
        elif suffix == ".csv":
            return pd.read_csv(file_path, skiprows=skip_rows)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    @on_event_error_wrapper(logger=logger)
    def on_preprocess(self):
        """Preprocess the data and save it."""
        raw_path = Path(self.raw_data_path_var.get())
        prep_path = Path(self.prep_data_path_var.get())
        skip_rows = self.skip_var.get()

        # Validate file format
        self._validate_file_format(raw_path)

        # Validate paths are different
        self._validate_paths_different(raw_path, prep_path)

        # Check if raw data file exists
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw data file not found: {raw_path}")

        logger.info(f"Reading data from {raw_path}")
        data = self._read_data(raw_path, skip_rows)
        logger.info(f"Data loaded successfully with {len(data)} rows")

        logger.info("Preprocessing data")
        preprocessed_data = preprocess_data(data)
        logger.info("Data preprocessed successfully")

        self.save_preprocessed_data(preprocessed_data, prep_path)

    def save_preprocessed_data(self, data: pd.DataFrame, save_path: Path) -> None:
        """Save the preprocessed data to the given path.

        Parameters:
            data: pd.DataFrame
                Preprocessed data to save
            save_path: Path
                Path to save the data to
        """
        logger.info(f"Saving preprocessed data to {save_path}")
        # Create parent directories if they do not exist
        save_path.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(save_path, index=False)
        logger.info("Preprocessed data saved successfully")

        # Show window with success message
        Messagebox.show_info(
            title="Data preprocessed",
            message=f"Data preprocessed and saved successfully to {save_path}",
            alert=True,
        )


if __name__ == "__main__":
    root = ttk.Window()
    prep_data_window = PrepDataFrame(root)
    prep_data_window.pack()

    logging.basicConfig(level=logging.DEBUG)

    root.mainloop()
