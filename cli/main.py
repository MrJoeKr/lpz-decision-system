import argparse
import logging

import gui

LOG_FORMAT = "%(levelname)s:%(name)s:%(asctime)s:%(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        # Log to file and console
        logging.FileHandler("logs/lpz-nor.log", mode="a"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool for LPZ-NOR Decision System"
    )

    # Add subcommand `run`
    sub_parser = parser.add_subparsers(dest="command")

    run_parser = sub_parser.add_parser("run", help="Run the application GUI")

    args = parser.parse_args()

    if args.command == "run":
        gui.run()
        logger.info("GUI ran successfully!")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
