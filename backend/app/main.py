from fastapi import FastAPI

from backend.app.api.datalog import router as datalog_router

app = FastAPI(
    title="Accessport Telemetry Analyzer",
    description="API for analyzing vehicle telemetry data",
    version="0.1.0",
)

app.include_router(datalog_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Accessport Telemetry Analyzer API",
            "name": "Accessport Telemetry Analyzer",
            "version": "0.1.0",
            "status": "online",
            }
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
