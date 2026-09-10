from pathlib import Path

import pandas as pd

from backend.app.services.ingestion.normalizer import normalize_telemetry
from backend.app.services.ingestion.parser import parse_log
from backend.app.services.ingestion.validator import validate_telemetry


def test_complete_ingestion_pipeline():
    file_path = Path("data/sample/datalog57.csv")

    #parse raw Accessport log
    parsed = parse_log(file_path)

    assert "metadata" in parsed
    assert "data" in parsed

    #Validate telemetry
    assert validate_telemetry(parsed["data"]) is True

    #normalize telemetry
    normalized = normalize_telemetry(parsed["data"])

    #verify data survived the complete pipeline
    assert isinstance(normalized, pd.DataFrame)
    assert len(normalized) == 1902

    assert "timestamp" in normalized.columns
    assert "rpm" in normalized.columns
    assert "speed" in normalized.columns
    assert "boost" in normalized.columns 

    #verify metadata survived parsing
    assert parsed["metadata"]["ap_info"]



