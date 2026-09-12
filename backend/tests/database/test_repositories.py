from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.database.models import Base, DatalogModel, TelemetrySampleModel
from backend.app.database.repositories.datalog import DatalogRepository


def test_create_datalog():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="datalog57.csv",
        )

        result = repository.create(datalog)

        assert result.id is not None
        assert result.filename == "datalog57.csv"


def test_get_datalog_by_id():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="datalog57.csv",
        )

        repository.create(datalog)

        result = repository.get_by_id(datalog.id)

        assert result is not None
        assert result.id == datalog.id
        assert result.filename == "datalog57.csv"

def test_get_datalog_by_id_returns_none_when_not_found():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        result = repository.get_by_id(999)

        assert result is None

def test_get_all_datalogs():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog_1 = DatalogModel(filename="datalog1.csv")
        datalog_2 = DatalogModel(filename="datalog2.csv")

        repository.create(datalog_1)
        repository.create(datalog_2)

        result = repository.get_all()

        assert len(result) == 2
        assert result[0].filename == "datalog1.csv"
        assert result[1].filename == "datalog2.csv"

def test_delete_datalog():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(filename="datalog57.csv")
        repository.create(datalog)

        result = repository.delete(datalog.id)

        assert result is True
        assert repository.get_by_id(datalog.id) is None


def test_delete_datalog_returns_false_when_not_found():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        result = repository.delete(999)

        assert result is False

def test_delete_datalog_deletes_telemetry_samples():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(filename="datalog57.csv")

        sample_1 = TelemetrySampleModel(
            timestamp=0.0,
            datalog=datalog,
        )
        sample_2 = TelemetrySampleModel(
            timestamp=0.055,
            datalog=datalog,
        )

        repository.create(datalog)
        session.flush()

        assert len(datalog.telemetry_samples) == 2

        repository.delete(datalog.id)

        assert repository.get_by_id(datalog.id) is None
