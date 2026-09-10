"""
Validator for COBB Accessport telemetry data.

Validates data quality and required columns.
"""

import pandas as pd


class ValidationError(Exception):
    """Raised when telemetry data validation fails."""
    pass


# Required telemetry columns that must be present in every valid Accessport log
REQUIRED_COLUMNS = {
    "time (sec)",
    "rpm (rpm)",
    "vehicle speed (mph)",
    "coolant temp (f)",
}

# Optional but commonly analyzed columns
OPTIONAL_COLUMNS = {
    "boost (psi)",
    "boost extended (psi)",
    "af sens 1 ratio (afr)",
    "intake temp (f)",
    "throttle pos (%)",
    "fuel pressure (psi)",
    "man abs press (psi)",
    "ignition timing (°)",
}

NUMERIC_COLUMNS = {
    "time (sec)",
    "rpm (rpm)",
    "vehicle speed (mph)",
    "coolant temp (f)",
    "boost (psi)",
    "boost extended (psi)",
    "af sens 1 ratio (afr)",
    "intake temp (f)",
    "throttle pos (%)",
    "fuel pressure (psi)",
    "man abs press (psi)",
    "ignition timing (°)",
}


def validate_telemetry(df: pd.DataFrame) -> bool:
    """
    Validate telemetry DataFrame for data quality and required columns.

    Args:
        df: DataFrame from parser.parse_log()

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    # Check if dataframe is empty
    if df.empty:
        raise ValidationError("Telemetry data is empty")

    # Check for minimum row count
    if len(df) < 10:
        raise ValidationError(f"Telemetry has only {len(df)} rows, need at least 10")

    # Validate required columns exist
    _validate_required_columns(df)

    # Validate data integrity
    _validate_data_integrity(df)

    # Validate numeric columns
    _validate_numeric_columns(df)

    return True


def _validate_required_columns(df: pd.DataFrame) -> None:
    """
    Check that all required columns exist in the dataframe.

    Column names are case-insensitive.

    Args:
        df: DataFrame to validate

    Raises:
        ValidationError: If required columns are missing
    """
    # Convert column names to lowercase for comparison
    df_columns_lower = {col.lower() for col in df.columns}

    # Find missing required columns
    missing = REQUIRED_COLUMNS - df_columns_lower

    if missing:
        raise ValidationError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )


def _validate_data_integrity(df: pd.DataFrame) -> None:
    """
    Validate data values and integrity.

    Checks for:
    - NaN values in critical columns

    Raises:
        ValidationError: If data integrity issues found
    """

    # check for completely empty rows
    empty_rows = df.isna().all(axis=1).sum()

    if empty_rows > 0:
        raise ValidationError(
            f"Found {empty_rows} completely empty rows"
         )

    critical_columns = {
        "time (sec)",
        "rpm (rpm)",
        "vehicle speed (mph)",
        "coolant temp (f)",
    }

    df_columns_by_lower = {
        col.lower(): col for col in df.columns
    }

    # Check critical columns for excessive NaN values
    # (allow some missing data, but not too much)
    for column in critical_columns:
        actual_column = df_columns_by_lower[column]

        nan_count = df[actual_column].isna().sum()
        nan_percentage = (nan_count / len(df)) * 100

        if nan_percentage > 50:
            raise ValidationError(
                f"Column '{actual_column}' has "
                f"{nan_percentage:.1f}% missing values"
            )


def _validate_numeric_columns(df: pd.DataFrame) -> None:
    """
    Validate that numeric telemetry columns contain valid numeric values.

    Args:
        df: DataFrame to validate

    Raises:
        ValidationError: If a numeric column contains invalid values
    """

    numeric_columns = {
        "time (sec)",
        "rpm (rpm)",
        "vehicle speed (mph)",
        "coolant temp (f)",
        "boost (psi)",
        "boost extended (psi)",
        "af sens 1 ratio (afr)",
        "intake temp (f)",
        "throttle pos (%)",
        "fuel pressure (psi)",
        "man abs press (psi)",
        "ignition timing (°)",
    }

    df_columns_by_lower = {
        col.lower(): col for col in df.columns
    }

    for column in numeric_columns:
        if column not in df_columns_by_lower:
            continue

        actual_column = df_columns_by_lower[column]

        converted = pd.to_numeric(
            df[actual_column],
            errors="coerce",
        )

        invalid_values = (
            converted.isna() &
            df[actual_column].notna()
        )

        if invalid_values.any():
            raise ValidationError(
                f"Column '{actual_column}' contains invalid numeric values"
            )