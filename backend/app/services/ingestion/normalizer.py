"""
Normalizer for COBB Accessport telemetry data.

Standardizes column names, types, and formats for consistent processing.
"""

import pandas as pd


class NormalizationError(Exception):
    """Raised when normalization fails."""
    pass


# Map raw Accessport column names to standardized names
# Use this to normalize variations in column naming
COLUMN_NAME_MAPPING = {
    "time (sec)": "timestamp",
    "rpm (rpm)": "rpm",
    "vehicle speed (mph)": "speed",
    "coolant temp (f)": "coolant_temp",
    "boost (psi)": "boost",
    "boost extended (psi)": "boost_ext",
    "af sens 1 ratio (afr)": "afr",
    "intake temp (f)": "intake_temp",
    "intake temp manifold (f)": "intake_temp_manifold",
    "throttle pos (%)": "throttle_position",
    "fuel pressure (psi)": "fuel_pressure",
    "fuel pressure target (psi)": "fuel_pressure_target",
    "man abs press (psi)": "map",
    "ignition timing (°)": "ignition_timing",
    "inj duty cycle (%)": "inj_duty_cycle",
    "inj pw (ms)": "inj_pulse_width",
    "maf corr final (g/s)": "maf_corrected",
    "calculated load (g/rev)": "load",
    "oil temp (f)": "oil_temp",
}

NUMERIC_COLUMNS = {
    "timestamp",
    "rpm",
    "speed",
    "coolant_temp",
    "boost",
    "boost_ext",
    "afr",
    "intake_temp",
    "intake_temp_manifold",
    "throttle_position",
    "fuel_pressure",
    "fuel_pressure_target",
    "map",
    "ignition_timing",
    "inj_duty_cycle",
    "inj_pulse_width",
    "maf_corrected",
    "load",
    "oil_temp",
}


def normalize_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize telemetry DataFrame.

    Steps:
    1. Standardize column names (lowercase, remove units, use underscores)
    2. Coerce numeric columns to float
    3. Handle missing values

    Args:
        df: DataFrame from parser.parse_log() that passed validator

    Returns:
        Normalized DataFrame

    Raises:
        NormalizationError: If normalization fails
    """
    try:
        df = df.copy()  # Don't modify original

        # Normalize column names
        df = _normalize_column_names(df)

        # Coerce numeric columns
        df = _coerce_numeric_columns(df)

        return df

    except Exception as e:
        raise NormalizationError(f"Normalization failed: {e}") from e


def _normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names.

    Converts column names to lowercase, removes special characters,
    and applies the standardized mapping.

    Args:
        df: DataFrame with raw column names

    Returns:
        DataFrame with normalized column names
    """
    # Create rename mapping from raw to normalized names
    rename_map = {}

    for raw_col in df.columns:
        raw_col_lower = raw_col.lower().strip()

        # Check if we have a mapping for this column
        if raw_col_lower in COLUMN_NAME_MAPPING:
            normalized = COLUMN_NAME_MAPPING[raw_col_lower]
        else:
            # If no mapping, just lowercase and use underscores
            normalized = (raw_col_lower
                          .replace(" ", "_")
                          .replace("-", "_")
                          .replace("/", "_")
                          .replace(")", "")
                          .replace("°", "")
                          .replace("/", "_")
                          )
            normalized = normalized.replace("(", "").replace(")", "").replace("°", "")
        rename_map[raw_col] = normalized

    return df.rename(columns=rename_map)


def _coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric columns to float type.

    Attempts to convert all columns except 'timestamp' to numeric.
    Non-numeric values are converted to NaN.

    Args:
        df: DataFrame with normalized column names

    Returns:
        DataFrame with coerced numeric columns
    """
    # Skip these columns (they are not numeric)
    #skip_columns = {"timestamp", "gear_position"}

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            continue

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",  # Non-numeric values become NAN
        )
    return df


def get_column_mapping() -> dict:
    """
    Get the column name mapping for reference.

    Returns:
        Dictionary of raw_name -> normalized_name mappings
    """
    return COLUMN_NAME_MAPPING.copy()
