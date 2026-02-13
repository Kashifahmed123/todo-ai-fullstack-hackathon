# Todo-AI Frontend (Phase II)

Next.js 16+ frontend with Better Auth, TanStack Query, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.x+
- **Authentication**: Better Auth with JWT plugin
- **State Management**: TanStack Query (React Query)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Package Manager**: pnpm

## Prerequisites

- Node.js 20+
- pnpm 9+

## Setup

1. **Install dependencies**:
   ```bash
   pnpm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your API URL and secrets
   ```

3. **Start development server**:
   ```bash
   pnpm dev
   ```

4. **Open browser**:
   - http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Landing page
│   │   ├── login/        # Login page
│   │   ├── register/     # Registration page
│   │   └── dashboard/    # Task dashboard (protected)
│   ├── components/       # React components
│   ├── lib/              # Utilities (auth, API client, types)
│   └── hooks/            # Custom React hooks
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
└── package.json          # Project configuration
```

## Scripts

```bash
# Development
pnpm dev              # Start dev server

# Build
pnpm build            # Build for production
pnpm start            # Start production server

# Testing
pnpm test             # Run unit tests
pnpm test:coverage    # Run tests with coverage
pnpm test:e2e         # Run E2E tests

# Linting
pnpm lint             # Run ESLint
```

## Environment Variables

See `.env.local.example` for required configuration:
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `BETTER_AUTH_SECRET`: Same secret as backend
- `BETTER_AUTH_URL`: Frontend URL
- `NODE_ENV`: Environment (development/production)

## Features

- **Authentication**: Register, login, logout with JWT
- **Protected Routes**: Automatic redirect to login for unauthenticated users
- **Task Management**: Create, read, update, delete tasks
- **Real-time Updates**: Optimistic UI updates with TanStack Query
- **Responsive Design**: Mobile-first with Tailwind CSS
- **Type Safety**: 100% TypeScript coverage

## Development Guidelines

- Use TypeScript strict mode (100% type coverage required)
- Follow Next.js App Router conventions
- Use Server Components by default, Client Components when needed
- Leverage TanStack Query for server state management
- Write tests before implementation (TDD)
- Use Tailwind CSS for styling (no custom CSS)

## Authentication Flow

1. User registers/logs in via Better Auth
2. Backend issues JWT token
3. Frontend stores token (httpOnly cookie or localStorage)
4. Token included in all API requests (Authorization header)
5. Protected routes check for valid token
6. Automatic redirect to login if unauthenticated
