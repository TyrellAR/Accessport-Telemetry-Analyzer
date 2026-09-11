from sqlalchemy.orm import Session

from backend.app.database.models import DatalogModel


class DatalogRepository:
    """Repository for database operations involving datalogs."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, datalog: DatalogModel) -> DatalogModel:
        """Persist a datalog and return it."""
        self.session.add(datalog)
        self.session.flush()

        return datalog