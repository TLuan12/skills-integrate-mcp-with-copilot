#!/usr/bin/env python3
"""Import activities from JSON, CSV, XLSX, or Google Sheets URLs."""

import argparse
from pathlib import Path

from src.data_pipeline import DEFAULT_ACTIVITY_FILE, import_activity_file, save_activities


def main() -> None:
    parser = argparse.ArgumentParser(description="Import extracurricular activity data into the app.")
    parser.add_argument("source", help="Source file or URL to import. Supports JSON, CSV, XLSX, and Google Sheets URLs.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_ACTIVITY_FILE),
        help="Destination JSON file for the normalized activities data.",
    )
    args = parser.parse_args()

    imported = import_activity_file(args.source)
    save_activities(imported, Path(args.output))
    print(f"Imported {len(imported)} activities into {args.output}")


if __name__ == "__main__":
    main()
