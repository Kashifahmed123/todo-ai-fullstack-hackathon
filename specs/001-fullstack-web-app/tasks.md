# Tasks: Phase II Full-Stack Web Application

**Input**: Design documents from `/specs/001-fullstack-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Automated testing is MANDATORY per constitution (70% minimum coverage). Tests are included for all user stories.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow monorepo structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create monorepo directory structure (backend/, frontend/, specs/)
- [x] T002 [P] Initialize backend project with uv in backend/pyproject.toml
- [x] T003 [P] Initialize frontend project with pnpm in frontend/package.json
- [x] T004 [P] Create backend environment template in backend/.env.example
- [x] T005 [P] Create frontend environment template in frontend/.env.local.example
- [x] T006 [P] Configure TypeScript strict mode in frontend/tsconfig.json
- [x] T007 [P] Configure Tailwind CSS in frontend/tailwind.config.ts
- [x] T008 [P] Create backend README with setup instructions in backend/README.md
- [x] T009 [P] Create frontend README with setup instructions in frontend/README.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Install backend dependencies (FastAPI, SQLModel, python-jose, passlib, uvicorn) via uv in backend/
- [x] T011 Install frontend dependencies (Next.js 16+, Better Auth, TanStack Query, Tailwind) via pnpm in frontend/
- [x] T012 [P] Create database configuration in backend/src/core/database.py
- [x] T013 [P] Create settings configuration using Pydantic BaseSettings in backend/src/core/config.py
- [x] T014 [P] Implement password hashing utilities using passlib in backend/src/core/security.py
- [x] T015 [P] Implement JWT token creation and verification in backend/src/core/security.py
- [x] T016 Create database session dependency in backend/src/api/deps.py
- [x] T017 Create FastAPI application instance with CORS in backend/src/main.py
- [x] T018 [P] Create pytest configuration in backend/tests/conftest.py
- [x] T019 [P] Create test database fixtures in backend/tests/conftest.py
- [x] T020 [P] Setup Next.js app router structure in frontend/src/app/layout.tsx
- [x] T021 [P] Configure Better Auth with JWT plugin in frontend/src/lib/auth.ts
- [x] T022 [P] Create API client with JWT handling in frontend/src/lib/api.ts
- [x] T023 [P] Setup TanStack Query provider in frontend/src/app/layout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to register, login, and access protected routes with JWT authentication

**Independent Test**: Register a new account, logout, login again, and access dashboard

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T024 [P] [US1] Contract test for /auth/register endpoint in backend/tests/contract/test_auth_contract.py
- [x] T025 [P] [US1] Contract test for /auth/login endpoint in backend/tests/contract/test_auth_contract.py
- [x] T026 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py
- [x] T027 [P] [US1] Integration test for user login flow in backend/tests/integration/test_auth.py
- [x] T028 [P] [US1] Integration test for duplicate email rejection in backend/tests/integration/test_auth.py
- [x] T029 [P] [US1] Integration test for invalid credentials in backend/tests/integration/test_auth.py

### Implementation for User Story 1

- [x] T030 [P] [US1] Create User SQLModel in backend/src/models/user.py
- [x] T031 [P] [US1] Create UserRegister schema in backend/src/schemas/user.py
- [x] T032 [P] [US1] Create UserLogin schema in backend/src/schemas/user.py
- [x] T033 [P] [US1] Create UserResponse schema in backend/src/schemas/user.py
- [x] T034 [P] [US1] Create TokenResponse schema in backend/src/schemas/user.py
- [x] T035 [US1] Implement POST /auth/register endpoint in backend/src/api/auth.py
- [x] T036 [US1] Implement POST /auth/login endpoint in backend/src/api/auth.py
- [x] T037 [US1] Create get_current_user_id dependency in backend/src/api/deps.py
- [x] T038 [US1] Implement GET /auth/me endpoint in backend/src/api/auth.py
- [x] T039 [US1] Register auth router in backend/src/main.py
- [x] T040 [US1] Add email validation logic in backend/src/schemas/user.py
- [x] T041 [US1] Add password strength validation in backend/src/schemas/user.py
- [x] T042 [P] [US1] Create registration page UI in frontend/src/app/register/page.tsx
- [x] T043 [P] [US1] Create login page UI in frontend/src/app/login/page.tsx
- [x] T044 [P] [US1] Create useAuth hook in frontend/src/hooks/useAuth.ts
- [x] T045 [US1] Implement registration form logic in frontend/src/app/register/page.tsx
- [x] T046 [US1] Implement login form logic in frontend/src/app/login/page.tsx
- [x] T047 [US1] Add protected route middleware in frontend/src/middleware.ts
- [x] T048 [US1] Create landing page with auth links in frontend/src/app/page.tsx
- [x] T049 [US1] Add logout functionality in frontend/src/hooks/useAuth.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Creation and Management (Priority: P2)

**Goal**: Enable authenticated users to create, update, delete, and view their personal tasks

**Independent Test**: Login, create a task, edit it, delete it, verify data isolation

### Tests for User Story 2

- [x] T050 [P] [US2] Contract test for /tasks endpoints in backend/tests/contract/test_tasks_contract.py
- [x] T051 [P] [US2] Integration test for task creation in backend/tests/integration/test_tasks.py
- [x] T052 [P] [US2] Integration test for task update in backend/tests/integration/test_tasks.py
- [x] T053 [P] [US2] Integration test for task deletion in backend/tests/integration/test_tasks.py
- [x] T054 [P] [US2] Integration test for data isolation (cross-user access blocked) in backend/tests/integration/test_tasks.py
- [x] T055 [P] [US2] Integration test for task validation (empty title) in backend/tests/integration/test_tasks.py

### Implementation for User Story 2

- [x] T056 [P] [US2] Create Task SQLModel in backend/src/models/task.py
- [x] T057 [P] [US2] Create TaskCreate schema in backend/src/schemas/task.py
- [x] T058 [P] [US2] Create TaskUpdate schema in backend/src/schemas/task.py
- [x] T059 [P] [US2] Create TaskResponse schema in backend/src/schemas/task.py
- [x] T060 [US2] Implement GET /tasks endpoint with user_id filter in backend/src/api/tasks.py
- [x] T061 [US2] Implement POST /tasks endpoint in backend/src/api/tasks.py
- [x] T062 [US2] Implement GET /tasks/{task_id} endpoint with ownership check in backend/src/api/tasks.py
- [x] T063 [US2] Implement PUT /tasks/{task_id} endpoint with ownership check in backend/src/api/tasks.py
- [x] T064 [US2] Implement DELETE /tasks/{task_id} endpoint with ownership check in backend/src/api/tasks.py
- [x] T065 [US2] Register tasks router in backend/src/main.py
- [x] T066 [US2] Add task title validation (1-200 chars) in backend/src/schemas/task.py
- [x] T067 [US2] Add task description validation (max 5000 chars) in backend/src/schemas/task.py
- [x] T068 [P] [US2] Create TypeScript Task type in frontend/src/lib/types.ts
- [x] T069 [P] [US2] Create useTasks hook with TanStack Query in frontend/src/hooks/useTasks.ts
- [x] T070 [P] [US2] Create TaskForm component in frontend/src/components/TaskForm.tsx
- [x] T071 [P] [US2] Create TaskItem component in frontend/src/components/TaskItem.tsx
- [x] T072 [P] [US2] Create TaskList component in frontend/src/components/TaskList.tsx
- [x] T073 [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx
- [x] T074 [US2] Implement task creation UI in frontend/src/components/TaskForm.tsx
- [x] T075 [US2] Implement task editing UI in frontend/src/components/TaskItem.tsx
- [x] T076 [US2] Implement task deletion UI in frontend/src/components/TaskItem.tsx
- [x] T077 [US2] Add optimistic updates for task mutations in frontend/src/hooks/useTasks.ts
- [x] T078 [US2] Add error handling and validation messages in frontend/src/components/TaskForm.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Status Management (Priority: P3)

**Goal**: Enable users to toggle task completion status and visually distinguish completed tasks

**Independent Test**: Create a task, toggle completion status multiple times, verify persistence

### Tests for User Story 3

- [x] T079 [P] [US3] Integration test for task toggle in backend/tests/integration/test_tasks.py
- [x] T080 [P] [US3] Integration test for status persistence in backend/tests/integration/test_tasks.py

### Implementation for User Story 3

- [x] T081 [US3] Implement POST /tasks/{task_id}/toggle endpoint in backend/src/api/tasks.py
- [x] T082 [US3] Add toggle functionality to TaskItem component in frontend/src/components/TaskItem.tsx
- [x] T083 [US3] Add visual styling for completed tasks (strikethrough, opacity) in frontend/src/components/TaskItem.tsx
- [x] T084 [US3] Add optimistic toggle updates in frontend/src/hooks/useTasks.ts

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Task List Viewing and Filtering (Priority: P4)

**Goal**: Provide organized task list view with empty state and data isolation verification

**Independent Test**: Create multiple tasks, view list, verify organization and data isolation

### Tests for User Story 4

- [x] T085 [P] [US4] Integration test for task list retrieval in backend/tests/integration/test_tasks.py
- [x] T086 [P] [US4] Integration test for empty task list in backend/tests/integration/test_tasks.py

### Implementation for User Story 4

- [x] T087 [US4] Add empty state UI to TaskList component in frontend/src/components/TaskList.tsx
- [x] T088 [US4] Add loading state UI to TaskList component in frontend/src/components/TaskList.tsx
- [x] T089 [US4] Add task count display to dashboard in frontend/src/app/dashboard/page.tsx
- [x] T090 [US4] Optimize task list rendering for multiple tasks in frontend/src/components/TaskList.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T091 [P] Add comprehensive error handling to all API endpoints in backend/src/api/
- [x] T092 [P] Add request logging middleware in backend/src/main.py
- [x] T093 [P] Add database indexes for performance in backend/src/models/
- [ ] T094 [P] Create unit tests for security utilities in backend/tests/unit/test_security.py
- [ ] T095 [P] Create unit tests for models in backend/tests/unit/test_models.py
- [ ] T096 [P] Add E2E test for complete auth flow in frontend/tests/e2e/auth.spec.ts
- [ ] T097 [P] Add E2E test for complete task CRUD flow in frontend/tests/e2e/tasks.spec.ts
- [ ] T098 [P] Add responsive design improvements for mobile in frontend/src/components/
- [ ] T099 [P] Add accessibility improvements (ARIA labels, keyboard navigation) in frontend/src/components/
- [x] T100 [P] Update backend README with API documentation in backend/README.md
- [x] T101 [P] Update frontend README with component documentation in frontend/README.md
- [ ] T102 Run quickstart.md validation to verify setup instructions
- [x] T103 Verify 70% test coverage target met (pytest --cov, vitest --coverage)
- [ ] T104 Run security audit (npm audit, safety check) and fix vulnerabilities
- [x] T105 Verify all user_id filters present in database queries (code review)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires US1 for authentication context but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US2 task model but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Enhances US2 task viewing but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services/endpoints
- Backend endpoints before frontend components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models/schemas within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for /auth/register endpoint in backend/tests/contract/test_auth_contract.py"
Task: "Contract test for /auth/login endpoint in backend/tests/contract/test_auth_contract.py"
Task: "Integration test for user registration flow in backend/tests/integration/test_auth.py"

# Launch all models/schemas for User Story 1 together:
Task: "Create User SQLModel in backend/src/models/user.py"
Task: "Create UserRegister schema in backend/src/schemas/user.py"
Task: "Create UserLogin schema in backend/src/schemas/user.py"
Task: "Create UserResponse schema in backend/src/schemas/user.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 105
- Phase 1 (Setup): 9 tasks
- Phase 2 (Foundational): 14 tasks (BLOCKING)
- Phase 3 (US1 - Auth): 26 tasks (6 tests + 20 implementation)
- Phase 4 (US2 - Task CRUD): 29 tasks (6 tests + 23 implementation)
- Phase 5 (US3 - Status): 6 tasks (2 tests + 4 implementation)
- Phase 6 (US4 - Viewing): 6 tasks (2 tests + 4 implementation)
- Phase 7 (Polish): 15 tasks

**Parallel Opportunities**: 47 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- US1: Register, logout, login, access dashboard
- US2: Login, create task, edit task, delete task
- US3: Create task, toggle status multiple times
- US4: Create multiple tasks, view organized list

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 49 tasks
