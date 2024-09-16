"""
GUI window for training the model and saving it
"""

import logging
import tkinter.filedialog
from datetime import datetime
from pathlib import Path

import pandas as pd
import ttkbootstrap as ttk
import xgboost as xgb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from data_preparation import preprocess_data
from data_preparation.drop_id import drop_id_from_data
from gui.error_wrapper import on_event_error_wrapper
from lib import DATA_COLUMNS as DC
from model import train

logger = logging.getLogger(__name__)


class TrainFrame(ttk.Frame):
    """
    TrainWindow class for training the model and saving it.
    Consists of the following widgets:
    - Title label
    - Choose training data button
    - Train and save model button
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, padding=15, *args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        master.title("Train the model")

        self.title_label = ttk.Label(
            self, text="Train the model", style="primary.TLabel"
        )
        self.title_label.pack(pady=10)

        # Default path to the data directory
        self.default_path = Path(Path().absolute(), "data")
        # Path to the RAW training data
        self.data_path_var = ttk.StringVar(value=self.default_path)

        date_today = datetime.now().strftime("%Y-%m-%d")
        model_today_dir = Path(self.default_path, "models", date_today)

        self.save_model_path_var = ttk.StringVar(
            value=Path(model_today_dir, "model.json")
        )

        # header and labelframe option container
        option_text = "Select training data"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_path_row()
        self.create_save_model_row()
        self.create_train_button()

    def create_path_row(self):
        """Add path row to labelframe"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES, pady=(5, 10))

        path_lbl = ttk.Label(path_row, text="Take data from:", width=15)
        path_lbl.pack(side=LEFT, padx=(15, 0))

        path_ent = ttk.Entry(
            path_row, textvariable=self.data_path_var, width=50
        )
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        browse_btn = ttk.Button(
            master=path_row,
            text="Browse",
            command=self.on_browse_data,
            width=8,
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_save_model_row(self):
        """Add save model path row to labelframe"""
        save_model_row = ttk.Frame(self.option_lf)
        save_model_row.pack(fill=X, expand=YES, pady=10)

        save_model_lbl = ttk.Label(
            save_model_row, text="Save model to:", width=15
        )
        save_model_lbl.pack(side=LEFT, padx=(15, 0))

        save_model_ent = ttk.Entry(
            save_model_row, textvariable=self.save_model_path_var, width=50
        )
        save_model_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        browse_btn = ttk.Button(
            master=save_model_row,
            text="Browse",
            command=self.on_browse_save_model,
            width=8,
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_train_button(self):
        """Add train button to labelframe"""
        train_btn = ttk.Button(
            self.option_lf,
            text="Train and save model",
            command=self.on_train,
        )
        train_btn.pack(pady=10)

    def on_browse_data(self):
        """Open file dialog to select training data"""
        path = tkinter.filedialog.askopenfilename(
            initialdir=self.default_path,
            title="Select training data",
            filetypes=[("CSV files", "*.csv")],
        )
        if path:
            self.data_path_var.set(path)

    def on_browse_save_model(self):
        """Open file dialog to select save model path"""
        path = tkinter.filedialog.asksaveasfilename(
            initialdir=Path(self.default_path, "models"),
            title="Save model to",
            filetypes=[("JSON files", "*.json")],
        )
        if path:
            self.save_model_path_var.set(path)

    def _check_save_path_suffix(self, save_path: Path) -> None:
        logging.debug(f"SUFFIX: {save_path.suffix}")
        if save_path.suffix != ".json":
            raise ValueError(
                f"Model must be saved as a JSON file, got {save_path.name}"
            )

    @on_event_error_wrapper(logger=logger)
    def on_train(self):
        """Train the model and save it"""
        save_path = Path(self.save_model_path_var.get())
        self._check_save_path_suffix(save_path)

        data_path = self.data_path_var.get()

        logger.info(f"Preprocessing data at {data_path}")
        data = preprocess_data(pd.read_csv(data_path))
        # Drop the ID column from the data
        data, _ = drop_id_from_data(data)
        logger.info("Data preprocessed successfully")

        logger.info(f"Training model with preprocessed data")
        model = train(data)
        logger.info("Model trained successfully")

        self.save_model(model, save_path)

    def save_model(self, model: xgb.XGBClassifier, save_path: Path) -> None:
        """
        Save the model to the given path.

        Parameters:
            model: xgb.XGBClassifier
                Model to save
            save_path: Path
                Path to save the model to
        """

        logger.info(f"Saving model to {save_path}")
        # Create parent directories if they do not exist
        save_path.parent.mkdir(parents=True, exist_ok=True)
        model.save_model(save_path)
        logger.info("Model saved successfully")

        # Show window with success message
        Messagebox.show_info(
            title="Model saved",
            message=f"Model saved successfully to {save_path}",
            alert=True,
        )


if __name__ == "__main__":
    root = ttk.Window()
    train_window = TrainFrame(root)
    train_window.pack()

    logging.basicConfig(level=logging.DEBUG)

    root.mainloop()
