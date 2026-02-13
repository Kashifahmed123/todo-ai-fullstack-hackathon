# API Contracts

**Feature**: 001-fullstack-web-app
**Date**: 2026-02-10
**Version**: 2.0.0

## Overview

This directory contains the API contract specifications for the Phase II Full-Stack Web Application. The contracts define the interface between the Next.js frontend and FastAPI backend.

## Files

- **openapi.yaml**: OpenAPI 3.1 specification defining all REST endpoints, request/response schemas, and authentication requirements

## Contract Format

We use OpenAPI 3.1 (formerly Swagger) as our API contract format because:
- FastAPI automatically generates OpenAPI specs from Python type hints
- Industry standard for REST APIs
- Enables automatic documentation generation (Swagger UI)
- Supports contract testing and validation
- Can generate TypeScript types for frontend

## Endpoints Summary

### Authentication Endpoints (Public)

| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/register | Register new user account |
| POST | /auth/login | Login and receive JWT token |
| GET | /auth/me | Get current user profile (protected) |

### Task Endpoints (Protected)

| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks | List all tasks for authenticated user |
| POST | /tasks | Create a new task |
| GET | /tasks/{task_id} | Get a specific task |
| PUT | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |
| POST | /tasks/{task_id}/toggle | Toggle task completion status |

## Authentication

All protected endpoints require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

**Token Acquisition**:
1. Register via POST /auth/register OR login via POST /auth/login
2. Receive `access_token` in response
3. Include token in Authorization header for all subsequent requests

**Token Format**:
```json
{
  "sub": "user_id",
  "exp": 1234567890
}
```

## Request/Response Examples

### Register User

**Request**:
```http
POST /auth/register HTTP/1.1
Content-Type: application/json

{
  "email": "alice@example.com",
  "password": "AlicePass123"
}
```

**Response** (201 Created):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create Task

**Request**:
```http
POST /tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-02-10T14:30:00Z",
  "updated_at": "2026-02-10T14:30:00Z"
}
```

### List Tasks

**Request**:
```http
GET /tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "user_id": 1,
    "created_at": "2026-02-10T14:30:00Z",
    "updated_at": "2026-02-10T14:30:00Z"
  },
  {
    "id": 2,
    "title": "Complete project report",
    "description": null,
    "completed": true,
    "user_id": 1,
    "created_at": "2026-02-09T10:15:00Z",
    "updated_at": "2026-02-10T12:00:00Z"
  }
]
```

### Toggle Task Completion

**Request**:
```http
POST /tasks/1/toggle HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-02-10T14:30:00Z",
  "updated_at": "2026-02-10T15:45:00Z"
}
```

## Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Human-readable error message",
  "type": "error_type",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

### Common HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, POST (non-creation) |
| 201 | Created | Successful POST (resource creation) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input (validation errors) |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists (e.g., duplicate email) |
| 422 | Unprocessable Entity | Semantic validation errors |
| 500 | Internal Server Error | Server-side error |

## Data Validation Rules

### Email
- Must be valid RFC 5322 format
- Maximum 255 characters
- Case-insensitive for uniqueness
- Example: `alice@example.com`

### Password (Pre-hash)
- Minimum 8 characters
- Maximum 100 characters
- Must contain: 1 uppercase, 1 lowercase, 1 digit
- Example: `AlicePass123`

### Task Title
- Minimum 1 character (after trimming)
- Maximum 200 characters
- Cannot be only whitespace
- Example: `Buy groceries`

### Task Description
- Optional (can be null)
- Maximum 5000 characters
- Example: `Milk, eggs, bread`

## Security Considerations

### Data Isolation
- All task endpoints automatically filter by authenticated user's ID
- Users can ONLY access their own tasks
- Attempting to access another user's task returns 403 Forbidden

### JWT Security
- Tokens signed with BETTER_AUTH_SECRET (shared between frontend and backend)
- Token expiration: 1 hour (configurable)
- User ID extracted from JWT `sub` claim, never from request parameters
- Invalid tokens return 401 Unauthorized

### Password Security
- Passwords hashed with bcrypt (12 rounds minimum)
- Plain text passwords NEVER stored or logged
- Password field NEVER returned in API responses

## Contract Testing

To validate API responses match this contract:

```bash
# Backend: Run contract tests
cd backend
pytest tests/contract/test_openapi.py

# Frontend: Generate TypeScript types from OpenAPI spec
cd frontend
npm run generate-types
```

## Interactive Documentation

When the backend is running, interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Browse all endpoints
- View request/response schemas
- Test endpoints directly in the browser
- See example requests and responses

## Versioning

API version: **2.0.0** (Phase II)

Version format: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes (incompatible with previous version)
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

## Future Enhancements (Phase III+)

Potential contract changes for future phases:
- Pagination for task lists (query parameters: `?page=1&limit=20`)
- Task filtering (query parameters: `?completed=true`)
- Task sorting (query parameters: `?sort=created_at&order=desc`)
- Task search (query parameters: `?q=groceries`)
- Batch operations (POST /tasks/batch)
- AI suggestions (GET /tasks/{task_id}/suggestions)

## Contact

For questions or issues with the API contract, refer to:
- Specification: `specs/001-fullstack-web-app/spec.md`
- Data Model: `specs/001-fullstack-web-app/data-model.md`
- Implementation Plan: `specs/001-fullstack-web-app/plan.md`
