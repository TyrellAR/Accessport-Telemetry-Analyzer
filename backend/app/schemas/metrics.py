from pydantic import BaseModel, ConfigDict

class MetricsStatisticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    minimum: float | None
    maximum: float | None
    average: float | None


class TelemetryMetricsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    boost: MetricsStatisticsResponse
    rpm: MetricsStatisticsResponse
    afr: MetricsStatisticsResponse
    coolant_temp: MetricsStatisticsResponse

