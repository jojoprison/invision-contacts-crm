# Multi-tenant Mini-CRM (Senior Python Test)

## Overview
Backend service for a multi-tenant CRM system.
Built with FastAPI, SQLAlchemy (Async), Alembic, and PostgreSQL.

## Architecture
The project follows a Clean Architecture / Layered approach:

- **src/api**: REST API layer (Routes, Request/Response schemas).
- **src/services**: Business logic layer. Domain rules, transactions, and orchestration.
- **src/repositories**: Data access layer. Abstraction over SQLAlchemy.
- **src/models**: Database models (SQLAlchemy ORM).
- **src/core**: Configuration, security, exceptions, utilities.

## Tech Stack
- **Python 3.11+**
- **FastAPI** (Async Web Framework)
- **SQLAlchemy 2.0** (Async ORM)
- **Alembic** (Migrations)
- **PostgreSQL** (Database)
- **Docker** (Containerization)

## Getting Started

### 1. Environment Setup
```bash
cd senior_crm
uv sync
```

### 2. Run Database
```bash
docker-compose up -d
```

### 3. Run Migrations
```bash
uv run alembic upgrade head
```

### 4. Run Application
```bash
uv run uvicorn src.main:app --reload
```
