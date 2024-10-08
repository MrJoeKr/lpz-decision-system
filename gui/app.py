import logging

from gui.main_menu_window import MainWindow

logger = logging.getLogger(__name__)


def run() -> None:
    """
    Run the application.
    """
    app = MainWindow()

    logger.info("Starting the application")

    app.mainloop()


if __name__ == "__main__":
    run()
