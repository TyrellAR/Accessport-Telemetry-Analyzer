from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.database.models import Base, DatalogModel
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