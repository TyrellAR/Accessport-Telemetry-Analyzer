from pathlib import Path

import pandas as pd

from backend.app.models.datalog import Datalog
from backend.app.services.ingestion.metadata import DatalogMetadata


def test_datalog_creation():
    metadata = DatalogMetadata(
        accessport_model="AP3-SUB-004",
        firmware_version="1.7.6.0-28208",
        vehicle="2021 USDM WRX MT CCF Gen2",
        reflash_tune="Stage1+BigSF 93 v400.ptm",
        realtime_tune="Stage1+BigSF 93 v400.ptm",
    )

    telemetry = pd.DataFrame(
        {
            "timestamp": [0.0, 0.1, 0.2],
            "rpm": [800, 1000, 1200],
            "speed": [0, 0, 1],
        }
    )

    datalog = Datalog(
        filename="datalog57.csv",
        metadata=metadata,
        telemetry=telemetry,
    )

    assert datalog.filename == "datalog57.csv"
    assert datalog.metadata == metadata
    assert datalog.telemetry.equals(telemetry)


def test_datalog_from_dataframe():
    metadata = DatalogMetadata(
        accessport_model="AP3-SUB-004",
        firmware_version="1.7.6.0-28208",
        vehicle="2021 USDM WRX MT CCF Gen2",
        reflash_tune="Stage1+BigSF 93 v400.ptm",
        realtime_tune="Stage1+BigSF 93 v400.ptm",
    )

    telemetry = pd.DataFrame(
        {
            "timestamp": [0.0, 0.1],
            "rpm": [800, 1000],
        }
    )

    datalog = Datalog.from_dataframe(
        Path("data/sample/datalog57.csv"),
        metadata,
        telemetry,
    )

    assert datalog.filename == "datalog57.csv"
    assert datalog.metadata == metadata
    assert datalog.telemetry.equals(telemetry)