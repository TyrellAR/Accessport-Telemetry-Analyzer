from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
import pytest

from backend.app.database.models import Base, DatalogModel, TelemetrySampleModel
from backend.app.database.database import get_db
from backend.app.main import app

@pytest.fixture
def test_db():
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        )
    Base.metadata.create_all(test_engine)

    yield test_engine

    test_engine.dispose()

def override_get_db(test_db):
    def _get_db():
        with Session(test_db) as session:
            yield session

    return _get_db

client = TestClient(app)

def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_datalogs(test_db):
    app.dependency_overrides[get_db] = override_get_db(test_db)
    response = client.get("/api/logs")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()

def test_get_datalogs_returns_datalogs(test_db):
    app.dependency_overrides[get_db] = override_get_db(test_db)

    with Session(test_db) as session:
        datalog_1 = DatalogModel(
            filename="datalog1.csv",
            vehicle="2021 USDM WRX",
        )
        datalog_2 = DatalogModel(
            filename="datalog2.csv",
            vehicle="2021 USDM WRX",
        )
        session.add_all([datalog_1, datalog_2])
        session.commit()

    response = client.get("/api/logs")

    assert response.status_code == 200

    data = response.json()

    assert len(data)  == 2
    assert data[0]["filename"] == "datalog1.csv"
    assert data[0]["vehicle"] == "2021 USDM WRX"
    assert data[1]["filename"] == "datalog2.csv"
    assert data[1]["vehicle"] == "2021 USDM WRX"

    app.dependency_overrides.clear()

def test_get_datalog_by_id(test_db):
    app.dependency_overrides[get_db] = override_get_db(test_db)

    with Session(test_db) as session:
        datalog = DatalogModel(
            filename="datalog3.csv",
            vehicle="2021 USDM WRX",
        )
        session.add(datalog)
        session.commit()
        datalog_id = datalog.id

    response = client.get(f"/api/logs/{datalog_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == datalog_id
    assert data["filename"] == "datalog3.csv"
    assert data["vehicle"] == "2021 USDM WRX"

    app.dependency_overrides.clear()

def test_get_datalog_by_id_not_found(test_db):
    app.dependency_overrides[get_db] = override_get_db(test_db)

    response = client.get("/api/logs/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Datalog not found"}

    app.dependency_overrides.clear()

def test_get_datalog_telemetry(test_db):
    """Test retrieving telemetry samples for a datalog."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="telemetry_test.csv",
            vehicle="2021 USDM WRX",
        )

        sample_1 = TelemetrySampleModel(
            timestamp=1.0,
            rpm=2500,
            speed=30,
            coolant_temp=190,
            boost=12.5,
            datalog=datalog,
        )

        sample_2 = TelemetrySampleModel(
            timestamp=2.0,
            rpm=3000,
            speed=35,
            coolant_temp=191,
            boost=14.0,
            datalog=datalog,
        )

        with Session(test_db) as session:
            session.add(datalog)
            session.add_all([sample_1, sample_2])
            session.commit()

            datalog_id = datalog.id

        with TestClient(app) as client:
            response = client.get(
                f"/api/logs/{datalog_id}/telemetry"
            )

            assert response.status_code == 200

            data = response.json()

            assert len(data) == 2

            assert data[0]["timestamp"] == 1.0
            assert data[0]["rpm"] == 2500
            assert data[0]["speed"] == 30
            assert data[0]["coolant_temp"] == 190
            assert data[0]["boost"] == 12.5

            assert data[1]["timestamp"] == 2.0
            assert data[1]["rpm"] == 3000
            assert data[1]["speed"] == 35
            assert data[1]["coolant_temp"] == 191
            assert data[1]["boost"] == 14.0

    finally:
        app.dependency_overrides.clear()

def test_get_datalog_telemetry_not_found(test_db):
    """Test retrieving telemetry for a nonexisting datalog."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        with TestClient(app) as client:
            response = client.get(
                "/api/logs/999/telemetry"
            )

            assert response.status_code == 404
            assert response.json()["detail"] == "Datalog not found"

    finally:
        app.dependency_overrides.clear()


def test_delete_datalog(test_db):
        app.dependency_overrides[get_db] = override_get_db(test_db)

        with TestClient(app) as client:
            datalog = DatalogModel(
                filename="delete_test.csv",
                accessport_model="AP3-SUB-004",
                firmware_version="1.7.6.0-28208",
                vehicle="2021 US WRX",
            )

            with Session(test_db) as session:
                session.add(datalog)
                session.commit()
                datalog_id = datalog.id

            response = client.delete(f"/api/logs/{datalog_id}")

            assert response.status_code == 200
            assert response.json() == {"detail": "Datalog deleted"}

            response = client.get(f"/api/logs/{datalog_id}")

            assert response.status_code == 404

def test_delete_datalog_not_found(test_db):
    app.dependency_overrides[get_db] = override_get_db(test_db)

    with TestClient(app) as client:
        response = client.delete("/api/logs/999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Datalog not found"}

def test_delete_datalog_cascades_telemetry_samples(test_db):
    app.dependency_overrides[get_db] = override_get_db(test_db)

    with TestClient(app) as client:
        datalog = DatalogModel(
            filename="cascade_test.csv",
            accessport_model="AP3-SUB-004",
            firmware_version="1.7.6.0-28208",
            vehicle="2021 USDM WRX",
        )

        sample_1 = TelemetrySampleModel(
            timestamp=1.0,
            rpm=2500,
            speed=30,
            datalog=datalog,
        )

        sample_2 = TelemetrySampleModel(
            timestamp=2.0,
            rpm=3000,
            speed=35,
            datalog=datalog,
        )

        with Session(test_db) as session:
            session.add(datalog)
            session.add_all([sample_1, sample_2])
            session.commit()

            datalog_id = datalog.id
            sample_1_id = sample_1.id
            sample_2_id = sample_2.id

        response = client.delete(f"/api/logs/{datalog_id}")

        assert response.status_code == 200

        with Session(test_db) as session:
            deleted_datalog = session.get(
                DatalogModel,
                datalog_id,
            )

            deleted_sample_1 = session.get(
                TelemetrySampleModel,
                sample_1_id,
            )
            deleted_sample_2 = session.get(
                TelemetrySampleModel,
                sample_2_id,
            )

        assert deleted_datalog is None
        assert deleted_sample_1 is None
        assert deleted_sample_2 is None

def test_upload_datalog(test_db):
    """Test uploading a valid COBB Accessport datalog."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        with TestClient(app) as client:
            with open("data/sample/datalog57.csv", "rb") as file:
                response = client.post(
                    "/api/logs/upload",
                    files={
                        "file": (
                            "datalog57.csv",
                            file,
                            "text/csv",
                        )
                    },
                )

                assert response.status_code == 200

                data = response.json()

                assert data["filename"] == "datalog57.csv"
                assert data["accessport_model"] == "AP3-SUB-004"
                assert data["vehicle"] == "2021 USDM WRX MT CCF Gen2"

    finally:
        app.dependency_overrides.clear()

def test_upload_empty_csv_returns_422(test_db):
    """Test uploading an empty CSV returns a 422 error."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/logs/upload",
                files={
                    "file": (
                        "empty.csv",
                        "time (sec), RPM (RPM), Vehicle Speed (mph), Coolant Temp (F)\n",
                        "text/csv",
                    ),
                },
            )

            assert response.status_code == 422
            assert response.json()["detail"] == "CSV file is empty"

    finally:
        app.dependency_overrides.clear()

def test_upload_insufficient_datalog_returns_422(test_db):
    """Test uploading a CSV with too few telemetry rows returns 422."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/logs/upload",
                files={
                    "file": (
                        "insufficient.csv",
                        (
                            "time (sec), (RPM), Vehicle Speed (mph), Coolant Temp (F)\n"
                            "0,800,0,190\n"

                        ),
                        "test/csv",
                    ),
                },
            )

            assert response.status_code == 422
            assert response.json()["detail"] == (
                "Telemetry has only 1 rows, need at least 10"
            )

    finally:
        app.dependency_overrides.clear()

def test_upload_invalid_file_type_returns_422(test_db):
    """Test that uploading a non-CSV file return 422."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/logs/upload",
                files={
                    "file": (
                        "wrong_file_type.txt",
                        (
                            "time (sec),RPM (RPM),Vehicle Speed (mph),Coolant Temp (F)\n"
                            "0,800,0,190\n"
                            "1,900,1,190\n"
                            "2,1000,2,191\n"
                            "3,1100,3,191\n"
                            "4,1200,4,192\n"
                            "5,1300,5,192\n"
                            "6,1400,6,193\n"
                            "7,1500,7,193\n"
                            "8,1600,8,194\n"
                            "9,1700,9,194\n"
                        ),
                        "text/plain",

                    ),

                },
            )

            assert response.status_code == 422
            assert response.json()["detail"] == "The program only accepts .csv files"

    finally:
        app.dependency_overrides.clear()

def test_get_datalog_telemetry_pagination(test_db):
    """Test retrieving telemetry samples for a datalog with pagination."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="telemetry_pagination_test.csv",
            vehicle="2021 USDM WRX",
        )

        samples = [
                    TelemetrySampleModel(
                        timestamp=float(i),
                        rpm=2000 + i * 100,
                        speed=20 + i,
                        coolant_temp=190 + i,
                        boost=10.0 + i * 0.5,
                        datalog=datalog,
                    )
                    for i in range(1, 21)
                ]
        
        with Session(test_db) as session:
                # Add a datalog and 20 telemetry samples to the test database
                session.add(datalog)
                session.add_all(samples)
                session.commit()

                datalog_id = datalog.id

        with TestClient(app) as client:
            # testClient communicaties with the FastAPI app, which uses the overridden get_db dependency to use the test database
            response = client.get(
                f"/api/logs/{datalog_id}/telemetry?limit=2&offset=2"
            )
            assert response.status_code == 200

            data = response.json()

            assert len(data) == 2
            assert data[0]["timestamp"] == 3.0
            assert data[1]["timestamp"] == 4.0

    finally: 
        app.dependency_overrides.clear()

def test_get_datalog_telemetry_invalid_limit(test_db):
    """Reject telemetry requests with an invalid limit."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="telemetry_invalid_limit_test.csv",
            vehicle="2021 USDM WRX",

        )
        with Session(test_db) as session: 
            #establish a datalog in the test database
            session.add(datalog)
            session.commit()

            datalog_id = datalog.id

        with TestClient(app) as client:
            #testClient communicates with the FastAPI app, which uses the overridden get_db dependency to use the test database
            response = client.get(
                #get telemetry samples for the datalog with an invalid limit of 0 from api route base + /api/logs/ + datalog id
                f"/api/logs/{datalog_id}/telemetry?limit=0"
            )

            # assert unprocessable api or json response
            assert response.status_code == 422
            errors = response.json()["detail"]
            assert len(errors) > 0
            assert errors[0]["loc"] == ["query", "limit"]
            assert errors[0]["type"] == "greater_than_equal"

    finally: # close the dependency override to avoid affecting other tests
        app.dependency_overrides.clear()


def test_get_datalog_telemetry_limit_exceeds_maximum(test_db):
    """Reject telemetry requests with a limit that exceeds the maximum allowed."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="telemetry_exceed_limit_test.csv",
            vehicle="2021 USDM WRX",
        )
        with Session(test_db) as session:
            # establish a datalog in the test database
            session.add(datalog)
            session.commit()

            datalog_id = datalog.id

        with TestClient(app) as client:
            # testClient communicates with the FastAPI app, which uses the overridden get_db dependency to use the test database
            response = client.get(
                # get telemetry samples for the datalog with a limit that exceeds the maximum allowed (1000) from api route base + /api/logs/ + datalog id
                f"/api/logs/{datalog_id}/telemetry?limit=1001"
            )

            # assert unprocessable api or json response
            assert response.status_code == 422
            errors = response.json()["detail"]
            assert len(errors) > 0
            assert errors[0]["loc"] == ["query", "limit"]
            assert errors[0]["type"] == "less_than_equal"

    finally:  # close the dependency override to avoid affecting other tests
        app.dependency_overrides.clear()


def test_get_datalog_telemetry_invalid_offset(test_db):
    """Reject telemetry request with an invalid offset."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="telemetry_invalid_offset_test.csv",
            vehicle="2021 USDM WRX",
        )

        with Session(test_db) as session:
            session.add(datalog)
            session.commit()

            datalog_id = datalog.id

        with TestClient(app) as client:
            response = client.get(
                f"/api/logs/{datalog_id}/telemetry?offset=-1"
            )

            assert response.status_code == 422
            errors = response.json()["detail"]
            assert len(errors) > 0
            assert errors[0]["loc"] == ["query", "offset"]
            assert errors[0]["type"] == "greater_than_equal"

    finally:
        app.dependency_overrides.clear()

def test_get_datalog_telemetry_offset_beyond_records(test_db):
    """Test retrieving telemetry samples with an offset beyond the valid range of records """

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="telemetry_offset_beyond_records_test.csv",
            vehicle="2021 USDM WRX",
        )

        samples = [
            TelemetrySampleModel(
                timestamp=float(i),
                rpm=2000 + i * 100,
                speed=20 + i,
                coolant_temp=190 + i,
                boost=10.0 + i * 0.5,
                datalog=datalog,
            )
            for i in range(1, 6)  # Create 5 telemetry samples
        ]

        with Session(test_db) as session:
            # Add a datalog and 5 telemetry samples to the test database
            session.add(datalog)
            session.add_all(samples)
            session.commit()

            datalog_id = datalog.id

        with TestClient(app) as client:
            # Request telemetry samples with an offset beyond the number of available records
            response = client.get(
                f"/api/logs/{datalog_id}/telemetry?limit=2&offset=10"
            )

            assert response.status_code == 200

            assert response.json() == []  # Expecting an empty list since the offset is beyond the available records

    finally:
        app.dependency_overrides.clear()

def test_get_datalog_metrics(test_db):
    """Test retrieving aggregated telemetry metrics for a datalog."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="metrics_test.csv",
            vehicle="2021 USDM WRX",
        )

        sample_1 = TelemetrySampleModel(
            timestamp=1.0,
            rpm=2000,
            speed=30,
            boost=10.0,
            afr=14.0,
            coolant_temp=190,
            datalog=datalog,
        )
        sample_2 = TelemetrySampleModel(
            timestamp=2.0,
            rpm=4000,
            speed=50,
            boost=20.0,
            afr=12.0,
            coolant_temp=200,
            datalog=datalog,
       )

        with Session(test_db) as session:
            session.add(datalog)
            session.add_all([sample_1, sample_2])
            session.commit()

            datalog_id = datalog.id

        with TestClient(app) as client:
            response = client.get(
                f"/api/logs/{datalog_id}/metrics"
            )

            assert response.status_code == 200

            data = response.json()

            assert data["boost"] == {
                "minimum": 10.0,
                "maximum": 20.0,
                "average": 15.0,
            }

            assert data["rpm"] == {
                "minimum": 2000.0,
                "maximum": 4000.0,
                "average": 3000.0,
            }

            assert data["afr"] == {
                "minimum": 12.0,
                "maximum": 14.0,
                "average": 13.0,
            }

            assert data["coolant_temp"] == {
                "minimum": 190.0,
                "maximum": 200.0,
                "average": 195.0,
            }

    finally:
        app.dependency_overrides.clear()


def test_get_datalog_metrics_not_found(test_db):
    """Test retrieving metrics for a nonexistent datalog."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        with TestClient(app) as client:
            response = client.get("/api/logs/999/metrics")

            assert response.status_code == 404
            assert response.json() == {
                "detail": "Datalog not found"
            }

    finally:
        app.dependency_overrides.clear()


def test_get_datalog_metrics_no_samples(test_db):
    """Test metrics for a datalog with no telemetry samples."""

    app.dependency_overrides[get_db] = override_get_db(test_db)

    try:
        datalog = DatalogModel(
            filename="empty_metrics.csv",
            vehicle="2021 USDM WRX",
        )


        with Session(test_db) as session:
            session.add(datalog)
            session.commit()

            datalog_id = datalog.id

        with TestClient(app) as client:
            response = client.get(
                f"/api/logs/{datalog_id}/metrics"

            )

            assert response.status_code == 200

            data = response.json()

            expected_statistics = {
                "minimum": None,
                "maximum": None,
                "average": None,
            }

            assert data["boost"] == expected_statistics
            assert data["rpm"] == expected_statistics
            assert data["afr"] == expected_statistics
            assert data["coolant_temp"] == expected_statistics
            
    finally:
        app.dependency_overrides.clear()