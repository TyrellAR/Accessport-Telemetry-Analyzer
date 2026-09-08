"""
Parser for COBB Accessport telemetry CSV files.

Reads raw CSV files and extracts metadata + telemetry data.
"""

from pathlib import Path
from typing import TypedDict

import pandas as pd


class ParseError(Exception):
    """Raised when CSV parsing fails."""
    pass


class LogData(TypedDict):
    metadata: dict
    data: pd.DataFrame


def parse_log(file_path: str | Path) -> LogData:
    """
    Parse COBB Accessport CSV and extract metadata + telemetry data.

    Accessport CSVs contain:
    - Header row with column names
    - Data rows with telemetry values
    - Metadata embedded in the last column header as "AP Info:[...]"

    Args:
        file_path: Path to the CSV file

    Returns:
        Dictionary with 'metadata' and 'data' (DataFrame)

    Raises:
        FileNotFoundError: If file does not exist
        ParseError: If file cannot be parsed
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    try:
        # Read CSV with Windows-1252 encoding (COBB standard)
        df = pd.read_csv(path, encoding="windows-1252")
    except UnicodeDecodeError:
        # Fallback to latin-1 if windows-1252 fails
        try:
            df = pd.read_csv(path, encoding="latin-1")
        except Exception as e:
            raise ParseError(f"Failed to parse CSV: {e}") from e
    except Exception as e:
        raise ParseError(f"Failed to read CSV: {e}") from e

    if df.empty:
        raise ParseError("CSV file is empty")

    # Extract metadata from column headers
    metadata = _extract_metadata(df)

    return {
        "metadata": metadata,
        "data": df,
    }


def _extract_metadata(df: pd.DataFrame) -> dict:
    """
    Extract metadata from CSV column headers.

    COBB Accessport includes metadata in the last column header
    formatted as "AP Info:[...]"

    Args:
        df: DataFrame with column headers from CSV

    Returns:
        Dictionary with extracted metadata
    """
    metadata = {}

    # Look for "AP Info" in column headers
    for col in df.columns:
        if "AP Info" in str(col):
            ap_info = str(col)
            # Extract the content between [ and ]
            if "[" in ap_info and "]" in ap_info:
                content = ap_info[ap_info.index("[") : ap_info.rindex("]") + 1]
                metadata["ap_info"] = content
            break

    return metadata


