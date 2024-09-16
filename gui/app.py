import logging

from gui.main_menu_window import MenuWindow

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run() -> None:
    """
    Run the application.
    """
    app = MenuWindow()

    logger.info("Starting the application")

    app.mainloop()


if __name__ == "__main__":
    run()
