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
