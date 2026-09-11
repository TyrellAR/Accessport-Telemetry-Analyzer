"""
SQLAlchemy database models for Accessport telemetry
"""


from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Base class for all database models."""

    pass

class DatalogModel(Base):
    """Database representation of an Accessport datalog"""

    __tablename__ = "datalogs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    filename: Mapped[str] = mapped_column(String[255])

    accessport_model: Mapped[str | None] = mapped_column(String[100])
    firmware_version: Mapped[str | None] = mapped_column(String[100])
    vehicle: Mapped[str | None] = mapped_column(String[255])
    reflash_tune: Mapped[str | None] = mapped_column(String[255])
    realtime_tune: Mapped[str | None] = mapped_column(String[255])

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        
    )

    telemetry_samples: Mapped[list["TelemetrySampleModel"]] = relationship(
    back_populates="datalog",
    cascade="all, delete-orphan",

    )

class TelemetrySampleModel(Base):
    """Database representation of a single telemetry sample"""

    __tablename__ = "telemetry_samples"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    ) 

    datalog_id: Mapped[int] = mapped_column(
        ForeignKey("datalogs.id"),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    rpm: Mapped[float | None] = mapped_column(Float)
    speed: Mapped[float | None] = mapped_column(Float)
    coolant_temp: Mapped[float | None] = mapped_column(Float)
    boost: Mapped[float | None] = mapped_column(Float)
    boost_ext: Mapped[float | None] = mapped_column(Float)
    afr: Mapped[float | None] = mapped_column(Float)
    intake_temp: Mapped[float | None] = mapped_column(Float)
    intake_temp_manifold: Mapped[float | None] = mapped_column(Float)
    throttle_position: Mapped[float | None] = mapped_column(Float)
    fuel_pressure: Mapped[float | None] = mapped_column(Float)
    fuel_pressure_target: Mapped[float | None] = mapped_column(Float)
    map: Mapped[float | None] = mapped_column(Float)
    ignition_timing: Mapped[float | None] = mapped_column(Float)
    inj_duty_cycle: Mapped[float | None] = mapped_column(Float)
    inj_pulse_width: Mapped[float | None] = mapped_column(Float)
    maf_corrected: Mapped[float | None] = mapped_column(Float)
    load: Mapped[float | None] = mapped_column(Float)
    oil_temp: Mapped[float | None] = mapped_column(Float)

    datalog: Mapped["DatalogModel"] = relationship(
        back_populates="telemetry_samples",
    )
