from datetime import datetime

from pydantic import BaseModel, ConfigDict

class DatalogResponse(BaseModel):
    """API representation of a datalog"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    accessport_model: str | None
    firmware_version: str | None
    vehicle: str | None
    reflash_tune: str | None
    realtime_tune: str | None
    created_at: datetime

class TelemetrySampleResponse(BaseModel):
    """API representation of a telemetry sample."""

    model_config = ConfigDict(from_attributes=True)

    timestamp: float
    rpm: float | None
    speed: float | None
    coolant_temp: float | None
    boost: float | None
    boost_ext: float | None
    afr: float | None
    intake_temp: float | None
    intake_temp_manifold: float | None
    throttle_position: float | None
    fuel_pressure: float | None
    fuel_pressure_target: float | None
    map: float | None
    ignition_timing: float | None
    inj_duty_cycle: float | None
    inj_pulse_width: float | None
    maf_corrected: float | None
    load: float | None
    oil_temp: float | None