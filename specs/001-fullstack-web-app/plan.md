# Implementation Plan: Phase II Full-Stack Web Application

**Branch**: `001-fullstack-web-app` | **Date**: 2026-02-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fullstack-web-app/spec.md`

## Summary

Migrate from Phase I console application to a multi-user full-stack web application with secure authentication and persistent storage. The system will support user registration, JWT-based authentication, and complete task CRUD operations with strict data isolation between users. Backend uses FastAPI with SQLModel ORM connecting to Neon PostgreSQL; frontend uses Next.js 16+ with Better Auth for authentication. All operations enforce user_id filtering to prevent cross-user data access.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x+ (frontend)
**Primary Dependencies**: FastAPI 0.115+, SQLModel 0.0.22+, Next.js 16+, Better Auth 1.x, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest (backend), Vitest/Jest (frontend), Playwright (E2E)
**Target Platform**: Web application (Linux/Docker for backend, modern browsers for frontend)
**Project Type**: Web application (monorepo with separate frontend and backend)
**Performance Goals**: <500ms p95 API response time, <2s page load, <100ms database queries, 100+ concurrent users
**Constraints**: 100% type coverage (Python type hints + TypeScript), JWT verification on all protected endpoints, mandatory user_id filtering on all queries
**Scale/Scope**: Multi-user system supporting 100+ concurrent users, 2 entities (User, Task), 4 user stories, RESTful API with 8+ endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

- ✅ **I. Spec-Driven Development (SDD)**: Following Spec-Kit Plus workflow with approved spec.md
- ✅ **II. Agentic Accountability**: PHR created for spec phase, will create for plan phase
- ✅ **III. Authoritative Hierarchy**: Constitution → CLAUDE.md → specs hierarchy maintained
- ✅ **IV. Multi-Tenancy & Security**: All queries filter by user_id, JWT verification mandatory
- ✅ **V. Stateless Execution**: Backend stateless, PostgreSQL for persistence (Kafka deferred to Phase V)
- ✅ **VI. Type Safety**: 100% type coverage required for both Python and TypeScript

### Technical Standards Compliance

**Backend Requirements**:
- ✅ Package manager: `uv` (mandatory)
- ✅ Validation: Pydantic V2 via SQLModel (mandatory)
- ✅ API format: RESTful JSON (mandatory)
- ✅ Python version: 3.13+ (mandatory)

**Frontend Requirements**:
- ✅ Language: TypeScript (mandatory, no JavaScript)
- ✅ Styling: Tailwind CSS (mandatory)
- ✅ Rendering: Server-Side Rendering (SSR) via Next.js 16+
- ✅ Type coverage: 100% (mandatory)

**DevOps Requirements**:
- ⏸️ Deployment: Helm-first (deferred to Phase IV)
- ⏸️ CI/CD: GitHub Actions (deferred to Phase IV)
- ⏸️ Container runtime: Docker (deferred to Phase IV)

### Quality & Compliance Gates

**Testing Requirements**:
- ✅ Automated testing MANDATORY for Phase II
- ✅ Target: 70% minimum coverage
- ✅ Unit tests for business logic
- ✅ Integration tests for API endpoints
- ✅ Contract tests for external interfaces
- ✅ E2E tests for critical user journeys (auth, task CRUD)

**Security Standards**:
- ✅ JWT-based authentication MANDATORY
- ✅ RBAC REQUIRED (basic user role for Phase II)
- ✅ Passwords hashed with bcrypt/argon2
- ✅ TLS/HTTPS for external communication
- ✅ No hardcoded secrets (environment variables)

**Performance Standards (Phase II)**:
- ✅ API response time: p95 < 500ms
- ✅ Database queries: < 100ms for simple CRUD
- ✅ Frontend initial load: < 3s

### Gate Status: ✅ PASSED

All constitutional requirements for Phase II are met. DevOps requirements (Helm, CI/CD, Docker) are appropriately deferred to Phase IV per the evolutionary roadmap.

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-web-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   ├── openapi.yaml     # OpenAPI 3.1 specification
│   └── README.md        # Contract documentation
├── checklists/
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (DB session, JWT verification)
│   │   ├── auth.py          # Auth endpoints (register, login)
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings (Pydantic BaseSettings)
│   │   ├── security.py      # Password hashing, JWT verification
│   │   └── database.py      # Database engine and session
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User request/response schemas
│   │   └── task.py          # Task request/response schemas
│   └── main.py              # FastAPI application entry point
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── unit/
│   │   ├── test_models.py
│   │   └── test_security.py
│   ├── integration/
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   └── contract/
│       └── test_openapi.py
├── pyproject.toml           # uv project configuration
├── .env.example             # Environment variables template
└── README.md

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/landing page
│   │   ├── login/
│   │   │   └── page.tsx     # Login page
│   │   ├── register/
│   │   │   └── page.tsx     # Registration page
│   │   └── dashboard/
│   │       └── page.tsx     # Task dashboard (protected)
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   ├── TaskList.tsx     # Task list component
│   │   ├── TaskItem.tsx     # Individual task component
│   │   └── TaskForm.tsx     # Task create/edit form
│   ├── lib/
│   │   ├── auth.ts          # Better Auth configuration
│   │   ├── api.ts           # API client with JWT handling
│   │   └── types.ts         # TypeScript type definitions
│   └── hooks/
│       ├── useTasks.ts      # Task data fetching hook
│       └── useAuth.ts       # Authentication hook
├── tests/
│   ├── unit/
│   │   └── components/
│   ├── integration/
│   │   └── api/
│   └── e2e/
│       ├── auth.spec.ts
│       └── tasks.spec.ts
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── .env.local.example
└── README.md

specs/                       # Feature specifications
.specify/                    # Spec-Kit Plus configuration
history/                     # Prompt History Records and ADRs
```

**Structure Decision**: Selected Option 2 (Web application) with monorepo structure. Backend and frontend are separate projects with independent dependency management (uv for Python, npm/pnpm for Node.js). This separation enables:
- Independent deployment and scaling
- Clear API contract boundaries
- Technology-specific tooling and testing
- Team specialization (backend vs frontend developers)

## Complexity Tracking

> **No violations detected** - All constitutional requirements are met without exceptions.

## Phase 0: Research Summary

*See [research.md](./research.md) for detailed findings*

### Key Technology Decisions

**1. Authentication Architecture**
- **Decision**: Better Auth (frontend) with JWT plugin + FastAPI JWT verification (backend)
- **Rationale**: Better Auth provides production-ready authentication with JWT support; FastAPI has excellent JWT libraries (python-jose, PyJWT)
- **Alternatives**: NextAuth.js (more complex setup), Auth0 (external dependency), custom JWT (reinventing wheel)

**2. Database ORM**
- **Decision**: SQLModel
- **Rationale**: Type-safe ORM built on SQLAlchemy and Pydantic, perfect for FastAPI integration, excellent TypeScript-like experience
- **Alternatives**: SQLAlchemy (more verbose), Tortoise ORM (less mature), raw SQL (no type safety)

**3. Frontend State Management**
- **Decision**: React hooks + SWR/TanStack Query for server state
- **Rationale**: Simple, built-in, sufficient for Phase II scope; server state library handles caching and revalidation
- **Alternatives**: Redux (overkill for Phase II), Zustand (adds dependency), Context API (performance concerns)

**4. Password Hashing**
- **Decision**: bcrypt via passlib
- **Rationale**: Industry standard, well-tested, built-in salt generation, adjustable work factor
- **Alternatives**: argon2 (newer but less ecosystem support), scrypt (less common)

**5. JWT Library**
- **Decision**: python-jose[cryptography]
- **Rationale**: FastAPI documentation standard, supports multiple algorithms, active maintenance
- **Alternatives**: PyJWT (simpler but fewer features), authlib (more complex)

### Integration Patterns

**Frontend → Backend Communication**:
- RESTful JSON API over HTTPS
- JWT in Authorization header: `Bearer <token>`
- CORS configured for local development (localhost:3000 → localhost:8000)
- Error responses follow RFC 7807 Problem Details format

**Database Connection**:
- Neon PostgreSQL connection string via environment variable
- SQLModel async engine with connection pooling
- Dependency injection for database sessions (FastAPI Depends)
- Automatic session cleanup via context managers

**Authentication Flow**:
1. User registers → Backend hashes password → Stores in DB
2. User logs in → Backend verifies password → Issues JWT with user_id claim
3. Frontend stores JWT → Includes in all API requests
4. Backend verifies JWT → Extracts user_id → Filters all queries

## Phase 1: Design Artifacts

*Detailed design documents generated in Phase 1*

- ✅ [data-model.md](./data-model.md) - Entity schemas and relationships
- ✅ [contracts/openapi.yaml](./contracts/openapi.yaml) - API contract specification
- ✅ [quickstart.md](./quickstart.md) - Development setup guide

## Architecture Decision Records

The following architectural decisions warrant ADR documentation:

1. **Monorepo Structure with Separate Frontend/Backend** - Significant structural decision affecting deployment and development workflow
2. **Better Auth + FastAPI JWT Architecture** - Cross-cutting authentication strategy with security implications
3. **SQLModel as ORM** - Data access pattern affecting all backend development

Suggested command: `/sp.adr "Monorepo Structure and Authentication Architecture"`

## Next Steps

1. ✅ Phase 0: Research completed (see research.md)
2. ✅ Phase 1: Design artifacts generated (data-model.md, contracts/, quickstart.md)
3. ⏭️ Phase 2: Run `/sp.tasks` to generate actionable task breakdown
4. ⏭️ Phase 3: Run `/sp.implement` to execute tasks

## Risk Mitigation Strategies

**Data Isolation Risk**:
- Mitigation: Create reusable dependency `get_current_user_id()` that all endpoints use
- Mitigation: Add integration tests that verify cross-user access is blocked
- Mitigation: Code review checklist item: "All queries include user_id filter"

**JWT Security Risk**:
- Mitigation: Use strong secret (32+ random bytes) stored in environment variables
- Mitigation: Set reasonable expiration (1 hour access token)
- Mitigation: Implement token refresh mechanism (deferred to future phase if needed)

**Database Performance Risk**:
- Mitigation: Add indexes on user_id and frequently queried fields
- Mitigation: Use connection pooling (SQLModel default)
- Mitigation: Monitor query performance with logging

**Session Management Risk**:
- Mitigation: Document JWT expiration strategy in quickstart.md
- Mitigation: Frontend handles 401 responses by redirecting to login
- Mitigation: Consider refresh tokens in future phase if UX issues arise
