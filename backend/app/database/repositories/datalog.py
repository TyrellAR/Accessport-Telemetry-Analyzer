from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models import DatalogModel, TelemetrySampleModel

class DatalogRepository:
    """Repository for database operations involving datalogs."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, datalog: DatalogModel) -> DatalogModel:
        """Persist a datalog and return it."""
        self.session.add(datalog)
        self.session.flush()

        return datalog

    def get_by_id(self, datalog_id: int) -> DatalogModel | None:
        """Retrieve a datalog by its primary key."""
        statement = select(DatalogModel).where(
        DatalogModel.id == datalog_id
    )

        return self.session.scalar(statement)

    def get_all(self) -> list[DatalogModel]:
        """Retrieve all datalogs."""
        statement = select(DatalogModel)

        return list(self.session.scalars(statement))

    def delete(self, datalog_id: int) -> bool:
            """Delete a datalog by its primary key"""
            datalog = self.get_by_id(datalog_id)

            if datalog is None:
                return False

            self.session.delete(datalog)
            self.session.flush()

            return True
    
    def add_telemetry_samples(
        self,
        samples: list[TelemetrySampleModel],
    ) -> list[TelemetrySampleModel]:
        """Persist telemetry samples and return them."""

        self.session.add_all(samples)
        self.session.flush()

        return samples
