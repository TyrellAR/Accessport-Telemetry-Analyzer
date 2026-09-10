
from pathlib import Path
import pandas as pd

from backend.app.services.ingestion.normalizer import normalize_telemetry
from backend.app.services.ingestion.parser import parse_log



def test_normalize_real_accessport_log():
    file_path = Path("data/sample/datalog57.csv")

    parsed = parse_log(file_path)
    normalized = normalize_telemetry(parsed["data"])

    #verify row count is preserved
    assert len(normalized) == 1902

    #verify important columns were normalized correctly

    expected_columns = {
        "timestamp",
        "rpm",
        "speed",
        "coolant_temp",
        "boost",
        "boost_ext",
        "afr",
        "intake_temp",
        "throttle_position",
        "fuel_pressure",
        "map",
        "ignition_timing",
        "oil_temp",
    }

    assert expected_columns.issubset(set(normalized.columns))

    #verify numeric columns are actually numeric
    numeric_columns = {
        "timestamp",
        "rpm",
        "speed",
        "coolant_temp",
        "boost",
        "afr",
        "throttle_position",
    }

    for column in numeric_columns:
        assert pd.api.types.is_any_real_numeric_dtype(normalized[column])

        #verify categorical telemetry remains intact
        assert "ac_compressor_sw_on_off" in normalized.columns
        assert normalized["ac_compressor_sw_on_off"].isin(["on","off"]).all()
        

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