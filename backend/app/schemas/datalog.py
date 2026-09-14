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


