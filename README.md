# Phase II: Todo Full-Stack Web Application

> Professional full-stack Todo application built for Governor Sindh AI Course Hackathon - Quarter 4b

![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![React](https://img.shields.io/badge/React-19-blue?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.13-yellow?style=flat-square&logo=python)

## ✨ Features

### Frontend
- 🎨 **Professional Dark Theme** - Modern UI with gradient backgrounds and glassmorphic effects
- 🎭 **Animated Backgrounds** - Blob animations, floating particles, and grid patterns
- 🔐 **Password Visibility Toggle** - Enhanced UX for authentication forms
- 📱 **Responsive Design** - Works seamlessly on all devices
- ⚡ **Micro-interactions** - Smooth hover effects, scale transforms, and rotations
- 🎯 **Custom Components** - Beautiful task cards with custom checkboxes

### Backend
- 🔒 **JWT Authentication** - Secure user authentication with token-based auth
- 🗄️ **SQLite Database** - Async database operations with SQLModel
- 🚀 **FastAPI** - High-performance async API
- ✅ **Input Validation** - Comprehensive request/response validation
- 🔄 **CORS Support** - Configured for Next.js frontend

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 16 (App Router)
- **UI Library:** React 19
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** React Query (TanStack Query)
- **HTTP Client:** Axios

### Backend
- **Framework:** FastAPI
- **ORM:** SQLModel
- **Database:** SQLite (async with aiosqlite)
- **Authentication:** JWT with passlib bcrypt
- **Validation:** Pydantic v2

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and pnpm
- Python 3.13+
- Git

### Backend Setup

```bash
cd backend

# Install dependencies using uv
uv sync --all-extras

# Create .env file
cp .env.example .env

# Run the server
uv run uvicorn src.main:app --reload --port 8005
```

The backend will be available at `http://localhost:8005`

### Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Create .env.local file
cp .env.local.example .env.local

# Run the development server
pnpm dev
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
├── backend/
│   ├── src/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   └── schemas/      # Pydantic schemas
│   └── tests/            # Backend tests
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js app router pages
│   │   ├── components/   # React components
│   │   └── hooks/        # Custom React hooks
│   └── public/           # Static assets
└── specs/                # Project specifications
```

## 🎯 Key Features Showcase

### Animated Dark Theme
- Gradient orbs with blob animations
- Floating particles with staggered delays
- Grid pattern overlay
- Glassmorphic cards with backdrop blur

### Authentication
- Secure JWT-based authentication
- Password hashing with bcrypt
- Token refresh mechanism
- Protected routes

### Task Management
- Create, read, update, delete tasks
- Mark tasks as complete/incomplete
- Task filtering (active/completed)
- Real-time updates

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite+aiosqlite:///./test.db
BETTER_AUTH_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8005
```

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8005/docs`
- ReDoc: `http://localhost:8005/redoc`

## 🧪 Testing

### Backend Tests
```bash
cd backend
uv run pytest
```

## 🎨 Design Highlights

- **Color Palette:** Dark grays with indigo, purple, and pink accents
- **Typography:** Clean, modern fonts with proper hierarchy
- **Animations:** Smooth transitions with custom keyframes
- **Spacing:** Consistent padding and margins throughout
- **Shadows:** Layered shadows for depth perception

## 🏆 Built For

Governor Sindh AI Course - Quarter 4b Hackathon

## 📄 License

This project is built for educational purposes as part of the Governor Sindh AI Course.

## 🤝 Contributing

This is a hackathon project. Feel free to fork and experiment!

## 📧 Contact

Built with ❤️ by Kashif Ahmed

---

**Note:** This is a Phase II implementation featuring a complete full-stack architecture with modern UI/UX design patterns.