# Accessport Telemetry Analyzer

A full-stack application for importing, processing, analyzing, and visualizing vehicle telemetry data recorded by the COBB Accessport.

The project is designed to turn raw vehicle datalogs into an interactive application that makes telemetry easier to inspect, compare, and understand.

> **Project Status:** 🚧 In Development — Backend API development underway

---

## Overview

Vehicle datalogs contain a large amount of time-series information such as engine speed, boost pressure, throttle position, air/fuel measurements, temperatures, and ignition timing.

The Accessport Telemetry Analyzer provides a centralized system for uploading, processing, storing, retrieving, and eventually visualizing these logs through a REST API and interactive web dashboard.

### Core workflow

```text
COBB Accessport CSV
        │
        ▼
   File Upload
        │
        ▼
 Data Validation
        │
        ▼
 Pandas Processing
        │
        ▼
 Data Normalization
        │
        ▼
     Persistence
        │
        ▼
 SQLAlchemy / SQLite
        │
        ▼
    REST API
        │
        ▼
 React + TypeScript
        │
        ▼
 Telemetry Dashboard
```

---

## Features

### Implemented

* Parse COBB Accessport datalog CSV files
* Extract Accessport metadata
* Validate telemetry columns
* Handle invalid and empty telemetry data
* Normalize telemetry data
* Create domain-level datalog objects
* Persist datalog metadata
* Persist normalized telemetry samples
* Retrieve datalogs by ID
* Retrieve all datalogs
* Delete datalogs
* Reconstruct domain datalog objects from database records
* Convert persisted telemetry back into Pandas DataFrames
* Maintain datalog → telemetry relationships
* Cascade-delete telemetry when a datalog is deleted
* FastAPI application foundation
* API health-check endpoint
* Automated backend testing with Pytest

### Planned Features

* Upload COBB Accessport datalog CSV files through the REST API
* REST API for retrieving telemetry
* Interactive telemetry charts
* RPM and boost analysis
* AFR/lambda visualization
* Throttle position analysis
* Engine temperature monitoring
* Ignition timing visualization
* Summary statistics
* Identify potentially unusual telemetry values
* Compare telemetry channels
* Manage and delete uploaded logs
* Frontend dashboard

---

## Technology Stack

### Backend

* Python
* FastAPI
* Pandas
* SQLAlchemy
* SQLite
* Pytest

### Frontend

* React
* TypeScript
* Vite
* Recharts

### Development & Infrastructure

* Git
* GitHub
* Docker
* GitHub Actions
* REST APIs
* Azure

> PostgreSQL, Docker, CI/CD, and cloud deployment are planned for later stages of development. The current development database is SQLite.

---

## Project Structure

The backend currently contains the following structure:

```text
Accessport-Telemetry-Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── repositories/
│   │   │       ├── __init__.py
│   │   │       └── datalog.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── datalog.py
│   │   │
│   │   └── services/
│   │       ├── ingestion/
│   │       │   ├── __init__.py
│   │       │   ├── metadata.py
│   │       │   ├── normalizer.py
│   │       │   ├── parser.py
│   │       │   └── validator.py
│   │       │
│   │       └── persistence/
│   │           ├── __init__.py
│   │           └── datalog.py
│   │
│   ├── tests/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── test_main.py
│   │   ├── database/
│   │   │   ├── test_database.py
│   │   │   ├── test_models.py
│   │   │   └── test_repositories.py
│   │   ├── ingestion/
│   │   │   ├── test_metadata.py
│   │   │   ├── test_normalizer.py
│   │   │   ├── test_parser.py
│   │   │   ├── test_pipeline.py
│   │   │   └── test_validator.py
│   │   ├── models/
│   │   │   └── test_datalog.py
│   │   └── services/
│   │       └── test_persistence.py
│   │
│   └── requirements.txt
│
├── frontend/
│   └── ...
│
├── data/
│   └── sample/
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

The API layer is currently being developed within `backend/app/main.py`. Dedicated API modules will be introduced as the REST API grows.

---

## API

The backend exposes a RESTful API for interacting with telemetry logs.

### Current Endpoints

| Method | Endpoint  | Description     |
| ------ | --------- | --------------- |
| `GET`  | `/`       | API information |
| `GET`  | `/health` | Health check    |

### Planned Endpoints

| Method   | Endpoint                   | Description                  |
| -------- | -------------------------- | ---------------------------- |
| `POST`   | `/api/logs/upload`         | Upload a telemetry CSV       |
| `GET`    | `/api/logs`                | Retrieve uploaded logs       |
| `GET`    | `/api/logs/{id}`           | Retrieve a specific log      |
| `GET`    | `/api/logs/{id}/telemetry` | Retrieve telemetry samples   |
| `GET`    | `/api/logs/{id}/metrics`   | Retrieve telemetry metrics   |
| `GET`    | `/api/logs/{id}/analysis`  | Retrieve calculated analysis |
| `DELETE` | `/api/logs/{id}`           | Delete a telemetry log       |

Interactive API documentation is provided by FastAPI:

```text
/docs
```

Once the development server is running, the interactive Swagger UI will be available at:

```text
http://127.0.0.1:8000/docs
```

---

## Telemetry Data

The application is designed to work with time-series vehicle telemetry such as:

* RPM
* Vehicle speed
* Boost pressure
* Manifold absolute pressure (MAP)
* Air/fuel ratio (AFR)
* Lambda
* Throttle position
* Intake air temperature (IAT)
* Coolant temperature
* Ignition timing
* Fuel pressure
* Knock feedback
* Other channels available in the source datalog

The exact telemetry channels depend on the Accessport configuration and the data contained within each log.

---

## Data Analysis

The application will calculate and visualize useful statistics from uploaded telemetry.

Examples include:

### Engine Speed

* Minimum RPM
* Maximum RPM
* Average RPM
* RPM over time

### Boost / MAP

* Minimum pressure
* Maximum pressure
* Average pressure
* Pressure vs. RPM
* Pressure vs. time

### AFR / Lambda

* Minimum value
* Maximum value
* Average value
* AFR/lambda vs. RPM
* AFR/lambda vs. time

### Temperature

* Intake air temperature
* Coolant temperature
* Temperature changes over time

### Throttle

* Throttle position over time
* Throttle position vs. RPM

---

## Example Visualizations

The dashboard will provide interactive charts such as:

```text
RPM vs. Time

RPM
│
│        ╭──────╮
│       ╱        ╲
│      ╱          ╲
│  ╭──╯            ╰──╮
│ ╱                    ╲
└────────────────────────── Time
```

Additional charts will allow multiple telemetry channels to be analyzed independently or compared against one another.

---

## Getting Started

### Prerequisites

Make sure the following are installed:

* Python 3.11+
* Node.js 20+
* npm
* Git

The current backend uses SQLite, so PostgreSQL is **not required for local development**.

Docker support will be added as the project develops.

---

## Backend Setup

Clone the repository:

```bash
git clone <repository-url>
cd Accessport-Telemetry-Analyzer
```

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the backend tests:

```bash
python -m pytest backend/tests -v
```

The development API server can be started with Uvicorn once the server dependencies are available:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Testing

Backend tests are written using Pytest.

Run the complete backend test suite with:

```bash
python -m pytest backend/tests -v
```

### Current Test Coverage

The test suite currently covers:

* Domain models
* Database models
* Database relationships
* Database initialization
* Repository operations
* Datalog creation
* Datalog retrieval
* Datalog deletion
* Telemetry persistence
* Telemetry retrieval
* Database cascade behavior
* Persistence round trips
* CSV parsing
* Metadata extraction
* Telemetry normalization
* Telemetry validation
* Ingestion pipeline behavior
* FastAPI health endpoint

### Current Test Status

```text
50 passed
```

The current backend baseline is:

```text
50 tests passing
```

The project uses automated tests throughout development to verify behavior before moving between development phases.

---

# Development Roadmap

## Phase 1 — Project & Backend Foundation

* [x] Initialize Git repository
* [x] Create Python environment
* [x] Establish backend application structure
* [x] Create initial FastAPI application
* [x] Add health-check endpoint
* [x] Establish automated testing with Pytest
* [x] Add project `.gitignore`
* [x] Track backend dependencies
* [ ] Configure application settings

---

## Phase 2 — Data Ingestion

* [x] Implement CSV parsing
* [x] Parse Accessport datalogs
* [x] Validate telemetry columns
* [x] Handle invalid files
* [x] Handle empty data
* [x] Normalize telemetry data
* [x] Parse Accessport metadata
* [x] Add sample datalog
* [x] Create domain datalog model

---

# Phase 3 — Database & Persistence

## Phase 3.1 — Domain Model

* [x] Create `Datalog` domain model
* [x] Define datalog metadata model
* [x] Define normalized telemetry representation
* [x] Add domain model tests

## Phase 3.2 — Database Design

* [x] Design datalog database schema
* [x] Design telemetry sample schema
* [x] Define primary keys
* [x] Define foreign-key relationships
* [x] Configure datalog → telemetry relationships
* [x] Define cascade-delete behavior
* [x] Add database indexes

## Phase 3.3 — Repository Layer

* [x] Configure SQLAlchemy database
* [x] Create database tables
* [x] Implement datalog repository
* [x] Create datalogs
* [x] Retrieve datalogs by ID
* [x] Retrieve all datalogs
* [x] Delete datalogs
* [x] Persist telemetry samples
* [x] Add repository tests

## Phase 3.4 — Persist Datalogs

* [x] Create persistence service
* [x] Convert domain datalogs to database models
* [x] Convert telemetry DataFrames to database models
* [x] Persist datalog metadata
* [x] Persist telemetry samples
* [x] Maintain datalog/telemetry relationships
* [x] Add persistence tests

## Phase 3.5 — Retrieve Datalogs

* [x] Retrieve datalogs through the repository
* [x] Convert database metadata to domain metadata
* [x] Convert telemetry samples to Pandas DataFrames
* [x] Reconstruct domain `Datalog` objects
* [x] Handle missing datalog IDs
* [x] Test database → domain round trips

## Phase 3.6 — Testing & Hardening

* [x] Review Phase 3 test coverage
* [x] Add missing unit tests
* [x] Add edge-case tests
* [x] Test invalid and empty data
* [x] Test persistence behavior
* [x] Improve test organization
* [x] Verify cascade-delete behavior
* [x] Add persistence → retrieval round-trip test
* [x] Run complete backend test suite

**Phase 3 Status: ✅ Complete**

---

# Phase 4 — REST API

## Phase 4.1 — API Foundation

* [x] Add FastAPI
* [x] Create FastAPI application entry point
* [x] Configure API metadata
* [x] Add root endpoint
* [x] Add `/health` endpoint
* [x] Add FastAPI API test
* [x] Verify complete backend test suite
* [x] Record backend dependencies
* [x] Clean tracked Python bytecode from repository
* [x] Commit API foundation
* [x] Push Phase 4.1 to GitHub

**Phase 4.1 Status: ✅ Complete**

Latest commit:

```text
9cf5af5 Add FastAPI foundation
```

Current Git state:

```text
main → origin/main
working tree clean
```

---

## Phase 4.2 — Datalog Endpoints

* [ ] Design API request/response schemas
* [ ] Implement datalog upload endpoint
* [ ] Connect upload endpoint to ingestion pipeline
* [ ] Connect ingestion pipeline to persistence service
* [ ] Implement datalog listing endpoint
* [ ] Implement individual datalog retrieval endpoint
* [ ] Implement datalog deletion endpoint
* [ ] Add endpoint tests
* [ ] Verify API → service → repository flow

**Current Development Phase: 🚧 Phase 4.2**

---

## Phase 4.3 — Telemetry Endpoints

* [ ] Implement telemetry retrieval endpoint
* [ ] Convert telemetry data into API-friendly JSON
* [ ] Handle large telemetry datasets
* [ ] Add telemetry response schemas
* [ ] Add telemetry endpoint tests

---

## Phase 4.4 — Analysis & Metrics

* [ ] Design metrics service
* [ ] Implement telemetry statistics
* [ ] Implement RPM analysis
* [ ] Implement boost/MAP analysis
* [ ] Implement AFR/lambda analysis
* [ ] Implement temperature analysis
* [ ] Implement throttle analysis
* [ ] Implement analysis endpoint
* [ ] Add analysis tests
* [ ] Keep analysis logic separated from HTTP/API layer

---

## Phase 4.5 — API Validation & Error Handling

* [ ] Validate uploaded files
* [ ] Validate request parameters
* [ ] Handle invalid CSV files
* [ ] Handle unsupported file types
* [ ] Handle missing datalog IDs
* [ ] Return appropriate HTTP status codes
* [ ] Add meaningful API error responses
* [ ] Add validation tests

---

## Phase 4.6 — API Integration Testing

* [ ] Test upload → ingestion → persistence
* [ ] Test persistence → API retrieval
* [ ] Test telemetry retrieval
* [ ] Test analysis workflow
* [ ] Test deletion workflow
* [ ] Test complete API lifecycle
* [ ] Run complete backend test suite

**Phase 4 Goal:**

```text
Upload
   ↓
Validate
   ↓
Parse
   ↓
Normalize
   ↓
Persist
   ↓
Retrieve
   ↓
Analyze
   ↓
Delete
```

---

# Phase 5 — Frontend

* [ ] Initialize React/TypeScript application
* [ ] Create dashboard layout
* [ ] Create upload interface
* [ ] Display uploaded logs
* [ ] Build telemetry charts
* [ ] Add metric summaries
* [ ] Add telemetry filtering
* [ ] Add responsive design
* [ ] Connect frontend to REST API

---

# Phase 6 — Testing

* [ ] Expand unit-test coverage
* [ ] Add API tests
* [ ] Add integration tests
* [ ] Add data-validation tests
* [ ] Add frontend tests
* [ ] Add end-to-end tests
* [ ] Improve test coverage
* [ ] Add CI test execution

---

# Phase 7 — Production Engineering

* [ ] Dockerize application
* [ ] Add Docker Compose
* [ ] Add environment configuration
* [ ] Add application logging
* [ ] Add GitHub Actions
* [ ] Add CI pipeline
* [ ] Improve security
* [ ] Add API documentation
* [ ] Evaluate PostgreSQL migration
* [ ] Add production database migrations

---

# Phase 8 — Deployment

* [ ] Deploy backend
* [ ] Deploy frontend
* [ ] Configure production database
* [ ] Configure environment variables
* [ ] Add production monitoring
* [ ] Add live demo
* [ ] Configure production domain

---

## Engineering Goals

This project is being developed with real-world software engineering practices in mind.

Key goals include:

* Clean architecture
* Separation of concerns
* RESTful API design
* Strong data validation
* Automated testing
* Version control
* Documentation
* Containerization
* CI/CD
* Cloud deployment
* Maintainable and readable code

The goal is not simply to create a working dashboard, but to demonstrate the complete development lifecycle of a modern full-stack application.

The backend architecture is intentionally being developed in layers:

```text
API Layer
    │
    ▼
Service Layer
    │
    ▼
Domain Models
    │
    ▼
Repository Layer
    │
    ▼
Database
```

This separation allows the API, business logic, domain models, persistence layer, and database to evolve independently.

---

## Important Note

This application is intended for **data analysis and visualization**.

Telemetry observations or automated flags produced by the application should not be interpreted as definitive mechanical diagnoses, tuning recommendations, or proof of vehicle safety.

---

## Future Improvements

Potential future features include:

* User authentication
* Multiple vehicle profiles
* Datalog comparison
* Advanced anomaly detection
* Automated telemetry summaries
* Real-time telemetry ingestion
* Additional data formats
* Exportable reports
* Cloud storage
* Background processing for large datalogs
* WebSocket-based live telemetry
* C#/.NET API implementation
* Containerized deployment
* Kubernetes deployment
* Advanced observability with OpenTelemetry
* Prometheus/Grafana monitoring

---

## License

This project is currently intended as a personal software engineering portfolio project.

A formal open-source license may be added in the future.

---

## Author

**Tyrell Robbins**

Computer Science student and software/IT professional focused on software engineering, systems, cloud technologies, and data-driven applications.
