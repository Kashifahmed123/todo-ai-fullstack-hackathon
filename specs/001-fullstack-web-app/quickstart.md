# Quickstart Guide: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Date**: 2026-02-10
**Audience**: Developers setting up local development environment

## Overview

This guide walks you through setting up the Phase II Full-Stack Web Application for local development. You'll have a working backend (FastAPI + PostgreSQL) and frontend (Next.js) running on your machine.

**Time to complete**: ~15 minutes

## Prerequisites

### Required Software

- **Python 3.13+**: [Download](https://www.python.org/downloads/)
- **Node.js 20+**: [Download](https://nodejs.org/)
- **uv** (Python package manager): Install via `pip install uv`
- **pnpm** (Node.js package manager): Install via `npm install -g pnpm`
- **Git**: [Download](https://git-scm.com/)
- **PostgreSQL** (or Neon account): [Neon Signup](https://neon.tech/)

### Verify Installations

```bash
python --version    # Should be 3.13+
node --version      # Should be 20+
uv --version        # Should be installed
pnpm --version      # Should be installed
git --version       # Should be installed
```

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd Todo-App-Final
git checkout 001-fullstack-web-app
```

## Step 2: Database Setup (Neon PostgreSQL)

### Option A: Neon Serverless PostgreSQL (Recommended)

1. Sign up at [neon.tech](https://neon.tech/)
2. Create a new project: "todo-ai-dev"
3. Copy the connection string (looks like: `postgresql://user:pass@host/dbname`)
4. Save for Step 3

### Option B: Local PostgreSQL

```bash
# Install PostgreSQL (if not already installed)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql
# Windows: Download from postgresql.org

# Start PostgreSQL service
# macOS: brew services start postgresql
# Ubuntu: sudo service postgresql start
# Windows: Start via Services app

# Create database
createdb todo_ai_dev

# Connection string: postgresql://localhost/todo_ai_dev
```

## Step 3: Backend Setup

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Environment File

Create `.env` file in `backend/` directory:

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
```

**`.env` contents**:
```env
# Database
DATABASE_URL=postgresql://user:pass@host/dbname  # Your Neon or local connection string

# Security
BETTER_AUTH_SECRET=your-32-character-random-secret-here-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# CORS (for local development)
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Generate BETTER_AUTH_SECRET**:
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use online generator: https://generate-secret.vercel.app/32
```

### 3.3 Install Dependencies

```bash
# Initialize uv project
uv init

# Install dependencies
uv pip install fastapi uvicorn sqlmodel psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart pydantic-settings

# Install dev dependencies
uv pip install pytest pytest-asyncio httpx
```

**Or use pyproject.toml** (if provided):
```bash
uv pip install -e .
```

### 3.4 Run Database Migrations

```bash
# Create tables (SQLModel will auto-create on first run)
# Or run migration script if provided
python -m src.core.database
```

### 3.5 Start Backend Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or use the run script
python -m src.main
```

**Verify backend is running**:
- Open browser: http://localhost:8000/docs
- You should see Swagger UI with API documentation

## Step 4: Frontend Setup

### 4.1 Navigate to Frontend Directory

```bash
# Open new terminal
cd frontend
```

### 4.2 Create Environment File

Create `.env.local` file in `frontend/` directory:

```bash
# Copy example file
cp .env.local.example .env.local

# Edit .env.local with your values
```

**`.env.local` contents**:
```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-32-character-random-secret-here-same-as-backend
BETTER_AUTH_URL=http://localhost:3000

# Environment
NODE_ENV=development
```

**⚠️ CRITICAL**: `BETTER_AUTH_SECRET` MUST be the same value as in backend `.env`

### 4.3 Install Dependencies

```bash
# Install all dependencies
pnpm install

# Or use npm
npm install
```

**Key dependencies installed**:
- Next.js 16+
- React 19+
- TypeScript
- Tailwind CSS
- Better Auth
- TanStack Query
- Lucide Icons

### 4.4 Start Frontend Server

```bash
# Development mode with hot reload
pnpm dev

# Or use npm
npm run dev
```

**Verify frontend is running**:
- Open browser: http://localhost:3000
- You should see the landing page

## Step 5: Verify Setup

### 5.1 Test Backend API

```bash
# Health check
curl http://localhost:8000/

# Register a test user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123"}'

# Expected response: {"access_token":"...", "token_type":"bearer"}
```

### 5.2 Test Frontend

1. Open http://localhost:3000
2. Click "Register" or "Sign Up"
3. Create account: `test@example.com` / `TestPass123`
4. You should be redirected to dashboard
5. Create a test task: "Buy groceries"
6. Verify task appears in list

### 5.3 Test Data Isolation

1. Open incognito/private browser window
2. Register different user: `test2@example.com` / `TestPass456`
3. Create a task in second user's account
4. Switch back to first user
5. Verify you CANNOT see second user's task ✅

## Development Workflow

### Running Both Servers

**Terminal 1 (Backend)**:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
pnpm dev
```

### Accessing Services

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Next.js application |
| Backend API | http://localhost:8000 | FastAPI REST API |
| API Docs (Swagger) | http://localhost:8000/docs | Interactive API documentation |
| API Docs (ReDoc) | http://localhost:8000/redoc | Alternative API documentation |

### Hot Reload

Both servers support hot reload:
- **Backend**: Changes to Python files automatically reload server
- **Frontend**: Changes to TypeScript/React files automatically refresh browser

## Common Issues & Solutions

### Issue: "Module not found" (Backend)

**Solution**:
```bash
cd backend
uv pip install -e .
```

### Issue: "Cannot connect to database"

**Solution**:
1. Verify DATABASE_URL in `.env` is correct
2. Check Neon dashboard - database should be active
3. Test connection:
```bash
psql $DATABASE_URL
```

### Issue: "CORS error" in browser console

**Solution**:
1. Verify FRONTEND_URL in backend `.env` matches frontend URL
2. Restart backend server after changing `.env`

### Issue: "Invalid token" or "Unauthorized"

**Solution**:
1. Verify BETTER_AUTH_SECRET is IDENTICAL in both `.env` files
2. Logout and login again to get fresh token
3. Check browser console for token errors

### Issue: Port already in use

**Solution**:
```bash
# Find process using port 8000 (backend)
lsof -i :8000
kill -9 <PID>

# Find process using port 3000 (frontend)
lsof -i :3000
kill -9 <PID>
```

### Issue: "Cannot find module 'better-auth'"

**Solution**:
```bash
cd frontend
pnpm install better-auth
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/integration/test_auth.py

# Run specific test
pytest tests/integration/test_auth.py::test_register_user
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
pnpm test

# Run E2E tests (requires backend running)
pnpm test:e2e

# Run with coverage
pnpm test:coverage
```

## Database Management

### View Database Contents

```bash
# Connect to database
psql $DATABASE_URL

# List tables
\dt

# View users
SELECT * FROM "user";

# View tasks
SELECT * FROM task;

# Exit
\q
```

### Reset Database

```bash
# Drop all tables
psql $DATABASE_URL -c "DROP TABLE IF EXISTS task, user CASCADE;"

# Restart backend to recreate tables
uvicorn src.main:app --reload
```

### Seed Test Data

```bash
cd backend
python scripts/seed_data.py  # If seed script provided
```

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL connection string |
| BETTER_AUTH_SECRET | Yes | - | 32+ character secret for JWT signing |
| JWT_ALGORITHM | No | HS256 | JWT signing algorithm |
| JWT_EXPIRATION_MINUTES | No | 60 | Token expiration time |
| FRONTEND_URL | Yes | - | Frontend URL for CORS |
| ENVIRONMENT | No | development | Environment name |

### Frontend (.env.local)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| NEXT_PUBLIC_API_URL | Yes | - | Backend API URL |
| BETTER_AUTH_SECRET | Yes | - | Same as backend secret |
| BETTER_AUTH_URL | Yes | - | Frontend URL |
| NODE_ENV | No | development | Node environment |

## Next Steps

After completing setup:

1. ✅ Verify both servers are running
2. ✅ Test user registration and login
3. ✅ Test task CRUD operations
4. ✅ Verify data isolation between users
5. ⏭️ Review [data-model.md](./data-model.md) for entity schemas
6. ⏭️ Review [contracts/openapi.yaml](./contracts/openapi.yaml) for API endpoints
7. ⏭️ Run `/sp.tasks` to generate implementation tasks
8. ⏭️ Run `/sp.implement` to start development

## Troubleshooting Resources

- **Backend Logs**: Check terminal running uvicorn
- **Frontend Logs**: Check browser console (F12)
- **Database Logs**: Check Neon dashboard or PostgreSQL logs
- **API Documentation**: http://localhost:8000/docs
- **Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)

## Development Tips

### Backend Development

- Use FastAPI's automatic validation (Pydantic models)
- Add type hints to all functions
- Use dependency injection for database sessions
- Test endpoints via Swagger UI at /docs
- Use `print()` or `logging` for debugging

### Frontend Development

- Use TypeScript strict mode
- Leverage TanStack Query for server state
- Use React DevTools for component debugging
- Test responsive design (mobile + desktop)
- Use browser Network tab to debug API calls

### Database Development

- Always filter queries by user_id
- Use indexes for frequently queried fields
- Test with multiple users to verify isolation
- Use transactions for multi-step operations
- Monitor query performance in logs

## Security Checklist

Before deploying to production:

- [ ] Change BETTER_AUTH_SECRET to strong random value
- [ ] Enable HTTPS (TLS/SSL certificates)
- [ ] Update CORS origins to production domain
- [ ] Set secure cookie flags (httpOnly, secure, sameSite)
- [ ] Enable rate limiting on auth endpoints
- [ ] Add request logging and monitoring
- [ ] Review and test all user_id filters
- [ ] Run security audit (npm audit, safety check)
- [ ] Set up database backups
- [ ] Configure environment-specific secrets

## Support

For issues or questions:
- Check [spec.md](./spec.md) for requirements
- Check [plan.md](./plan.md) for architecture decisions
- Check [data-model.md](./data-model.md) for entity schemas
- Check [contracts/README.md](./contracts/README.md) for API details
- Review error messages in terminal/console
- Search existing issues in repository

---

**Happy coding! 🚀**
