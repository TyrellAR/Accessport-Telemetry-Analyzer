from sqlalchemy import inspect

from backend.app.database.database import engine, init_db


def test_database_tables_are_created():
    init_db()

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "datalogs" in tables
    assert "telemetry_samples" in tables