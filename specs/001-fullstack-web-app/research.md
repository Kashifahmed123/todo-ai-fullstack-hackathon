# Research: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Date**: 2026-02-10
**Phase**: 0 (Research & Technology Selection)

## Overview

This document captures the research and technology selection process for migrating from Phase I console application to Phase II full-stack web application with authentication and persistent storage.

## Research Questions

1. How to implement secure JWT-based authentication between Next.js frontend and FastAPI backend?
2. What ORM provides the best type safety for FastAPI + PostgreSQL?
3. How to structure a monorepo with separate frontend and backend?
4. What authentication library works best with Next.js 16+ and JWT?
5. How to ensure data isolation in a multi-tenant system?

## Technology Research

### 1. Authentication Architecture

**Research Question**: How to implement secure JWT-based authentication between Next.js frontend and FastAPI backend?

**Options Evaluated**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Better Auth + python-jose | Production-ready, JWT plugin support, FastAPI standard | Requires coordination of shared secret | ✅ **Selected** |
| NextAuth.js + FastAPI JWT | Popular in Next.js ecosystem | More complex setup, v5 breaking changes | ❌ Rejected |
| Auth0 | Fully managed, enterprise features | External dependency, cost, overkill for Phase II | ❌ Rejected |
| Custom JWT implementation | Full control | Reinventing wheel, security risks | ❌ Rejected |

**Decision**: Better Auth (frontend) with JWT plugin + python-jose (backend)

**Rationale**:
- Better Auth provides production-ready authentication with minimal configuration
- JWT plugin generates standard JWT tokens that FastAPI can verify
- python-jose is the FastAPI documentation standard for JWT handling
- Shared secret (BETTER_AUTH_SECRET) enables symmetric verification
- No external dependencies or third-party services required

**Implementation Pattern**:
```
1. Frontend: Better Auth issues JWT with user_id claim
2. Frontend: Stores JWT in httpOnly cookie or localStorage
3. Frontend: Includes JWT in Authorization header: "Bearer <token>"
4. Backend: Verifies JWT signature using shared secret
5. Backend: Extracts user_id from JWT payload
6. Backend: Uses user_id to filter all database queries
```

**Security Considerations**:
- Shared secret must be 32+ random bytes
- JWT expiration set to 1 hour (configurable)
- HTTPS required in production
- Token refresh mechanism deferred to future phase

---

### 2. Database ORM Selection

**Research Question**: What ORM provides the best type safety for FastAPI + PostgreSQL?

**Options Evaluated**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| SQLModel | Type-safe, Pydantic integration, FastAPI-native | Newer, smaller ecosystem | ✅ **Selected** |
| SQLAlchemy 2.0 | Mature, feature-rich, large ecosystem | More verbose, separate Pydantic models | ❌ Rejected |
| Tortoise ORM | Async-first, Django-like | Less mature, smaller community | ❌ Rejected |
| Raw SQL | Full control, no abstraction | No type safety, manual query building | ❌ Rejected |

**Decision**: SQLModel

**Rationale**:
- Built on SQLAlchemy Core + Pydantic V2 = best of both worlds
- Single model definition serves as both ORM model and Pydantic schema
- Excellent type inference and IDE support
- Perfect integration with FastAPI (same author)
- Async support via SQLAlchemy async engine
- Reduces code duplication (no separate ORM and schema models)

**Example Usage**:
```python
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str | None = None
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### 3. Frontend State Management

**Research Question**: How to manage server state and authentication state in Next.js?

**Options Evaluated**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| React hooks + TanStack Query | Simple, built-in, excellent caching | Requires additional library | ✅ **Selected** |
| Redux Toolkit | Powerful, predictable | Overkill for Phase II, boilerplate | ❌ Rejected |
| Zustand | Lightweight, simple API | Adds dependency, less ecosystem | ❌ Rejected |
| Context API only | No dependencies | Performance issues, no caching | ❌ Rejected |

**Decision**: React hooks + TanStack Query (React Query)

**Rationale**:
- React hooks (useState, useEffect) sufficient for local UI state
- TanStack Query handles server state (tasks, user data) with automatic caching
- Built-in request deduplication and background refetching
- Optimistic updates for better UX
- Minimal learning curve
- Can be replaced with Redux later if complexity grows

**State Categories**:
- **Local UI State**: Form inputs, modals, loading states → React hooks
- **Server State**: Tasks, user profile → TanStack Query
- **Auth State**: JWT token, user session → Better Auth + React Context

---

### 4. Password Hashing

**Research Question**: What password hashing algorithm should be used?

**Options Evaluated**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| bcrypt (via passlib) | Industry standard, adjustable work factor | Slower than modern alternatives | ✅ **Selected** |
| argon2 | Winner of password hashing competition | Less ecosystem support in Python | ❌ Rejected |
| scrypt | Good security properties | Less common, fewer libraries | ❌ Rejected |
| PBKDF2 | NIST approved | Weaker than bcrypt/argon2 | ❌ Rejected |

**Decision**: bcrypt via passlib

**Rationale**:
- Industry standard with 20+ years of battle-testing
- Excellent Python support via passlib library
- Automatic salt generation
- Adjustable work factor (rounds) for future-proofing
- FastAPI documentation uses bcrypt as example
- Sufficient security for Phase II (can migrate to argon2 later if needed)

**Configuration**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Default rounds: 12 (good balance of security and performance)
```

---

### 5. JWT Library Selection

**Research Question**: Which JWT library should FastAPI use?

**Options Evaluated**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| python-jose[cryptography] | FastAPI standard, multiple algorithms | Slightly heavier | ✅ **Selected** |
| PyJWT | Simpler, lightweight | Fewer features, less FastAPI integration | ❌ Rejected |
| authlib | Comprehensive OAuth/JWT library | Overkill, more complex | ❌ Rejected |

**Decision**: python-jose[cryptography]

**Rationale**:
- Official FastAPI documentation uses python-jose
- Supports multiple JWT algorithms (HS256, RS256, etc.)
- Includes cryptography backend for better performance
- Active maintenance and security updates
- Well-tested in production environments

**Usage Pattern**:
```python
from jose import JWTError, jwt

# Encode
token = jwt.encode({"sub": user_id}, SECRET_KEY, algorithm="HS256")

# Decode and verify
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
user_id = payload.get("sub")
```

---

### 6. Monorepo Structure

**Research Question**: How to structure a monorepo with separate frontend and backend?

**Options Evaluated**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Separate directories (backend/, frontend/) | Simple, clear separation | Manual coordination | ✅ **Selected** |
| Turborepo/Nx monorepo tools | Shared tooling, caching | Overkill for 2 projects | ❌ Rejected |
| Single package.json with workspaces | Unified dependencies | Mixes Python and Node.js | ❌ Rejected |

**Decision**: Separate directories with independent dependency management

**Rationale**:
- Clear separation of concerns
- Independent deployment and scaling
- Technology-specific tooling (uv for Python, pnpm for Node.js)
- No need for monorepo tools with only 2 projects
- Easier for developers to work on one side without affecting the other

**Directory Structure**:
```
/
├── backend/          # Python 3.13+ with uv
│   ├── pyproject.toml
│   └── src/
├── frontend/         # Next.js 16+ with pnpm
│   ├── package.json
│   └── src/
└── specs/            # Shared documentation
```

---

### 7. API Contract Format

**Research Question**: How to document and validate API contracts?

**Options Evaluated**:

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| OpenAPI 3.1 (Swagger) | FastAPI auto-generation, industry standard | Verbose YAML | ✅ **Selected** |
| GraphQL | Type-safe, flexible queries | Overkill, learning curve | ❌ Rejected |
| gRPC | High performance, type-safe | Not web-friendly, complex | ❌ Rejected |

**Decision**: OpenAPI 3.1 (auto-generated by FastAPI)

**Rationale**:
- FastAPI automatically generates OpenAPI spec from Python type hints
- Interactive documentation (Swagger UI) at /docs endpoint
- Contract testing via generated spec
- Frontend can generate TypeScript types from OpenAPI spec
- Industry standard for REST APIs

---

## Integration Patterns

### Frontend → Backend Communication

**Pattern**: RESTful JSON API with JWT authentication

**Flow**:
1. User action in frontend (e.g., create task)
2. Frontend calls API client function
3. API client adds JWT to Authorization header
4. Backend receives request, verifies JWT
5. Backend extracts user_id from JWT
6. Backend executes operation with user_id filter
7. Backend returns JSON response
8. Frontend updates UI

**Error Handling**:
- 401 Unauthorized → Redirect to login
- 403 Forbidden → Show error message
- 422 Validation Error → Show field-specific errors
- 500 Server Error → Show generic error message

**CORS Configuration**:
```python
# Development
origins = ["http://localhost:3000"]

# Production
origins = [os.getenv("FRONTEND_URL")]
```

---

### Database Connection Pattern

**Pattern**: Async SQLModel with dependency injection

**Implementation**:
```python
# database.py
engine = create_async_engine(DATABASE_URL)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

# API endpoint
@app.get("/tasks")
async def get_tasks(
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    result = await session.exec(
        select(Task).where(Task.user_id == user_id)
    )
    return result.all()
```

**Benefits**:
- Automatic session cleanup
- Connection pooling
- Type-safe queries
- Testable (can inject mock session)

---

## Best Practices Identified

### Security Best Practices

1. **Never trust client input**: Always extract user_id from JWT, never from request body/params
2. **Filter all queries**: Every database query MUST include user_id filter
3. **Hash passwords**: Use bcrypt with automatic salt generation
4. **Secure secrets**: Store BETTER_AUTH_SECRET in environment variables, never in code
5. **HTTPS only**: Enforce HTTPS in production (JWT tokens in transit)
6. **Token expiration**: Set reasonable JWT expiration (1 hour recommended)

### Code Organization Best Practices

1. **Separation of concerns**: Models, schemas, API routes, business logic in separate modules
2. **Dependency injection**: Use FastAPI Depends for database sessions and auth
3. **Type hints everywhere**: 100% type coverage for both Python and TypeScript
4. **Reusable dependencies**: Create `get_current_user_id()` dependency used by all protected endpoints
5. **Environment configuration**: Use Pydantic BaseSettings for type-safe config

### Testing Best Practices

1. **Test pyramid**: Many unit tests, fewer integration tests, few E2E tests
2. **Test data isolation**: Each test creates its own user and tasks
3. **Mock external dependencies**: Mock database in unit tests, use test database in integration tests
4. **Contract testing**: Validate API responses match OpenAPI spec
5. **Security testing**: Verify cross-user access is blocked

---

## Unresolved Questions

None. All technical decisions have been made with sufficient confidence for Phase II implementation.

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Better Auth Documentation: https://www.better-auth.com/
- Next.js 16 Documentation: https://nextjs.org/docs
- TanStack Query: https://tanstack.com/query/latest
- python-jose: https://python-jose.readthedocs.io/
- passlib: https://passlib.readthedocs.io/

---

## Next Steps

Proceed to Phase 1: Generate design artifacts (data-model.md, contracts/, quickstart.md)
