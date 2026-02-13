<!--
Sync Impact Report:
- Version: NEW → 1.0.0 (Initial constitution)
- Modified principles: N/A (initial creation)
- Added sections: All sections (initial creation)
- Removed sections: None
- Templates requiring updates:
  ✅ .specify/templates/spec-template.md (reviewed - compatible)
  ✅ .specify/templates/plan-template.md (reviewed - compatible)
  ✅ .specify/templates/tasks-template.md (reviewed - compatible)
- Follow-up TODOs: None
-->

# Todo-AI Ecosystem Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

The agent MUST strictly follow the Spec-Kit Plus workflow. No file modification or creation is permitted without a corresponding entry in `/specs` and an approved `/sp.plan`.

**Rationale**: Ensures all changes are intentional, documented, and traceable. Prevents ad-hoc modifications that bypass architectural review and testing requirements.

### II. Agentic Accountability

Every modification MUST generate a Prompt History Record (PHR). The agent MUST maintain the `history/prompts/` directory as a verbatim audit trail of the project's evolution.

**Rationale**: Creates complete traceability of all decisions and changes. Enables learning from past interactions and provides accountability for autonomous agent actions.

### III. Authoritative Hierarchy

The project follows a three-level authority structure:
- **Level 1**: `constitution.md` (Project Laws) - Non-negotiable principles
- **Level 2**: `CLAUDE.md` (Operational Instructions) - Agent behavior and workflows
- **Level 3**: `@specs/` (Functional Blueprints) - Feature-specific requirements

**Rationale**: Clear precedence prevents conflicts and ensures consistent decision-making across all project activities.

### IV. Multi-Tenancy & Security

All data access MUST be filtered by `user_id`. JWT verification is MANDATORY for all REST and MCP operations. No exceptions.

**Rationale**: Security-first architecture prevents data leakage between users. Essential for production deployment and compliance requirements.

### V. Stateless Execution

The Backend and AI Agents MUST remain stateless. Persistence is delegated to PostgreSQL; event-state is delegated to Kafka.

**Rationale**: Enables horizontal scaling, simplifies deployment, and ensures system resilience. Stateless services can be restarted or scaled without data loss.

### VI. Type Safety

100% Type Hints (Python) and 100% TypeScript coverage are MANDATORY. No untyped code is permitted in production.

**Rationale**: Catches errors at compile-time, improves IDE support, serves as living documentation, and reduces runtime errors significantly.

## Evolutionary Roadmap

The Todo-AI Ecosystem evolves through five distinct phases, each building on the previous:

### Phase I: Baseline
Python 3.13+ Console Application with In-Memory storage.

**Deliverables**: Core todo CRUD operations, CLI interface, basic validation.

### Phase II: Scaling
Transition to Monorepo. FastAPI backend, Next.js 16+ frontend, Neon PostgreSQL (SQLModel), and Better Auth (JWT).

**Deliverables**: Web UI, persistent storage, user authentication, RESTful API.

### Phase III: Intelligence
Integration of OpenAI Agents SDK and a stateless MCP Server for natural language task orchestration.

**Deliverables**: AI-powered task management, natural language interface, intelligent task suggestions.

### Phase IV: Cloud-Native
Containerization via Gordon (Docker AI) and local Kubernetes orchestration via Helm and Minikube.

**Deliverables**: Container images, Helm charts, local K8s deployment, CI/CD pipelines.

### Phase V: Advanced Infrastructure
Event-Driven Architecture using Kafka (Strimzi/Redpanda) and Dapr distributed runtime on AKS/GKE.

**Deliverables**: Event streaming, distributed tracing, cloud deployment, production-grade observability.

## Technical Standards

### Tech Stack Rigor

**Backend Requirements**:
- Package manager: `uv` (mandatory)
- Validation: Pydantic V2 (mandatory)
- API format: RESTful JSON (mandatory)
- Python version: 3.13+ (mandatory)

**Frontend Requirements**:
- Language: TypeScript (mandatory, no JavaScript)
- Styling: Tailwind CSS (mandatory)
- Rendering: Server-Side Rendering (SSR) via Next.js 16+
- Type coverage: 100% (mandatory)

**DevOps Requirements**:
- Deployment: Helm-first (mandatory for Phase IV+)
- CI/CD: GitHub Actions (mandatory)
- Container runtime: Docker (mandatory for Phase IV+)

**Rationale**: Standardized stack reduces cognitive load, improves maintainability, and ensures team members can work across all components.

## Quality & Compliance

### Documentation Standards

Automatic generation of Architecture Decision Records (ADRs) is REQUIRED for all significant architectural decisions. ADRs MUST include:
- Context and problem statement
- Decision drivers
- Considered options
- Decision outcome
- Consequences (positive and negative)

### Testing Requirements

**Phase I**: Manual testing acceptable for console application.

**Phase II+**: Automated testing MANDATORY:
- Unit tests for business logic
- Integration tests for API endpoints
- Contract tests for external interfaces
- E2E tests for critical user journeys

**Coverage targets**:
- Phase II: 70% minimum
- Phase III+: 80% minimum
- Critical paths: 100% (authentication, data persistence, payment flows if applicable)

### Security Standards

**Authentication**: JWT-based authentication MANDATORY for Phase II+.

**Authorization**: Role-Based Access Control (RBAC) REQUIRED for Phase II+.

**Data Protection**:
- All passwords MUST be hashed (bcrypt/argon2)
- Sensitive data MUST be encrypted at rest (Phase III+)
- TLS/HTTPS MANDATORY for all external communication (Phase II+)

**Secrets Management**:
- NO hardcoded secrets (enforced via pre-commit hooks)
- Environment variables for local development
- Secret management service for production (Phase IV+)

### Performance Standards

**Phase I**: No specific requirements (console application).

**Phase II**:
- API response time: p95 < 500ms
- Database queries: < 100ms for simple CRUD
- Frontend initial load: < 3s

**Phase III+**:
- API response time: p95 < 200ms
- AI agent response: < 5s for simple queries
- Event processing latency: < 1s

**Phase V**:
- Event throughput: 10,000 events/second minimum
- System availability: 99.9% uptime SLO

## Governance

### Amendment Process

1. Proposed changes MUST be documented in an ADR
2. Changes MUST be reviewed and approved by project lead
3. Migration plan REQUIRED for breaking changes
4. All dependent templates and documentation MUST be updated
5. Version number MUST be incremented according to semantic versioning

### Compliance Verification

All pull requests MUST verify compliance with this constitution:
- Automated checks via pre-commit hooks
- Manual review checklist in PR template
- Constitution violations MUST be justified in PR description

### Complexity Justification

Any violation of simplicity principles (e.g., adding 4th project when constitution limits to 3, introducing unnecessary abstractions) MUST be justified with:
- Clear problem statement
- Why simpler alternatives are insufficient
- Long-term maintenance plan

### Version Control

**Version**: 1.0.0
**Ratified**: 2026-02-10
**Last Amended**: 2026-02-10

**Versioning Rules**:
- MAJOR: Backward-incompatible governance changes or principle removals
- MINOR: New principles added or material expansions
- PATCH: Clarifications, wording improvements, non-semantic refinements
