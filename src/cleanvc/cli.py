import argparse
import sys
from .cleaner import CSVCleaner
from . import __version__


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="cleanvc",
        description="Fast, zero-dependency CSV header and whitespace sanitizer.",
    )
    parser.add_argument("input", help="Path to input messy CSV file")
    parser.add_argument(
        "-o",
        "--output",
        help="Path for cleaned CSV output (default: cleaned_<filename>.csv)",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        default=",",
        help="CSV delimiter character (default: ',')",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args(argv)

    cleaner = CSVCleaner(delimiter=args.delimiter)
    try:
        out_path = cleaner.process_file(args.input, args.output)
        print(f"Successfully cleaned: {out_path}")
        return 0
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

