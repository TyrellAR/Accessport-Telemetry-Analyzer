from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.database.models import (
    Base,
    DatalogModel,
    TelemetrySampleModel,
)


def test_datalog_model_creation():
    datalog = DatalogModel(
        filename="datalog57.csv",
        accessport_model="AP3-SUB-004",
        firmware_version="1.7.6.0-28208",
        vehicle="2021 USDM WRX MT CCF Gen2",
        reflash_tune="Stage1+BigSF 93 v400.ptm",
        realtime_tune="Stage1+BigSF 93 v400.ptm",
    )

    assert datalog.filename == "datalog57.csv"
    assert datalog.accessport_model == "AP3-SUB-004"
    assert datalog.vehicle == "2021 USDM WRX MT CCF Gen2"


def test_telemetry_sample_creation():
    sample = TelemetrySampleModel(
        timestamp=12.5,
        rpm=3500,
        speed=45,
        boost=12.3,
        afr=11.2,
        coolant_temp=190,
    )

    assert sample.timestamp == 12.5
    assert sample.rpm == 3500
    assert sample.speed == 45
    assert sample.boost == 12.3
    assert sample.afr == 11.2


def test_datalog_telemetry_relationship():
    datalog = DatalogModel(
        filename="datalog57.csv",
    )

    sample = TelemetrySampleModel(
        timestamp=1.0,
        rpm=1000,
    )

    datalog.telemetry_samples.append(sample)

    assert len(datalog.telemetry_samples) == 1
    assert datalog.telemetry_samples[0] is sample
    assert sample.datalog is datalog


def test_datalog_created_at_has_default():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        datalog = DatalogModel(filename="datalog57.csv")

        session.add(datalog)
        session.flush()

        assert datalog.created_at is not None


def test_datalog_starts_with_no_telemetry_samples():
    datalog = DatalogModel(filename="datalog57.csv")

    assert datalog.telemetry_samples == []


def test_telemetry_sample_datalog_id_defaults_to_none():
    sample = TelemetrySampleModel(
        timestamp=12.5,
    )

    assert sample.datalog_id is None

def test_datalog_can_have_multiple_telemetry_samples():
    datalog = DatalogModel(filename="datalog57.csv")

    sample_1 = TelemetrySampleModel(timestamp=1.0)
    sample_2 = TelemetrySampleModel(timestamp=2.0)
    sample_3 = TelemetrySampleModel(timestamp=3.0)

    datalog.telemetry_samples.extend(
        [sample_1, sample_2, sample_3]
    )

    assert len(datalog.telemetry_samples) == 3
    assert sample_1.datalog is datalog
    assert sample_2.datalog is datalog
    assert sample_3.datalog is datalog