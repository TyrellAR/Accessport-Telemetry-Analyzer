from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.database.repositories.datalog import DatalogRepository
from backend.app.schemas.datalog import DatalogResponse


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