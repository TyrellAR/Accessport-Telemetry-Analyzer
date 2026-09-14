# Accessport Telemetry Analyzer

A full-stack application for importing, processing, analyzing, and visualizing vehicle telemetry data recorded by the COBB Accessport.

The project is designed to turn raw vehicle datalogs into an interactive application that makes telemetry easier to inspect, compare, and understand.

> **Project Status:** 🚧 In Development — Backend REST API development underway

---

## Overview

Vehicle datalogs contain a large amount of time-series information such as engine speed, boost pressure, throttle position, air/fuel measurements, temperatures, and ignition timing.

The Accessport Telemetry Analyzer provides a centralized system for uploading, processing, storing, retrieving, and eventually visualizing these logs through a REST API and interactive web dashboard.

### Core Workflow

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
   CSV Parsing
        │
        ▼
Metadata Extraction
        │
        ▼
Data Normalization
        │
        ▼
 Domain Datalog
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

# Features

## Implemented

### Data Ingestion

* Parse COBB Accessport datalog CSV files
* Extract Accessport metadata
* Parse Accessport model and firmware information
* Parse vehicle information
* Parse reflash and realtime tune information
* Validate telemetry columns
* Validate telemetry data integrity
* Handle invalid and empty telemetry data
* Normalize telemetry column names
* Normalize telemetry data types
* Create domain-level `Datalog` objects
* Coordinate ingestion through an ingestion service

### Database & Persistence

* SQLAlchemy database configuration
* SQLite development database
* Datalog database model
* Telemetry sample database model
* Datalog → telemetry relationships
* Foreign-key relationships
* Cascade deletion
* Database indexes
* Datalog repository
* Datalog creation
* Datalog retrieval by ID
* Datalog listing
* Datalog deletion
* Telemetry sample persistence
* Domain → database conversion
* Database → domain reconstruction
* Telemetry DataFrame reconstruction
* Persistence round-trip testing

### REST API

* FastAPI application
* API metadata
* Root endpoint
* `/health` endpoint
* Datalog response schema
* Datalog listing endpoint
* Individual datalog retrieval endpoint
* Datalog deletion endpoint
* API dependency injection for database sessions
* API integration with SQLAlchemy repository layer
* API endpoint tests
* Swagger/OpenAPI documentation

### Testing

* Automated backend testing with Pytest
* Domain model tests
* Database model tests
* Repository tests
* Persistence tests
* CSV parser tests
* Metadata tests
* Normalization tests
* Validation tests
* Ingestion pipeline tests
* API endpoint tests
* Database cascade tests
* Persistence round-trip tests

---

## Planned Features

* Upload COBB Accessport datalog CSV files through the REST API
* Complete API → ingestion → persistence integration
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

# Technology Stack

## Backend

* Python
* FastAPI
* Pandas
* SQLAlchemy
* SQLite
* Pytest

## Frontend

* React
* TypeScript
* Vite
* Recharts

## Development & Infrastructure

* Git
* GitHub
* Docker
* GitHub Actions
* REST APIs
* Azure

> PostgreSQL, Docker, CI/CD, and cloud deployment are planned for later stages of development. The current development database is SQLite.

---

# Architecture

The application is being developed using a layered architecture designed to separate HTTP concerns, business logic, domain models, persistence, and database operations.

## Target Architecture

```text
HTTP Request
     │
     ▼
API Layer
     │
     ▼
Service Layer
     │
     ▼
Domain Model
     │
     ▼
Repository Layer
     │
     ▼
Database
```

For an uploaded datalog, the intended flow is:

```text
POST /api/logs/upload
        │
        ▼
    FastAPI API
        │
        ▼
DatalogIngestionService
        │
        ├── Parse CSV
        ├── Extract metadata
        ├── Validate telemetry
        └── Normalize telemetry
        │
        ▼
      Datalog
        │
        ▼
DatalogPersistenceService
        │
        ▼
DatalogRepository
        │
        ▼
SQLAlchemy / SQLite
```

The API layer is responsible for HTTP concerns.

The service layer coordinates application workflows.

The domain layer represents the application's core datalog concepts.

The repository layer handles database operations.

The database layer manages persistence.

This separation is intended to allow individual parts of the application to evolve independently.

---

# Project Structure

The current backend structure is:

```text
Accessport-Telemetry-Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── datalog.py
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
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── datalog.py
│   │   │
│   │   └── services/
│   │       ├── ingestion/
│   │       │   ├── __init__.py
│   │       │   ├── metadata.py
│   │       │   ├── normalizer.py
│   │       │   ├── parser.py
│   │       │   ├── service.py
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
│   │   │
│   │   ├── database/
│   │   │   ├── test_database.py
│   │   │   ├── test_models.py
│   │   │   └── test_repositories.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── test_metadata.py
│   │   │   ├── test_normalizer.py
│   │   │   ├── test_parser.py
│   │   │   ├── test_pipeline.py
│   │   │   └── test_validator.py
│   │   │
│   │   ├── models/
│   │   │   └── test_datalog.py
│   │   │
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

The API has now been separated from the FastAPI application entry point.

`backend/app/main.py` is responsible for creating the FastAPI application and registering API routers.

Datalog-specific HTTP endpoints are located in:

```text
backend/app/api/datalog.py
```

API response schemas are located in:

```text
backend/app/schemas/datalog.py
```

Ingestion orchestration is handled by:

```text
backend/app/services/ingestion/service.py
```

---

# API

The backend exposes a RESTful API for interacting with telemetry logs.

## Current Endpoints

| Method   | Endpoint         | Description                 |
| -------- | ---------------- | --------------------------- |
| `GET`    | `/`              | API information             |
| `GET`    | `/health`        | Health check                |
| `GET`    | `/api/logs`      | Retrieve all datalogs       |
| `GET`    | `/api/logs/{id}` | Retrieve a specific datalog |
| `DELETE` | `/api/logs/{id}` | Delete a datalog            |

## In Development

| Method | Endpoint           | Description                        |
| ------ | ------------------ | ---------------------------------- |
| `POST` | `/api/logs/upload` | Upload and persist a telemetry CSV |

## Planned Endpoints

| Method | Endpoint                   | Description                  |
| ------ | -------------------------- | ---------------------------- |
| `GET`  | `/api/logs/{id}/telemetry` | Retrieve telemetry samples   |
| `GET`  | `/api/logs/{id}/metrics`   | Retrieve telemetry metrics   |
| `GET`  | `/api/logs/{id}/analysis`  | Retrieve calculated analysis |

Interactive API documentation is provided by FastAPI.

Once the development server is running:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI specification is also available through FastAPI.

---

# Telemetry Data

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

The ingestion system normalizes supported source channels into consistent application-level field names.

---

# Data Analysis

The application will calculate and visualize useful statistics from uploaded telemetry.

Examples include:

## Engine Speed

* Minimum RPM
* Maximum RPM
* Average RPM
* RPM over time

## Boost / MAP

* Minimum pressure
* Maximum pressure
* Average pressure
* Pressure vs. RPM
* Pressure vs. time

## AFR / Lambda

* Minimum value
* Maximum value
* Average value
* AFR/lambda vs. RPM
* AFR/lambda vs. time

## Temperature

* Intake air temperature
* Coolant temperature
* Temperature changes over time

## Throttle

* Throttle position over time
* Throttle position vs. RPM

---

# Example Visualizations

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

# Getting Started

## Prerequisites

Make sure the following are installed:

* Python 3.11+
* Node.js 20+
* npm
* Git

The current backend uses SQLite, so PostgreSQL is **not required for local development**.

Docker support will be expanded as the project develops.

---

# Backend Setup

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

Start the development server:

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

# Testing

Backend tests are written using Pytest.

Run the complete backend test suite with:

```bash
python -m pytest backend/tests -v
```

## Test Coverage

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
* Datalog API listing
* Datalog API retrieval
* Datalog API deletion
* API not-found behavior

The API tests use an isolated test database so API testing does not depend on the development SQLite database.

## Development Testing Strategy

The project uses multiple levels of testing:

```text
Unit Tests
    │
    ├── Parser
    ├── Validator
    ├── Normalizer
    ├── Metadata
    └── Domain Models
         │
         ▼
Service Tests
    │
    └── Persistence / Ingestion
         │
         ▼
API Tests
    │
    └── HTTP endpoints
         │
         ▼
Integration Tests
    │
    └── Upload → Ingestion → Persistence
```

The goal is to verify individual components independently before verifying complete application workflows.

---

# Development Roadmap

# Phase 1 — Project & Backend Foundation

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

# Phase 2 — Data Ingestion

* [x] Implement CSV parsing
* [x] Parse Accessport datalogs
* [x] Validate telemetry columns
* [x] Handle invalid files
* [x] Handle empty data
* [x] Normalize telemetry data
* [x] Parse Accessport metadata
* [x] Add sample datalog
* [x] Create domain datalog model

**Phase 2 Status: ✅ Complete**

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
* [x] Create dedicated API package
* [x] Commit API foundation
* [x] Push Phase 4.1 to GitHub

**Phase 4.1 Status: ✅ Complete**

---

## Phase 4.2 — Datalog Endpoints

### API Schemas

* [x] Create datalog response schema
* [x] Configure Pydantic ORM/database-model compatibility

### Datalog Listing

* [x] Implement `GET /api/logs`
* [x] Connect endpoint to repository
* [x] Add API tests
* [x] Test empty datalog collection
* [x] Test multiple datalogs

### Individual Datalog Retrieval

* [x] Implement `GET /api/logs/{id}`
* [x] Return 404 for missing datalog IDs
* [x] Add API tests

### Datalog Deletion

* [x] Implement `DELETE /api/logs/{id}`
* [x] Return 404 for missing datalog IDs
* [x] Commit database deletion
* [x] Verify cascade deletion of telemetry samples
* [x] Add API tests

### Datalog Upload

* [ ] Implement `POST /api/logs/upload`
* [x] Create `DatalogIngestionService`
* [x] Connect parsing to metadata extraction
* [x] Connect validation to ingestion pipeline
* [x] Connect normalization to ingestion pipeline
* [ ] Connect uploaded files to ingestion service
* [ ] Connect ingestion service to persistence service
* [ ] Persist uploaded datalogs through the API
* [ ] Return persisted datalog through the API
* [ ] Add upload endpoint tests

### Phase 4.2 Integration

* [ ] Verify API → service → repository flow
* [ ] Verify upload → ingestion → persistence
* [ ] Verify persisted datalog can be retrieved through API
* [ ] Verify uploaded telemetry is persisted
* [ ] Verify deletion after API upload

**Current Development Phase: 🚧 Phase 4.2**

**Current Focus: `POST /api/logs/upload`**

---

# Phase 4.3 — Telemetry Endpoints

* [ ] Implement telemetry retrieval endpoint
* [ ] Retrieve telemetry samples for a datalog
* [ ] Convert telemetry data into API-friendly JSON
* [ ] Design telemetry response schemas
* [ ] Handle large telemetry datasets
* [ ] Add telemetry endpoint tests

---

# Phase 4.4 — Analysis & Metrics

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

# Phase 4.5 — API Validation & Error Handling

This phase will focus specifically on making the API robust when dealing with invalid requests and files.

* [ ] Validate uploaded files
* [ ] Validate file extensions
* [ ] Validate request parameters
* [ ] Handle invalid CSV files
* [ ] Handle malformed CSV files
* [ ] Handle empty files
* [ ] Handle unsupported file types
* [ ] Handle invalid telemetry data
* [ ] Handle missing datalog IDs
* [ ] Return appropriate HTTP status codes
* [ ] Create meaningful API error responses
* [ ] Add API validation tests
* [ ] Add API error-handling tests

---

# Phase 4.6 — API Integration Testing

This phase will verify complete workflows across multiple application layers.

* [ ] Test upload → ingestion → persistence
* [ ] Test persistence → API retrieval
* [ ] Test telemetry retrieval
* [ ] Test analysis workflow
* [ ] Test deletion workflow
* [ ] Test complete API lifecycle
* [ ] Test invalid API workflows
* [ ] Run complete backend test suite

### Complete API Lifecycle

```text
Upload
   ↓
Validate
   ↓
Parse
   ↓
Normalize
   ↓
Create Domain Object
   ↓
Persist
   ↓
Retrieve
   ↓
Analyze
   ↓
Delete
```

**Phase 4 Goal:**

Build a complete backend API capable of accepting a COBB Accessport datalog, processing it through the application's data pipeline, persisting it, retrieving it, analyzing it, and deleting it.

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

# Engineering Goals

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

The current implementation is progressively moving toward this architecture.

For example, the upload workflow uses dedicated ingestion and persistence services to keep processing and database logic outside the HTTP endpoint.

Simple CRUD endpoints currently use the repository layer directly where appropriate. As the API grows, application-level workflows will be moved behind services when additional business logic is introduced.

---

# Important Note

This application is intended for **data analysis and visualization**.

Telemetry observations or automated flags produced by the application should not be interpreted as definitive mechanical diagnoses, tuning recommendations, or proof of vehicle safety.

---

# Future Improvements

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

# License

This project is currently intended as a personal software engineering portfolio project.

A formal open-source license may be added in the future.

---

# Author

**Tyrell Robbins**

Computer Science student and software/IT professional focused on software engineering, systems, cloud technologies, and data-driven applications.
