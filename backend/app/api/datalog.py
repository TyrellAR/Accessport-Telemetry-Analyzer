import tempfile

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.database.repositories.datalog import DatalogRepository
from backend.app.schemas.datalog import DatalogResponse, TelemetrySampleResponse
from backend.app.services.ingestion.parser import ParseError
from backend.app.services.ingestion.service import DatalogIngestionService
from backend.app.services.ingestion.validator import ValidationError
from backend.app.services.persistence.datalog import DatalogPersistenceService



router = APIRouter(
    prefix="/api/logs",
    tags=["datalogs"],
)


@router.get("", response_model=list[DatalogResponse])
def get_datalogs(db: Session = Depends(get_db)):
    """Return all datalogs."""
    repository = DatalogRepository(db)

    return repository.get_all()

@router.get("/{datalog_id}", response_model=DatalogResponse)
def get_datalog(datalog_id: int, db: Session = Depends(get_db)):
    """Return a datalog by ID."""
    repository = DatalogRepository(db)

    datalog = repository.get_by_id(datalog_id)

    if datalog is None:
        raise HTTPException(
            status_code=404,
            detail="Datalog not found",
        )

    return datalog

@router.get(
        "/{datalog_id}/telemetry",
        response_model=list[TelemetrySampleResponse],
)
def get_datalog_telemetry(
    datalog_id: int,
    db: Session = Depends(get_db),
):

    """Return telemetry samples for a datalog."""

    repository = DatalogRepository(db)

    datalog = repository.get_by_id(datalog_id)

    if datalog is None:
        raise HTTPException(
            status_code=404,
            detail="Datalog not found",
        )
    return repository.get_telemetry_samples(datalog_id)

@router.delete("/{datalog_id}")
def delete_datalog(
    datalog_id: int,
    db: Session = Depends(get_db),
):
    """Delete a datalog by ID."""

    repository = DatalogRepository(db)

    deleted = repository.delete(datalog_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Datalog not found",
        )
    db.commit()

    return {"detail": "Datalog deleted"}

@router.post("/upload", response_model=DatalogResponse)
def upload_datalog(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload, ingest, and persist a COBB Accessport datalog."""

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=422,
            detail="The program only accepts .csv files",
        )
    with tempfile.NamedTemporaryFile(suffix=".csv") as temp_file:
        temp_file.write(file.file.read())
        temp_file.flush()

        ingestion_service = DatalogIngestionService()

        try:
            datalog = ingestion_service.ingest(
                temp_file.name,
                file.filename or "uploaded.csv",
            )
        except (ParseError, ValidationError) as e:
            raise HTTPException(
                status_code=422,
                detail=str(e),
            ) from e
        repository = DatalogRepository(db)
        persistence_service = DatalogPersistenceService(repository)
        datalog_model = persistence_service.persist(datalog)
        db.commit()

        return datalog_model