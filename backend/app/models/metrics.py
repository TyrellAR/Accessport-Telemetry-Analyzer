from dataclasses import dataclass

@dataclass(frozen=True)
class MetricStatistics:
    """A dataclass to hold metrics statistics."""
    minimum: float | None
    maximum: float | None
    average: float | None

@dataclass(frozen=True)
class TelemetryMetrics:
    """A dataclass to hold telemetry metrics."""
    boost: MetricStatistics
    rpm: MetricStatistics
    afr: MetricStatistics
    coolant_temp: MetricStatistics


