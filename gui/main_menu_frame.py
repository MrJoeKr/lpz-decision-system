"""
Main menu window.
"""

import logging
import sys

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, YES

from gui.error_wrapper import on_event_error_wrapper
from gui.predict_frame import PredictFrame
from gui.train_frame import TrainFrame

logger = logging.getLogger(__name__)

BUTTON_WIDTH = 20


class MainMenuFrame(ttk.Frame):
    """
    Main menu window class.
    Consists of the following widgets:
    - Title label
    - Train model button
    - Predict button
    - Exit button
    """

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, padding=15, *args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        master.title("LPZ-NOR Decision System")

        self.title_label = ttk.Label(
            self, text="Main Menu", style="primary.TLabel"
        )
        self.title_label.pack(pady=10)

        self.create_train_button()
        self.create_predict_button()
        self.create_exit_button()

    def create_train_button(self):
        self.train_button = ttk.Button(
            self,
            text="Train model",
            style="primary.TButton",
            command=self._on_train,
            width=BUTTON_WIDTH,
        )
        self.train_button.pack(pady=10)

    @on_event_error_wrapper(logger=logger)
    def _on_train(self):
        """
        When the user clicks the "Train model" button.
        The window is switched to the TrainWindow.
        """
        self.master.switch_frame(TrainFrame)

    def create_predict_button(self):
        self.predict_button = ttk.Button(
            self,
            text="Predict",
            style="primary.TButton",
            width=BUTTON_WIDTH,
            command=self._on_predict,
        )
        self.predict_button.pack(pady=10)

    @on_event_error_wrapper(logger=logger)
    def _on_predict(self):
        """
        When the user clicks the "Predict" button.
        The window is switched to the PredictWindow.
        """
        self.master.switch_frame(PredictFrame)

    def create_exit_button(self):
        self.exit_button = ttk.Button(
            self,
            text="Exit",
            style="danger.TButton",
            command=self._quit_app,
            width=BUTTON_WIDTH,
        )
        self.exit_button.pack(pady=10)

    def _quit_app(self):
        logger.info("Exiting the application")
        self.master.destroy()


if __name__ == "__main__":
    root = ttk.Window()

    main_menu = MainMenuFrame(root)
    main_menu.pack(fill=BOTH, expand=YES)

    logging.basicConfig(level=logging.DEBUG)

    root.mainloop()
