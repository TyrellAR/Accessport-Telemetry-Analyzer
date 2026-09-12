import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.database.models import Base
from backend.app.models.datalog import Datalog
from backend.app.services.ingestion.metadata import DatalogMetadata
from backend.app.services.persistence.datalog import DatalogPersistenceService
from backend.app.database.repositories.datalog import DatalogRepository


def test_persist_datalog_metadata():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    metadata = DatalogMetadata(
        accessport_model="AP3-SUB-004",
        firmware_version="v1.7.6.0-28208",
        vehicle="2021 USDM WRX MT CCF Gen2",
        reflash_tune="Stage1+BigSF 93 v400.ptm",
        realtime_tune="Stage1+BigSF 93 v400.ptm",
    )

    datalog = Datalog(
        filename="test_datalog.csv",
        metadata=metadata,
        telemetry=pd.DataFrame(),
    )

    with Session(engine) as session:
        repository = DatalogRepository(session)
        service = DatalogPersistenceService(repository)
        
        persisted = service.persist(datalog)

        assert persisted.filename == "test_datalog.csv"
        assert persisted.accessport_model == "AP3-SUB-004"
        assert persisted.firmware_version == "v1.7.6.0-28208"
        assert persisted.vehicle == "2021 USDM WRX MT CCF Gen2"
        assert persisted.reflash_tune == "Stage1+BigSF 93 v400.ptm"
        assert persisted.realtime_tune == "Stage1+BigSF 93 v400.ptm"

def test_persist_datalog_telemetry():
    telemetry = pd.DataFrame(
        [
            {
                "timestamp": 0.000,
                "rpm": 850.0,
                "speed": 0.0,
                "coolant_temp": 190.0,
                "boost": -10.5,
            },
            {
                "timestamp": 0.055,
                "rpm": 1200.0,
                "speed": 5.0,
                "coolant_temp": 191.0,
                "boost": -8.2,
            },
        ]
    )

    metadata = DatalogMetadata(
        accessport_model="AP3-SUB-004",
    )

    datalog = Datalog(
        filename="telemetry_test.csv",
        metadata=metadata,
        telemetry=telemetry,
    )

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)
        service = DatalogPersistenceService(repository)

        persisted = service.persist(datalog)

        assert len(persisted.telemetry_samples) == 2
        assert persisted.id is not None

        for sample in persisted.telemetry_samples:
            assert sample.datalog_id == persisted.id

        first_sample = persisted.telemetry_samples[0]
        second_sample = persisted.telemetry_samples[1]

        assert first_sample.timestamp == 0.000
        assert first_sample.rpm == 850.0
        assert first_sample.speed == 0.0
        assert first_sample.coolant_temp == 190.0
        assert first_sample.boost == -10.5

        assert second_sample.timestamp == 0.055
        assert second_sample.rpm == 1200.0
        assert second_sample.speed == 5.0
        assert second_sample.coolant_temp == 191.0
        assert second_sample.boost == -8.2

def test_retrieve_datalog():
    telemetry = pd.DataFrame(
        [
            {
                "timestamp": 0.000,
                "rpm": 850.0,
                "speed": 0.0,
                "boost": -10.5,
            },
            {
                "timestamp": 0.055,
                "rpm": 1200.0,
                "speed": 5.0,
                "boost": -8.2,
            }
        ]
    )

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    metadata = DatalogMetadata(
        accessport_model="AP3-SUB-004",
        firmware_version="v1.7.6.0-28208",
        vehicle="2021 USDM WRX MT CCF Gen2",
        reflash_tune="Stage1+BigSF 93 v400.ptm",
        realtime_tune="Stage1+BigSF 93 v400.ptm",
    )

    datalog = Datalog(
        filename="test_datalog.csv",
        metadata=metadata,
        telemetry=telemetry,
    )

    with Session(engine) as session:
        repository = DatalogRepository(session)
        service = DatalogPersistenceService(repository)

        persisted = service.persist(datalog)

        retrieved = service.retrieve(persisted.id)

        assert retrieved is not None
        assert isinstance(retrieved, Datalog)

        assert retrieved.filename == "test_datalog.csv"

        assert retrieved.metadata.accessport_model == "AP3-SUB-004"
        assert retrieved.metadata.firmware_version == "v1.7.6.0-28208"
        assert retrieved.metadata.vehicle == "2021 USDM WRX MT CCF Gen2"
        assert retrieved.metadata.reflash_tune == "Stage1+BigSF 93 v400.ptm"
        assert retrieved.metadata.realtime_tune == "Stage1+BigSF 93 v400.ptm"

        assert isinstance(retrieved.telemetry, pd.DataFrame)
        assert len(retrieved.telemetry) == 2

        assert retrieved.telemetry.iloc[0]["timestamp"] == 0.000
        assert retrieved.telemetry.iloc[0]["rpm"] == 850.0
        assert retrieved.telemetry.iloc[0]["boost"] == -10.5

        assert retrieved.telemetry.iloc[1]["timestamp"] == 0.055
        assert retrieved.telemetry.iloc[1]["rpm"] == 1200.0
        assert retrieved.telemetry.iloc[1]["boost"] == -8.2

def test_persist_and_retrieve_preserves_all_telemetry_fields():
    telemetry = pd.DataFrame(
        [
            {
                "timestamp": 0.000,
                "rpm": 850.0,
                "speed": 0.0,
                "boost": -10.5,
                "coolant_temp": 190.0,
                "boost_ext": -10.2,
                "afr": 14.7,
                "intake_temp": 85.0,
                "intake_temp_manifold": 90.0,
                "throttle_position": 12.5,
                "fuel_pressure": 43.5,
                "fuel_pressure_target": 43.0,
                "map": 14.2,
                "ignition_timing": 12.5,
                "inj_duty_cycle": 3.5,
                "inj_pulse_width": 1.2,
                "maf_corrected": 2.8,
                "load": 0.35,
                "oil_temp": 185.0,
            }
        ]
    )

    metadata = DatalogMetadata(
        accessport_model="AP3-SUB-004",
    )

    datalog = Datalog(
        filename="round_trip_test.csv",
        metadata=metadata,
        telemetry=telemetry,
    )

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)
        service = DatalogPersistenceService(repository)

        persisted = service.persist(datalog)
        retrieved = service.retrieve(persisted.id)

        assert retrieved is not None
        assert isinstance(retrieved.telemetry, pd.DataFrame)
        assert len(retrieved.telemetry) == 1

        sample = retrieved.telemetry.iloc[0]

        assert sample["timestamp"] == 0.000
        assert sample["rpm"] == 850.0
        assert sample["speed"] == 0.0
        assert sample["boost"] == -10.5
        assert sample["coolant_temp"] == 190.0
        assert sample["boost_ext"] == -10.2
        assert sample["afr"] == 14.7
        assert sample["intake_temp"] == 85.0
        assert sample["intake_temp_manifold"] == 90.0
        assert sample["throttle_position"] == 12.5
        assert sample["fuel_pressure"] == 43.5
        assert sample["fuel_pressure_target"] == 43.0
        assert sample["map"] == 14.2
        assert sample["ignition_timing"] == 12.5
        assert sample["inj_duty_cycle"] == 3.5
        assert sample["inj_pulse_width"] == 1.2
        assert sample["maf_corrected"] == 2.8
        assert sample["load"] == 0.35
        assert sample["oil_temp"] == 185.0

def test_retrieve_datalog_returns_none_when_not_found():
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)

        with Session(engine) as session:
            repository = DatalogRepository(session)
            service = DatalogPersistenceService(repository)

            result = service.retrieve(9999)

            assert result is None



