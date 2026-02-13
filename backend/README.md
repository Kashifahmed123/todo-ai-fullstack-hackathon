# Todo-AI Backend (Phase II)

FastAPI backend with SQLModel ORM, JWT authentication, and Neon PostgreSQL.

## Tech Stack

- **Python**: 3.13+
- **Framework**: FastAPI 0.115+
- **ORM**: SQLModel 0.0.22+
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Package Manager**: uv

## Prerequisites

- Python 3.13+
- uv package manager
- Neon PostgreSQL database (or local PostgreSQL)

## Setup

1. **Install dependencies**:
   ```bash
   uv pip install -e .
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and secrets
   ```

3. **Run database migrations**:
   ```bash
   # SQLModel will auto-create tables on first run
   python -m src.main
   ```

4. **Start development server**:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── models/       # SQLModel database models
│   ├── schemas/      # Pydantic request/response schemas
│   ├── api/          # API endpoints
│   ├── core/         # Core utilities (config, security, database)
│   └── main.py       # FastAPI application
├── tests/
│   ├── unit/         # Unit tests
│   ├── integration/  # Integration tests
│   └── contract/     # Contract tests
└── pyproject.toml    # Project configuration
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/integration/test_auth.py
```

## Environment Variables

See `.env.example` for required configuration:
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: 32+ character secret for JWT signing
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `JWT_EXPIRATION_MINUTES`: Token expiration (default: 60)
- `FRONTEND_URL`: Frontend URL for CORS

## Security

- All passwords are hashed with bcrypt (12 rounds minimum)
- JWT tokens signed with BETTER_AUTH_SECRET
- All protected endpoints require valid JWT
- User ID extracted from JWT, never from request parameters
- All database queries filtered by user_id

## Development

- Use type hints for all functions (100% coverage required)
- Follow FastAPI best practices
- Use dependency injection for database sessions
- Write tests before implementation (TDD)
