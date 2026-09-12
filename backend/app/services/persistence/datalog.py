"""
Persistence service for Accessport datalogs.
"""
import pandas as pd

from backend.app.database.models import DatalogModel, TelemetrySampleModel
from backend.app.models.datalog import Datalog
from backend.app.database.repositories.datalog import DatalogRepository
from backend.app.services.ingestion.metadata import DatalogMetadata


TELEMETRY_FIELD_MAPPING = {
    "timestamp": "timestamp",
    "rpm": "rpm",
    "speed": "speed",
    "coolant_temp": "coolant_temp",
    "boost": "boost",
    "boost_ext": "boost_ext",
    "afr": "afr",
    "intake_temp": "intake_temp",
    "intake_temp_manifold": "intake_temp_manifold",
    "throttle_position": "throttle_position",
    "fuel_pressure": "fuel_pressure",
    "fuel_pressure_target": "fuel_pressure_target",
    "map": "map",
    "ignition_timing": "ignition_timing",
    "inj_duty_cycle": "inj_duty_cycle",
    "inj_pulse_width": "inj_pulse_width",
    "maf_corrected": "maf_corrected",
    "load": "load",
    "oil_temp": "oil_temp",
}


class DatalogPersistenceService:
    """Persist domain Datalog objects to the database."""

    def __init__(self, repository: DatalogRepository):
        self.repository = repository

    def persist(self, datalog: Datalog) -> DatalogModel:
        """
        Persist a domain Datalog to the database.

        Args:
            datalog: Parsed and normalized domain datalog.

        Returns:
            The persisted DatalogModel.
        """

        datalog_model = DatalogModel(
            filename=datalog.filename,
            accessport_model=datalog.metadata.accessport_model,
            firmware_version=datalog.metadata.firmware_version,
            vehicle=datalog.metadata.vehicle,
            reflash_tune=datalog.metadata.reflash_tune,
            realtime_tune=datalog.metadata.realtime_tune,
        )

        self.repository.create(datalog_model)

        samples = self._create_telemetry_samples(
            datalog_model,
            datalog,
        )

        self.repository.add_telemetry_samples(samples)

        return datalog_model

    def _create_telemetry_samples(
        self,
        datalog_model: DatalogModel,
        datalog: Datalog,
    ) -> list[TelemetrySampleModel]:
        """Convert domain telemetry rows into database models."""

        samples = []

        for _, row in datalog.telemetry.iterrows():
            sample_data = {
                database_field: row.get(dataframe_field)
                for dataframe_field, database_field in TELEMETRY_FIELD_MAPPING.items()
            }

            sample = TelemetrySampleModel(
                datalog=datalog_model,
                **sample_data,
            )

            samples.append(sample)

        return samples

    def retrieve(self, datalog_id: int) -> Datalog | None:
        """Retrieve a datalog from the database and convert it to a domain Datalog"""

        datalog_model = self.repository.get_by_id(datalog_id)

        if datalog_model is None:
            return None

        metadata = DatalogMetadata(
            accessport_model=datalog_model.accessport_model,
            firmware_version=datalog_model.firmware_version,
            vehicle=datalog_model.vehicle,
            reflash_tune=datalog_model.reflash_tune,
            realtime_tune=datalog_model.realtime_tune,
        )

        telemetry = pd.DataFrame(
            [
                {
                    "timestamp": sample.timestamp,
                    "rpm": sample.rpm,
                    "speed": sample.speed,
                    "coolant_temp": sample.coolant_temp,
                    "boost": sample.boost,
                    "boost_ext": sample.boost_ext,
                    "afr": sample.afr,
                    "intake_temp": sample.intake_temp,
                    "intake_temp_manifold": sample.intake_temp_manifold,
                    "throttle_position": sample.throttle_position,
                    "fuel_pressure": sample.fuel_pressure,
                    "fuel_pressure_target": sample.fuel_pressure_target,
                    "map": sample.map,
                    "ignition_timing": sample.ignition_timing,
                    "inj_duty_cycle": sample.inj_duty_cycle,
                    "inj_pulse_width": sample.inj_pulse_width,
                    "maf_corrected": sample.maf_corrected,
                    "load": sample.load,
                    "oil_temp": sample.oil_temp,
               }
                for sample in datalog_model.telemetry_samples
            ]
        )

        return Datalog(
            filename=datalog_model.filename,
            metadata=metadata,
            telemetry=telemetry,
        )


