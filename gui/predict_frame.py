"""
Frame for prediction of the model
"""

import logging
import tkinter
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
from model.hyperparams import get_xgbc_hyperparams

logger = logging.getLogger(__name__)


OPTION_LF_LABEL_WIDTH = 13


class PredictFrame(ttk.Frame):
    """
    PredictFrame class for predicting new data using the model.
    Consists of the following widgets:
    - Title label
    - Choose model button
    - Choose data button
    - Predict button
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, padding=15, *args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        master.title("Predict new data")

        ttk.Label(self, text="Predict new data", style="primary.TLabel").pack(
            pady=10
        )

        self.default_path = Path(Path().absolute(), "data")

        # Set default paths
        self.model_path_var = ttk.StringVar(
            value=Path(
                self.default_path,
                "models",
                datetime.now().strftime("%Y-%m-%d"),
                "model.json",
            )
        )
        self.data_path_var = ttk.StringVar(value=Path(self.default_path))
        self.save_data_path_var = ttk.StringVar(
            value=Path(self.default_path, "predict", "data.csv")
        )

        # header and labelframe option container
        option_text = "Select model and data"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_model_path_row()
        self.create_data_path_row()
        self.create_data_save_path_row()
        self.create_predict_button()

    def create_model_path_row(self):
        """Add model path row to labelframe"""
        model_path_row = ttk.Frame(self.option_lf)
        model_path_row.pack(fill=X, expand=YES, pady=(5, 10))

        ttk.Label(
            model_path_row, text="Model path:", width=OPTION_LF_LABEL_WIDTH
        ).pack(side=LEFT, padx=5)

        self.model_path_entry = ttk.Entry(
            model_path_row, textvariable=self.model_path_var, width=50
        )
        self.model_path_entry.pack(side=LEFT, padx=5)

        self.choose_model_button = ttk.Button(
            model_path_row,
            text="Choose model",
            style="primary.TButton",
            command=self._on_choose_model,
        )
        self.choose_model_button.pack(side=LEFT, padx=5)

    @on_event_error_wrapper(logger=logger)
    def _on_choose_model(self):
        """Open file dialog to choose model"""
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=self.default_path,
            title="Select model file",
            filetypes=[("JSON files", "*.json")],
        )
        self.model_path_var.set(file_path)

    def create_data_path_row(self):
        """Add data path row to labelframe"""
        data_path_row = ttk.Frame(self.option_lf)
        data_path_row.pack(fill=X, expand=YES, pady=10)

        ttk.Label(
            data_path_row, text="Data path:", width=OPTION_LF_LABEL_WIDTH
        ).pack(side=LEFT, padx=5)

        self.data_path_entry = ttk.Entry(
            data_path_row, textvariable=self.data_path_var, width=50
        )
        self.data_path_entry.pack(side=LEFT, padx=5)

        self.choose_data_button = ttk.Button(
            data_path_row,
            text="Choose data path",
            style="primary.TButton",
            command=self._on_choose_data,
        )
        self.choose_data_button.pack(side=LEFT, padx=5)

    @on_event_error_wrapper(logger=logger)
    def _on_choose_data(self):
        """Open file dialog to choose data"""
        file_path = tkinter.filedialog.askopenfilename(
            initialdir=self.default_path,
            title="Select data file",
            filetypes=[("CSV files", "*.csv")],
        )
        self.data_path_var.set(file_path)

    def create_predict_button(self):
        """Add predict button to labelframe"""
        predict_btn = ttk.Button(
            self.option_lf,
            text="Predict",
            command=self.on_predict,
        )
        predict_btn.pack(pady=10)

    @on_event_error_wrapper(logger=logger)
    def on_predict(self) -> None:
        """
        Predict new data using the model.
        Save the predictions to the specified path.
        """
        model_path = Path(self.model_path_var.get())
        data_path = Path(self.data_path_var.get())

        # Load the model
        logger.info(f"Predicting data using model: {model_path}")
        model = xgb.XGBClassifier(**get_xgbc_hyperparams())
        model.load_model(model_path)

        # Load the data
        logger.info(f"Loading data: {data_path}")
        data = pd.read_csv(data_path)
        # Preprocess the data
        logger.info("Preprocessing data")
        data = preprocess_data(data)
        data, _ = drop_id_from_data(data)

        assert hasattr(DC, "target")
        if DC.target in data.columns:
            logger.warning(
                f"Data contains target column '{DC.target}', dropping it"
            )
            data.drop(DC.target, axis=1, inplace=True)

        logger.info("Data preprocessed successfully")

        logger.info("Predicting data")
        predictions = model.predict(data)
        logger.info("Data predicted successfully")

        # Save the predictions
        save_data_path = Path(self.save_data_path_var.get())
        logger.info(f"Saving predictions to: {save_data_path}")
        predictions_df = pd.DataFrame(predictions, columns=["prediction"])

        save_data_path.parent.mkdir(parents=True, exist_ok=True)
        predictions_df.to_csv(save_data_path, index=False)

        logger.info("Predictions saved successfully")

        Messagebox.show_info(
            title="Predictions saved",
            message=f"Predictions saved to {save_data_path}",
            alert=True,
        )

    def create_data_save_path_row(self):
        """Add data save path row to labelframe"""
        data_save_path_row = ttk.Frame(self.option_lf)
        data_save_path_row.pack(fill=X, expand=YES, pady=10)

        ttk.Label(
            data_save_path_row,
            text="Save path:",
            width=OPTION_LF_LABEL_WIDTH,
        ).pack(side=LEFT, padx=5)

        self.data_save_path_entry = ttk.Entry(
            data_save_path_row, textvariable=self.save_data_path_var, width=50
        )
        self.data_save_path_entry.pack(side=LEFT, padx=5)

        self.choose_data_save_button = ttk.Button(
            data_save_path_row,
            text="Choose save path",
            style="primary.TButton",
            command=self._on_choose_data_save,
        )
        self.choose_data_save_button.pack(side=LEFT, padx=5)

    @on_event_error_wrapper(logger=logger)
    def _on_choose_data_save(self):
        """Open file dialog to choose data save path"""
        file_path = tkinter.filedialog.asksaveasfilename(
            initialdir=self.default_path,
            title="Select save path",
            filetypes=[("CSV files", "*.csv")],
        )
        self.save_data_path_var.set(file_path)
