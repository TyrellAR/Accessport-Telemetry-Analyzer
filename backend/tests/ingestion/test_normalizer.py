import pandas as pd

from backend.app.services.ingestion.normalizer import normalize_telemetry


def test_normalize_column_names():
    df = pd.DataFrame({
            "Time (sec)": [0.0, 0.1],
            "RPM (RPM)": [1000, 1500],
            "Vehicle Speed (mph)": [0, 5],
            "Coolant Temp (F)": [180, 181],
            "Boost (psi)": [0.5, 1.0],
            "AF Sens 1 Ratio (AFR)": [14.7, 14.5],
            "Throttle Pos (%)": [10, 20],
    })

    result = normalize_telemetry(df)

    expected_columns = {
        "timestamp",
        "rpm",
        "speed",
        "coolant_temp",
        "boost",
        "afr",
        "throttle_position",
    }

    assert set(result.columns) == expected_columns

def test_normalize_numeric_columns():
    df = pd.DataFrame({
        "Time (sec)": ["0.0", "0.1"],
        "RPM (RPM)": ["1000", "1500"],
        "Boost (psi)": ["0.5", "1.0"],
        "Coolant Temp (F)": ["180", "181"],
    })

    result = normalize_telemetry(df)

    assert pd.api.types.is_numeric_dtype(result["timestamp"])
    assert pd.api.types.is_numeric_dtype(result["rpm"])
    assert pd.api.types.is_numeric_dtype(result["boost"])
    assert pd.api.types.is_numeric_dtype(result["coolant_temp"])


def test_normalize_preserves_non_numeric_columns():
    df = pd.DataFrame({
        "Time (sec)": ["0.0", "0.1"],
        "RPM (RPM)": ["1000", "1500"],
        "Vehicle Speed (mph)": ["0", "5"],
        "Coolant Temp (F)": ["180", "181"],
        "AC Compressor Sw (on/off)": ["off", "on"],
    })

    result = normalize_telemetry(df)

    assert result["ac_compressor_sw_on_off"].tolist() == ["off", "on"]