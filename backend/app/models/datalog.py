"""
Domain models for Accessport telemetry data
"""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


from backend.app.services.ingestion.metadata import DatalogMetadata


@dataclass
class Datalog:
    """
    Represents a parsed and normalized Accesport datalog

    Att:
        filename: OG csv filename
        metadata: accessport and vehicle metadata
        telemetry: normalized telemetry samples
    """


    filename: str
    metadata: DatalogMetadata
    telemetry: pd.DataFrame

    @classmethod
    def from_dataframe(
        cls,
        filename: str | Path,
        metadata: DatalogMetadata,
        telemetry: pd.DataFrame,

    ) -> "Datalog":
        """Create a Datalog from normalized telemetry data"""

        return cls(
            filename=Path(filename).name,
            metadata=metadata,
            telemetry=telemetry,
        )

    

