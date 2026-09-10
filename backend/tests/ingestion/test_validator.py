import pandas as pd
import pytest

from backend.app.services.ingestion.validator import (
    ValidationError,
    validate_telemetry,
)


def test_validate_valid_telemetry():
    df = pd.DataFrame({
        "Time (sec)": [0.1 * i for i in range(10)],
        "RPM (RPM)": [1000 + (100 * i) for i in range(10)],
        "Vehicle Speed (mph)": [i for i in range(10)],
        "Coolant Temp (F)": [180 + i for i in range(10)],
    })

    result = validate_telemetry(df)

    assert result is True


def test_validate_empty_dataframe():
    df = pd.DataFrame()

    with pytest.raises(ValidationError, match="Telemetry data is empty"):
        validate_telemetry(df)

def test_validate_too_few_rows():
    df = pd.DataFrame({
        "Time (sec)": [0.0, 0.1],
        "RPM (RPM)": [1000, 1500],
        "Vehicle Speed (mph)": [0, 5],
        "Coolant Temp (F)": [180, 181],
    })

    with pytest.raises(
        ValidationError,
        match="Telemetry has only 2 rows, need at least 10",
    ):
        validate_telemetry(df)


def test_validate_missing_required_column():
    df = pd.DataFrame({
        "Time (sec)": [0.0] * 10,
        "RPM (RPM)": [1000] * 10,
        "Vehicle Speed (mph)": [0] * 10,
    })

    with pytest.raises(ValidationError, match="Missing required columns"):
        validate_telemetry(df)


def test_validate_required_columns_case_insensitive():
    df = pd.DataFrame({
        "TIME (SEC)": [0.0] * 10,
        "RPM (RPM)": [1000] * 10,
        "VEHICLE SPEED (MPH)": [0] * 10,
        "COOLANT TEMP (F)": [180] * 10,
    })

    result = validate_telemetry(df)

    assert result is True


def test_validate_completely_empty_rows():
    df = pd.DataFrame({
        "Time (sec)": [0.0, 0.1] + [None] * 8,
        "RPM (RPM)": [1000, 1500] + [None] * 8,
        "Vehicle Speed (mph)": [0, 5] + [None] * 8,
        "Coolant Temp (F)": [180, 181] + [None] * 8,
    })

    with pytest.raises(
        ValidationError,
        match="completely empty rows",
    ):
        validate_telemetry(df)


def test_validate_excessive_missing_values():
    df = pd.DataFrame({
        "Time (sec)": [None] * 6 + [0.6, 0.7, 0.8, 0.9],
        "RPM (RPM)": [1000] * 10,
        "Vehicle Speed (mph)": [0] * 10,
        "Coolant Temp (F)": [180] * 10,
    })

    with pytest.raises(
        ValidationError,
        match="Time \\(sec\\).*60.0% missing values",
    ):
        validate_telemetry(df)


def test_validate_numeric_columns():
      df = pd.DataFrame({
        "Time (sec)": [0.1 * i for i in range(10)],
        "RPM (RPM)": [1000 + (100 * i) for i in range(10)],
        "Vehicle Speed (mph)": [i for i in range(10)],
        "Coolant Temp (F)": [180 + i for i in range(10)],
        })

      result = validate_telemetry(df)
      assert result is True


def test_validate_invalid_numeric_value():
    df = pd.DataFrame({
        "Time (sec)": [0.1] * 10,
        "RPM (RPM)": ["1000"] * 10,
        "Vehicle Speed (mph)": [0] * 10,
        "Coolant Temp (F)": [180] * 10,
    })

    df.loc[5, "RPM (RPM)"] = "invalid"

    with pytest.raises(
        ValidationError,
        match="Column 'RPM \\(RPM\\)' contains invalid numeric values",
    ):
        validate_telemetry(df)