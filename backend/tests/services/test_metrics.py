from unittest.mock import Mock
from backend.app.models.metrics import (MetricStatistics, TelemetryMetrics)
from backend.app.services.analysis.metrics import TelemetryMetricsServices

def test_get_metrics_returns_statistics():
    repository = Mock()

    expected_metrics = TelemetryMetrics(
        boost=MetricStatistics(-8.0, 18.0, 5.0),
        rpm=MetricStatistics(1000.0, 5000.0, 3000.0),
        afr=MetricStatistics(11.1, 14.7, 12.6),
        coolant_temp=MetricStatistics(180.0, 200.0, 190.0),
    )

    repository.get_by_id.return_value = Mock(id=1)
    repository.get_telemetry_statistics.return_value = expected_metrics

    service = TelemetryMetricsServices(repository)

    result = service.get_metrics(1)

    assert result == expected_metrics

    repository.get_by_id.assert_called_once_with(1)
    repository.get_telemetry_statistics.assert_called_once_with(1)


def test_get_metrics_return_none_when_datalog_not_found():
    repository = Mock()

    repository.get_by_id.return_value = None

    service = TelemetryMetricsServices(repository)

    result = service.get_metrics(999)

    assert result is None

    repository.get_by_id.assert_called_once_with(999)
    repository.get_telemetry_statistics.assert_not_called()

