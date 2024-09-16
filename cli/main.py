import argparse

import gui


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
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
