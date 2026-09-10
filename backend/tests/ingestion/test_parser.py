import pandas as pd
import pytest

from backend.app.services.ingestion.parser import ParseError, parse_log


def test_parse_log():
    result = parse_log("data/sample/datalog57.csv")

    assert "metadata" in result
    assert "data" in result

    assert isinstance(result["data"], pd.DataFrame)
    assert not result["data"].empty


def test_parse_log_extracts_ap_info():
    result = parse_log("data/sample/datalog57.csv")

    metadata = result["metadata"]

    assert "ap_info" in metadata
    assert metadata["ap_info"].startswith("[")
    assert metadata["ap_info"].endswith("]")


def test_parse_log_preserves_telemetry_columns():
    result = parse_log("data/sample/datalog57.csv")

    data = result["data"]

    assert len(data.columns) == 49


def test_parse_log_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_log("data/sample/does_not_exist.csv")


def test_parse_log_empty_csv(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")

    with pytest.raises(ParseError):
        parse_log(empty_file)


def test_parse_log_row_count():
    result = parse_log("data/sample/datalog57.csv")

    data = result["data"]

    assert len(data) == 1902

def test_parse_log_contains_expected_columns():
    result = parse_log("data/sample/datalog57.csv")

    data = result["data"]

    expected_columns = [
        "Time (sec)",
        "RPM (RPM)",
        "Boost (psi)",
    ]

    for column in expected_columns:
        assert column in data.columns

def test_parse_log_without_ap_info(tmp_path):
    csv_file = tmp_path / "no_ap_info.csv"

    csv_file.write_text(
        "Time,RPM,Speed\n"
        "0.0,1000,0\n"
        "0.1,1100,1\n"
    )

    result = parse_log(csv_file)

    assert result["metadata"] == {}
    assert not result["data"].empty