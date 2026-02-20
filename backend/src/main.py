"""
FastAPI application entry point.

Main application with CORS configuration and router registration.
"""

import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .core.database import init_db


# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes database on startup.
    """
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: cleanup if needed


# Create FastAPI application
app = FastAPI(
    title="Todo-AI Phase III API",
    description="RESTful API for multi-user task management with AI chatbot",
    version="3.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing information."""
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.3f}s"
    )

    return response


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Todo-AI Phase III API",
        "version": "3.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Register routers
from .api import auth, tasks, chat

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
