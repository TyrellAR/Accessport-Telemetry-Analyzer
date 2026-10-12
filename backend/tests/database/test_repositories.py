import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from backend.app.database.models import Base, DatalogModel, TelemetrySampleModel
from backend.app.database.repositories.datalog import DatalogRepository
from backend.app.models.metrics import MetricStatistics, TelemetryMetrics


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

def test_get_datalog_by_id_includes_telemetry():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="telemetry_test.csv",
        )

        repository.create(datalog)

        sample_1 = TelemetrySampleModel(
            datalog=datalog,
            timestamp=0.000,
            rpm=850.0,
            speed=0.0,
            boost=-10.5,
        )

        sample_2 = TelemetrySampleModel(
            datalog=datalog,
            timestamp=0.055,
            rpm=1200.0,
            speed=5.0,
            boost=-8.2,
        )

        repository.add_telemetry_samples(
            [sample_1, sample_2]
        )

        result = repository.get_by_id(datalog.id)

        assert result is not None
        assert len(result.telemetry_samples) == 2

        first_sample = result.telemetry_samples[0]
        second_sample = result.telemetry_samples[1]

        assert first_sample.timestamp == 0.000
        assert first_sample.rpm == 850.0
        assert first_sample.boost == -10.5

        assert second_sample.timestamp == 0.055
        assert second_sample.rpm == 1200.0
        assert second_sample.boost == -8.2

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

        remaining_samples = session.scalars(
            select(TelemetrySampleModel)).all()

        assert remaining_samples == []

def test_get_telemetry_samples():
    """Test retrieving telemetry samples for a datalog."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="telemetry_test.csv",
            vehicle="2021 USDM WRX",
        )

        repository.create(datalog)

        sample_1 = TelemetrySampleModel(
            timestamp=2.0,
            rpm=3000,
            datalog=datalog,
        )

        sample_2 = TelemetrySampleModel(
            timestamp=1.0,
            rpm=2500,
            datalog=datalog,
        )
        repository.add_telemetry_samples(
            [sample_1, sample_2]
        )

        samples = repository.get_telemetry_samples(datalog.id)

        assert len(samples) == 2

        # Samples should be returned in chronological order.
        assert samples[0].timestamp == 1.0
        assert samples[1].timestamp == 2.0

        assert samples[0].rpm == 2500
        assert samples[1].rpm == 3000


def test_get_max_boost():
    """Test retrieve the maximum boost for a given datalog."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="boost_test.csv",
            vehicle="2021 USDM WRX",
        )

        repository.create(datalog)
        session.flush()

        sample_1 = TelemetrySampleModel(
            timestamp=0.0,
            boost=-8.5,
            datalog=datalog,
        )

        sample_2 = TelemetrySampleModel(
            timestamp=1.0,
            boost=12.6,
            datalog=datalog,
        )

        sample_3 = TelemetrySampleModel(
            timestamp=2.0,
            boost=-17.8,
            datalog=datalog,
        )

        repository.add_telemetry_samples(
            [sample_1, sample_2, sample_3]
        )

        repository.get_max_boost(datalog.id)

        max_boost = repository.get_max_boost(datalog.id)

        assert max_boost == 12.6

def test_get_max_boost_isolated_by_datalog_id():
    """Verify boost calculations don't mix different datalogs."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog_1 = DatalogModel(
            filename="boost_test_1.csv",
            vehicle="2021 USDM WRX",
        )

        datalog_2 = DatalogModel(
            filename="boost_test_2.csv",
            vehicle="2021 USDM WRX",
        )

        repository.create(datalog_1)
        repository.create(datalog_2)
        session.flush()

        sample_1 = TelemetrySampleModel(
            timestamp=0.0,
            boost=-8.5,
            datalog=datalog_1,
        )

        sample_2 = TelemetrySampleModel(
            timestamp=1.0,
            boost=12.6,
            datalog=datalog_1,
        )

        sample_3 = TelemetrySampleModel(
            timestamp=2.0,
            boost=-17.8,
            datalog=datalog_2,
        )

        sample_4 = TelemetrySampleModel(
            timestamp=3.0,
            boost=21.4,
            datalog=datalog_2,
        )

        repository.add_telemetry_samples(
            [sample_1, sample_2, sample_3, sample_4]
        )

        max_boost_datalog_1 = repository.get_max_boost(datalog_1.id)
        max_boost_datalog_2 = repository.get_max_boost(datalog_2.id)

        assert max_boost_datalog_1 == 12.6
        assert max_boost_datalog_2 == 21.4


def test_get_max_boost_no_samples():
    """Verify missing telemetry returns None."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="boost_test.csv",
            vehicle="2021 USDM WRX",
        )

        repository.create(datalog)
        session.flush()

        max_boost = repository.get_max_boost(datalog.id)

        assert max_boost is None


def test_get_boost_statistics():

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        datalog_repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="boost_test.csv",
            vehicle="2021 USDM WRX",
        )

        datalog_repository.create(datalog)
        session.flush()

        sample_1 = TelemetrySampleModel(
            timestamp=0.0,
            boost=-8.0,
            datalog=datalog,
        )

        sample_2 = TelemetrySampleModel(
            timestamp=1.0,
            boost=0.0,
            datalog=datalog,
        )

        sample_3 = TelemetrySampleModel(
            timestamp=2.0,
            boost=10.0,
            datalog=datalog,
        )
        sample_4 = TelemetrySampleModel(
            timestamp=3.0,
            boost=18.0,
            datalog=datalog,
        )

        datalog_repository.add_telemetry_samples(
            [sample_1, sample_2, sample_3, sample_4]
        )
        #Call the method to get metrics statistics
        metrics_statistics = datalog_repository.get_boost_statistics(datalog.id)

        #Assertions to check if returned values are of type MetricStatistics and are not None
        assert isinstance(metrics_statistics, MetricStatistics)

        assert metrics_statistics.minimum == -8.0
        assert metrics_statistics.maximum == 18.0
        assert metrics_statistics.average == 5.0


def test_get_boost_statistics_no_samples():
    """Verify that boost statistics return None when no telemetry samples exist."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        datalog_repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="boost_test.csv",
            vehicle="2021 USDM WRX",
        )

        datalog_repository.create(datalog)
        session.flush()

        metrics_statistics = datalog_repository.get_boost_statistics(datalog.id)

        assert isinstance(metrics_statistics, MetricStatistics)
        assert metrics_statistics.minimum is None
        assert metrics_statistics.maximum is None
        assert metrics_statistics.average is None

def test_get_telemetry_statistics():
    """Test retrieving telemetry statistics for a datalog."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="telemetry_test.csv",
            vehicle="2021 USDM WRX",
        )

        repository.create(datalog)
        session.flush()

        sample_1 = TelemetrySampleModel(
            timestamp=0.0,
            boost=-8.0,
            rpm=1000.0,
            afr=14.7,
            coolant_temp=180.0,
            datalog=datalog,
        )

        sample_2 = TelemetrySampleModel(
            timestamp=1.0,
            boost=10.0,
            rpm=3000.0,
            afr=12.0,
            coolant_temp=190.0,
            datalog=datalog,
        )

        sample_3 = TelemetrySampleModel(
            timestamp=2.0,
            boost=18.0,
            rpm=5000.0,
            afr=11.1,
            coolant_temp=200.0,
            datalog=datalog,
        )

        repository.add_telemetry_samples(
            [sample_1, sample_2, sample_3]
        )
        session.flush()

        metrics = repository.get_telemetry_statistics(datalog.id)

        assert isinstance(metrics, TelemetryMetrics)

        assert metrics.boost.minimum == -8.0
        assert metrics.boost.maximum == 18.0
        assert metrics.boost.average == pytest.approx(20.0 / 3.0)

        assert metrics.rpm.minimum == 1000.0
        assert metrics.rpm.maximum == 5000.0
        assert metrics.rpm.average == pytest.approx(9000.0 / 3.0)

        assert metrics.afr.minimum == 11.1
        assert metrics.afr.maximum == 14.7
        assert metrics.afr.average == pytest.approx(37.8 / 3.0)

        assert metrics.coolant_temp.minimum == 180.0
        assert metrics.coolant_temp.maximum == 200.0
        assert metrics.coolant_temp.average == pytest.approx(570.0 / 3.0)

def test_get_telemetry_statistics_no_samples():
    """Verify that telemetry statistics return None when no telemetry samples exist."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog = DatalogModel(
            filename="telemetry_test.csv",
            vehicle="2021 USDM WRX",
        )

        repository.create(datalog)
        session.flush()

        metrics = repository.get_telemetry_statistics(datalog.id)

        assert isinstance(metrics, TelemetryMetrics)

        for channel in (
            metrics.boost,
            metrics.rpm,
            metrics.afr,
            metrics.coolant_temp,
        ):
            assert isinstance(channel, MetricStatistics)
            assert channel.minimum is None
            assert channel.maximum is None
            assert channel.average is None

def test_get_telemetry_statistics_isolated_by_datalog_id():
    """Statistics must only include samples from the requested datalog."""

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DatalogRepository(session)

        datalog_a = DatalogModel(
            filename="telemetry_test_1.csv",
            vehicle="2021 USDM WRX",
        )

        datalog_b = DatalogModel(
            filename="telemetry_test_2.csv",
            vehicle="2021 USDM WRX",
        )

        repository.create(datalog_a)
        repository.create(datalog_b)
        session.flush()

        repository.add_telemetry_samples(
            [
                TelemetrySampleModel(
                    timestamp=0.0,
                    boost=-8.0,
                    rpm=1000.0,
                    afr=14.7,
                    coolant_temp=180.0,
                    datalog=datalog_a,
                ),
                TelemetrySampleModel(
                    timestamp=1.0,
                    boost=10.0,
                    rpm=3000.0,
                    afr=12.0,
                    coolant_temp=190.0,
                    datalog=datalog_b,
                ),
            ]
        )
        session.flush()
        metrics_a = repository.get_telemetry_statistics(datalog_a.id)
        metrics_b = repository.get_telemetry_statistics(datalog_b.id)

        #Datalog A
        assert metrics_a.boost.maximum == -8.0
        assert metrics_a.rpm.maximum == 1000.0
        assert metrics_a.afr.minimum == 14.7
        assert metrics_a.coolant_temp.maximum == 180.0

        #Datalog B
        assert metrics_b.boost.maximum == 10.0
        assert metrics_b.rpm.maximum == 3000.0
        assert metrics_b.afr.minimum == 12.0
        assert metrics_b.coolant_temp.maximum == 190.0
     