# Multi-tenant Mini-CRM (Senior Python Test)

## Overview
Backend service for a multi-tenant CRM system with role-based access control.

Built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **Alembic**, and **PostgreSQL**.

## Architecture

```
src/
├── api/                    # REST API Layer
│   ├── deps.py             # Dependencies (auth, org context)
│   └── v1/                 # Versioned endpoints
│       ├── auth.py         # Register, Login, Refresh
│       ├── organizations.py
│       ├── contacts.py
│       ├── deals.py
│       ├── tasks.py
│       ├── activities.py
│       └── analytics.py
├── services/               # Business Logic Layer
│   ├── auth.py             # JWT, password hashing
│   ├── organization.py     # RBAC, membership
│   ├── contact.py
│   ├── deal.py             # Status/stage validation
│   ├── task.py             # Due date validation
│   ├── activity.py
│   └── analytics.py        # Summary, funnel + cache
├── repositories/           # Data Access Layer
│   ├── base.py             # Generic CRUD
│   └── ...                 # Entity-specific repos
├── models/                 # SQLAlchemy ORM Models
│   ├── auth.py             # User, Organization, Member
│   ├── crm.py              # Contact, Deal, Task, Activity
│   └── enums.py            # UserRole, DealStatus, etc.
├── schemas/                # Pydantic Schemas
├── core/                   # Config, Security, Exceptions
└── main.py                 # FastAPI Application
```

## Tech Stack
- **Python 3.11+**
- **FastAPI** — Async Web Framework
- **SQLAlchemy 2.0** — Async ORM
- **Alembic** — Migrations
- **PostgreSQL** — Database
- **Pydantic v2** — Validation
- **python-jose** — JWT tokens
- **passlib** — Password hashing

## Getting Started

### 1. Environment Setup
```bash
cd senior_crm
uv sync
```

### 2. Run Database
```bash
make db
make wait-db  # Wait for DB to be ready
```

### 3. Run Migrations & Seed Data
```bash
make migrate
make seed     # Populate with demo data (admin@example.com / admin)
```

### 4. Run Application
```bash
make run
```

### 5. Open Swagger UI
http://localhost:8001/docs

## Useful Commands (Makefile)

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies via uv |
| `make db` | Start PostgreSQL (docker-compose) |
| `make wait-db` | Wait for DB connection |
| `make seed` | Seed DB with demo user and data |
| `make migrate` | Run Alembic migrations |
| `make test` | Run tests |
| `make test-cov` | Run tests with coverage report |
| `make lint` | Check code style (ruff) |
| `make format` | Auto-format code |
| `make docker-build` | Build production Docker image |

## Running Tests

Create test database first:
```bash
docker exec -it senior_crm-db-1 psql -U postgres -c "CREATE DATABASE senior_crm_test;"
```

Run tests:
```bash
uv run pytest -v
```

## API Endpoints

All endpoints are prefixed with `/api/v1`.

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/register | Register + create org |
| POST | /auth/login | Get tokens |
| POST | /auth/refresh | Refresh access token |

### Organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations/me | List user's orgs |

### Contacts (requires `X-Organization-Id` header)
| Method | Path | Description |
|--------|------|-------------|
| GET | /contacts | List (search, pagination) |
| GET | /contacts/{id} | Get by ID |
| POST | /contacts | Create |
| PATCH | /contacts/{id} | Update |
| DELETE | /contacts/{id} | Delete (if no deals) |

### Deals (requires `X-Organization-Id` header)
| Method | Path | Description |
|--------|------|-------------|
| GET | /deals | List (filters, sorting) |
| GET | /deals/{id} | Get by ID |
| POST | /deals | Create |
| PATCH | /deals/{id} | Update (validates status/stage) |
| DELETE | /deals/{id} | Delete |

### Tasks (requires `X-Organization-Id` header)
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks | List (filters) |
| GET | /tasks/{id} | Get by ID |
| POST | /tasks | Create (validates due_date) |
| PATCH | /tasks/{id} | Update |
| DELETE | /tasks/{id} | Delete |

### Activities (requires `X-Organization-Id` header)
| Method | Path | Description |
|--------|------|-------------|
| GET | /deals/{id}/activities | Get timeline |
| POST | /deals/{id}/activities | Add comment |

### Analytics (requires `X-Organization-Id` header)
| Method | Path | Description |
|--------|------|-------------|
| GET | /analytics/deals/summary | Deals summary |
| GET | /analytics/deals/funnel | Sales funnel |

## Business Rules

1. **Cannot mark deal as `won` if amount ≤ 0**
2. **Cannot delete contact with existing deals** (409 Conflict)
3. **Members can only create tasks for their own deals**
4. **Task `due_date` cannot be in the past**
5. **Stage rollback only allowed for admin/owner**
6. **Status/stage changes automatically create Activity records**

## Roles & Permissions

| Role | Manage own | Manage all | Org settings |
|------|------------|------------|--------------|
| owner | ✅ | ✅ | ✅ |
| admin | ✅ | ✅ | ✅ |
| manager | ✅ | ✅ | ❌ |
| member | ✅ | ❌ | ❌ |
