from backend.app.database.repositories.datalog import DatalogRepository
from backend.app.models.metrics import TelemetryMetrics


class TelemetryMetricsServices:
    """Coordinate telemetry statistics retrieval"""

    def __init__(self, repository: DatalogRepository):
        self.repository = repository

    def get_metrics(self, datalog_id: int) -> TelemetryMetrics | None:
        """Retrieve metrics for and existing datalog."""

        datalog = self.repository.get_by_id(datalog_id)

        if datalog is None:
            return None

        return self.repository.get_telemetry_statistics(datalog_id)