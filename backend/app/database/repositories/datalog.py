from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.app.database.models import DatalogModel, TelemetrySampleModel
from backend.app.models.metrics import MetricStatistics, TelemetryMetrics

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

    def get_telemetry_samples(
            self,
            datalog_id: int,
            limit: int = 100,
            offset: int = 0,
    ) -> list[TelemetrySampleModel]:
        
        statement = (
            select(TelemetrySampleModel)
            .where(TelemetrySampleModel.datalog_id == datalog_id)
            .order_by(
                TelemetrySampleModel.timestamp,
                TelemetrySampleModel.id,
            )
            .limit(limit)
            .offset(offset)
        )

        return list(self.session.scalars(statement))


    def get_max_boost(self, datalog_id: int) -> float | None:
        """ Retrieve the maximum recorded boost for a given datalog."""

        statement = (
            select(func.max(TelemetrySampleModel.boost))
            .where(TelemetrySampleModel.datalog_id == datalog_id)

        )

        return self.session.scalar(statement)


    def get_boost_statistics(self, datalog_id: int) -> MetricStatistics:
        """Calculate minumum, maximum and average boost for a datalog."""

        statement = (
            select(
                func.min(TelemetrySampleModel.boost).label("minimum"),
                func.max(TelemetrySampleModel.boost).label("maximum"),
                func.avg(TelemetrySampleModel.boost).label("average"),
            )
            .where(TelemetrySampleModel.datalog_id == datalog_id)
        )
        #return metrics instance with the retrieved values
        result = self.session.execute(statement).one()

        return MetricStatistics(
            minimum=result.minimum,
            maximum=result.maximum,
            average=result.average,
        )

    def get_telemetry_statistics(
            self,
            datalog_id: int,

    ) -> TelemetryMetrics:
        """Calculate minimum, maximum and average for all telemetry metrics for a datalog."""

        statement = (
            select(
                func.min(TelemetrySampleModel.boost).label("boost_minimum"),
                func.max(TelemetrySampleModel.boost).label("boost_maximum"),
                func.avg(TelemetrySampleModel.boost).label("boost_average"),
                func.min(TelemetrySampleModel.rpm).label("rpm_minimum"),
                func.max(TelemetrySampleModel.rpm).label("rpm_maximum"),
                func.avg(TelemetrySampleModel.rpm).label("rpm_average"),
                func.min(TelemetrySampleModel.afr).label("afr_minimum"),
                func.max(TelemetrySampleModel.afr).label("afr_maximum"),
                func.avg(TelemetrySampleModel.afr).label("afr_average"),
                func.min(TelemetrySampleModel.coolant_temp).label("coolant_temp_minimum"),
                func.max(TelemetrySampleModel.coolant_temp).label("coolant_temp_maximum"),
                func.avg(TelemetrySampleModel.coolant_temp).label("coolant_temp_average"),
            )
            .where(TelemetrySampleModel.datalog_id == datalog_id)
        )

        result = self.session.execute(statement).one()

        return TelemetryMetrics(
            boost=MetricStatistics(
                minimum=result.boost_minimum,
                maximum=result.boost_maximum,
                average=result.boost_average,
            ),
            rpm=MetricStatistics(
                minimum=result.rpm_minimum,
                maximum=result.rpm_maximum,
                average=result.rpm_average,
            ),
            afr=MetricStatistics(
                minimum=result.afr_minimum,
                maximum=result.afr_maximum,
                average=result.afr_average,
            ),
            coolant_temp=MetricStatistics(
                minimum=result.coolant_temp_minimum,
                maximum=result.coolant_temp_maximum,
                average=result.coolant_temp_average,
            ),
        )   