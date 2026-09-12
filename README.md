# Accessport Telemetry Analyzer

A full-stack application for importing, processing, analyzing, and visualizing vehicle telemetry data recorded by the COBB Accessport.

The project is designed to turn raw vehicle datalogs into an interactive dashboard that makes telemetry easier to inspect, compare, and understand.

> **Project Status:** 🚧 In Development

---

## Overview

Vehicle datalogs contain a large amount of time-series information such as engine speed, boost pressure, throttle position, air/fuel measurements, temperatures, and ignition timing.

The Accessport Telemetry Analyzer provides a centralized interface for uploading these logs and exploring the data through an API and interactive web dashboard.

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
     REST API
        │
        ▼
   PostgreSQL
        │
        ▼
 React + TypeScript
        │
        ▼
 Telemetry Dashboard
```

---

## Features

### Planned Features

* Upload COBB Accessport datalog CSV files
* Validate uploaded telemetry data
* Parse and normalize telemetry channels
* Store log metadata and telemetry data
* REST API for accessing telemetry
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

---

## Technology Stack

### Backend

* Python
* FastAPI
* Pandas
* PostgreSQL
* SQLAlchemy
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

---

## Project Structure

```text
accessport-telemetry-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   ├── database/
│   │   ├── models/
│   │   ├── services/
│   │   └── schemas/
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   │
│   └── package.json
│
├── data/
│   └── sample/
│
├── tests/
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

## API

The backend exposes a RESTful API for interacting with telemetry logs.

### Current Endpoints

| Method | Endpoint  | Description     |
| ------ | --------- | --------------- |
| `GET`  | `/`       | API information |
| `GET`  | `/health` | Health check    |

### Planned Endpoints

| Method   | Endpoint                  | Description                  |
| -------- | ------------------------- | ---------------------------- |
| `POST`   | `/api/logs/upload`        | Upload a telemetry CSV       |
| `GET`    | `/api/logs`               | Retrieve uploaded logs       |
| `GET`    | `/api/logs/{id}`          | Retrieve a specific log      |
| `GET`    | `/api/logs/{id}/metrics`  | Retrieve telemetry metrics   |
| `GET`    | `/api/logs/{id}/analysis` | Retrieve calculated analysis |
| `DELETE` | `/api/logs/{id}`          | Delete a telemetry log       |

Interactive API documentation will be available through FastAPI's automatically generated documentation:

```text
/docs
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
* PostgreSQL

Docker support will be added as the project develops.

---

## Backend Setup

Clone the repository:

```bash
git clone <repository-url>
cd accessport-telemetry-analyzer
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
pip install -r requirements.txt
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

## Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the local development address displayed by Vite.

---

## Testing

Backend tests are written using Pytest.

Run the test suite with:

```bash
pytest
```

Current tests cover:

* Domain models
* Database models
* Database relationships
* Repository operations
* Datalog persistence
* Datalog retrieval
* Telemetry persistence
* Telemetry retrieval
* Database cascade behavior
* Metadata parsing

Additional tests will be added as development continues.

---

## Development Roadmap

### Phase 1 — Backend Foundation

* [x] Initialize Git repository
* [x] Create Python environment
* [x] Create FastAPI application
* [x] Add health-check endpoint
* [ ] Configure application settings

### Phase 2 — Data Ingestion

* [x] Implement CSV parsing
* [x] Parse Accessport datalogs
* [x] Validate telemetry columns
* [x] Handle invalid files
* [x] Normalize telemetry data
* [x] Parse Accessport metadata
* [x] Add sample datalog
* [x] Create domain datalog model

### Phase 3 — Database & Persistence

#### Phase 3.1 — Domain Model

* [x] Create `Datalog` domain model
* [x] Define datalog metadata model
* [x] Define normalized telemetry representation
* [x] Add domain model tests

#### Phase 3.2 — Database Design

* [x] Design datalog database schema
* [x] Design telemetry sample schema
* [x] Define primary keys
* [x] Define foreign-key relationships
* [x] Configure datalog → telemetry relationships
* [x] Define cascade-delete behavior
* [x] Add database indexes

#### Phase 3.3 — Repository Layer

* [x] Configure SQLAlchemy database
* [x] Create database tables
* [x] Implement datalog repository
* [x] Create datalogs
* [x] Retrieve datalogs by ID
* [x] Retrieve all datalogs
* [x] Delete datalogs
* [x] Persist telemetry samples
* [x] Add repository tests

#### Phase 3.4 — Persist Datalogs

* [x] Create persistence service
* [x] Convert domain datalogs to database models
* [x] Convert telemetry DataFrames to database models
* [x] Persist datalog metadata
* [x] Persist telemetry samples
* [x] Maintain datalog/telemetry relationships
* [x] Add persistence tests

#### Phase 3.5 — Retrieve Datalogs

* [x] Retrieve datalogs through the repository
* [x] Convert database metadata to domain metadata
* [x] Convert telemetry samples to Pandas DataFrames
* [x] Reconstruct domain `Datalog` objects
* [x] Handle missing datalog IDs
* [x] Test database → domain round trips

#### Phase 3.6 — Testing

* [ ] Review Phase 3 test coverage
* [ ] Add missing unit tests
* [ ] Add edge-case tests
* [ ] Test invalid and empty data
* [ ] Test persistence failure scenarios
* [ ] Improve test organization
* [ ] Run complete backend test suite

### Phase 4 — REST API

* [ ] Implement log upload endpoint
* [ ] Implement log listing
* [ ] Implement individual log retrieval
* [ ] Implement telemetry metrics endpoint
* [ ] Implement analysis endpoint
* [ ] Implement log deletion
* [ ] Add API validation

### Phase 5 — Frontend

* [ ] Initialize React/TypeScript application
* [ ] Create dashboard layout
* [ ] Create upload interface
* [ ] Display uploaded logs
* [ ] Build telemetry charts
* [ ] Add metric summaries
* [ ] Add responsive design

### Phase 6 — Testing

* [ ] Add unit tests
* [ ] Add API tests
* [ ] Add data-validation tests
* [ ] Add frontend tests
* [ ] Improve test coverage

### Phase 7 — Production Engineering

* [ ] Dockerize application
* [ ] Add Docker Compose
* [ ] Add environment configuration
* [ ] Add application logging
* [ ] Add GitHub Actions
* [ ] Add CI pipeline
* [ ] Improve security
* [ ] Add API documentation

### Phase 8 — Deployment

* [ ] Deploy backend
* [ ] Deploy frontend
* [ ] Configure production database
* [ ] Configure environment variables
* [ ] Add production monitoring
* [ ] Add live demo

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
