# Data Model: Phase II Full-Stack Web Application

**Feature**: 001-fullstack-web-app
**Date**: 2026-02-10
**Phase**: 1 (Design)

## Overview

This document defines the data entities, their attributes, relationships, and validation rules for the Phase II full-stack web application. The data model supports multi-user task management with secure authentication and strict data isolation.

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ hashed_password │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N (owns)
         │
         ▼
┌─────────────────┐
│      Task       │
├─────────────────┤
│ id (PK)         │
│ title           │
│ description     │
│ completed       │
│ user_id (FK)    │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## Entities

### User

**Purpose**: Represents an authenticated user account in the system.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| email | String(255) | UNIQUE, NOT NULL, INDEX | User's email address (login identifier) |
| hashed_password | String(255) | NOT NULL | Bcrypt-hashed password (never store plain text) |
| created_at | DateTime | NOT NULL, DEFAULT NOW() | Account creation timestamp |

**Validation Rules**:
- Email MUST match RFC 5322 email format
- Email MUST be unique across all users
- Password MUST be at least 8 characters before hashing
- Password MUST contain at least one uppercase, one lowercase, one digit (enforced at API level)
- Hashed password MUST use bcrypt with minimum 12 rounds

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email` (for login lookups)

**Relationships**:
- One User has many Tasks (1:N)

**Security Considerations**:
- Password is NEVER returned in API responses
- Email is case-insensitive for uniqueness checks
- User ID is extracted from JWT, never from request parameters

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**TypeScript Type**:
```typescript
interface User {
  id: number;
  email: string;
  created_at: string; // ISO 8601 format
  // Note: hashed_password is NEVER exposed to frontend
}
```

---

### Task

**Purpose**: Represents a todo item owned by a single user.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| title | String(200) | NOT NULL | Task title (required) |
| description | Text | NULL | Optional detailed description |
| completed | Boolean | NOT NULL, DEFAULT FALSE | Completion status |
| user_id | Integer | FOREIGN KEY(User.id), NOT NULL, INDEX | Owner of the task |
| created_at | DateTime | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | DateTime | NOT NULL, DEFAULT NOW(), ON UPDATE NOW() | Last modification timestamp |

**Validation Rules**:
- Title MUST NOT be empty or only whitespace
- Title MUST be 1-200 characters after trimming
- Description MAY be NULL or empty
- Description MUST be ≤ 5000 characters if provided
- Completed MUST be boolean (true/false)
- User ID MUST reference an existing user
- User ID MUST match the authenticated user's ID (enforced at API level)

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for filtering tasks by user)
- COMPOSITE INDEX on `(user_id, created_at)` (for sorted task lists)

**Relationships**:
- Many Tasks belong to one User (N:1)

**Business Rules**:
- Tasks are ALWAYS filtered by user_id in all queries
- Users can ONLY access their own tasks
- Deleting a user SHOULD cascade delete all their tasks (deferred to future phase)
- Tasks cannot be shared or transferred between users (Phase II scope)

**State Transitions**:
```
[Created] → completed = false
    ↓
[Toggle] → completed = true
    ↓
[Toggle] → completed = false
    ↓
[Deleted] → removed from database
```

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, min_length=1)
    description: str | None = Field(default=None, max_length=5000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional, for ORM convenience)
    # user: User = Relationship(back_populates="tasks")
```

**TypeScript Type**:
```typescript
interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: number;
  created_at: string; // ISO 8601 format
  updated_at: string; // ISO 8601 format
}
```

---

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_user_email ON user(email);

-- Tasks table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id INTEGER NOT NULL REFERENCES user(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_user_created ON task(user_id, created_at);

-- Trigger to update updated_at on task modification (PostgreSQL)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_task_updated_at BEFORE UPDATE ON task
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## Request/Response Schemas

### User Schemas

**UserRegister** (Request):
```python
class UserRegister(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=100)
```

**UserLogin** (Request):
```python
class UserLogin(BaseModel):
    email: str
    password: str
```

**UserResponse** (Response):
```python
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
```

**TokenResponse** (Response):
```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

---

### Task Schemas

**TaskCreate** (Request):
```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
```

**TaskUpdate** (Request):
```python
class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    completed: bool | None = None
```

**TaskResponse** (Response):
```python
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
```

---

## Data Validation Rules

### Email Validation
- Format: RFC 5322 compliant
- Case-insensitive for uniqueness
- Maximum length: 255 characters
- Example valid: `user@example.com`, `user+tag@example.co.uk`
- Example invalid: `user@`, `@example.com`, `user space@example.com`

### Password Validation (Pre-hash)
- Minimum length: 8 characters
- Maximum length: 100 characters (before hashing)
- Must contain: 1 uppercase, 1 lowercase, 1 digit
- Optional: Special characters allowed but not required
- Example valid: `Password123`, `MySecure1Pass`
- Example invalid: `pass`, `password`, `PASSWORD123`

### Task Title Validation
- Minimum length: 1 character (after trimming whitespace)
- Maximum length: 200 characters
- Must not be only whitespace
- Example valid: `Buy groceries`, `Complete project report`
- Example invalid: ``, `   ` (whitespace only)

### Task Description Validation
- Optional (can be NULL or empty string)
- Maximum length: 5000 characters
- No minimum length requirement
- Whitespace-only descriptions are allowed (treated as empty)

---

## Migration Strategy

### Initial Migration (Phase II)

1. Create `user` table with indexes
2. Create `task` table with foreign key and indexes
3. Create trigger for `updated_at` auto-update
4. Seed test data (optional, for development only)

### Future Migrations (Phase III+)

Potential schema changes for future phases:
- Add `user.role` for RBAC (Phase III)
- Add `task.priority` for task prioritization (Phase III)
- Add `task.due_date` for deadlines (Phase III)
- Add `task.tags` for categorization (Phase III)
- Add `task.ai_suggestions` for AI features (Phase III)

---

## Data Isolation Strategy

**Critical Security Requirement**: All task queries MUST filter by `user_id`.

**Implementation Pattern**:
```python
# ✅ CORRECT: Always filter by user_id
async def get_user_tasks(user_id: int, session: AsyncSession):
    result = await session.exec(
        select(Task).where(Task.user_id == user_id)
    )
    return result.all()

# ❌ INCORRECT: Missing user_id filter (security vulnerability!)
async def get_all_tasks(session: AsyncSession):
    result = await session.exec(select(Task))
    return result.all()  # Exposes all users' tasks!
```

**Enforcement Mechanisms**:
1. Reusable dependency `get_current_user_id()` extracts user_id from JWT
2. All protected endpoints use this dependency
3. Integration tests verify cross-user access is blocked
4. Code review checklist includes "user_id filter present"

---

## Performance Considerations

### Indexes
- `user.email`: Speeds up login queries
- `task.user_id`: Speeds up task list queries (most common operation)
- `task.(user_id, created_at)`: Composite index for sorted task lists

### Query Optimization
- Use `select()` with explicit columns instead of `SELECT *`
- Limit result sets (pagination deferred to future phase)
- Use connection pooling (SQLModel default)

### Expected Query Performance
- User login: <10ms (indexed email lookup)
- Task list: <50ms (indexed user_id filter, <100 tasks per user)
- Task create/update/delete: <20ms (single row operation)

---

## Testing Data

### Test Users
```python
test_user_1 = {
    "email": "alice@example.com",
    "password": "AlicePass123"
}

test_user_2 = {
    "email": "bob@example.com",
    "password": "BobSecure456"
}
```

### Test Tasks
```python
test_task_1 = {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": False,
    "user_id": 1
}

test_task_2 = {
    "title": "Complete project report",
    "description": None,
    "completed": True,
    "user_id": 1
}
```

---

## Next Steps

1. Generate OpenAPI contract from these schemas
2. Implement SQLModel models in `backend/src/models/`
3. Create database migration scripts
4. Write unit tests for model validation
5. Write integration tests for data isolation
