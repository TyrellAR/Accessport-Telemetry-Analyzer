from pathlib import Path

from backend.app.models.datalog import Datalog
from backend.app.services.ingestion.metadata import parse_metadata
from backend.app.services.ingestion.normalizer import normalize_telemetry
from backend.app.services.ingestion.parser import parse_log
from backend.app.services.ingestion.validator import validate_telemetry

class DatalogIngestionService:
    """Coordinate parsing, validation, and normalization of datalogs"""

    def ingest(
            self,
            file_path: str | Path,
            filename: str,
    ) -> Datalog:
        """Ingest a Cobb Accessport datalog into a domain Datalog"""

        parsed_log = parse_log(file_path)

        ap_info = parse_log["metadata"].get(
            "ap_info",
            "",
        )

        metadata = parse_metadata(ap_info)

        telemetry = parsed_log["data"]

        validate_telemetry(telemetry)

        normalized_telemetry = normalize_telemetry(telemetry)

        return Datalog(
            filename=filename,
            metadata=metadata,
            telemetry=normalize_telemetry,
        )


