from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.auth.router import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifecycle management."""
    logger.info("Application initialization...")
    yield
    logger.info("Application shutdown...")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="FastAPI Starter Template",
        description=(
            "Starter template with integrated SQLAlchemy 2 for developing FastAPI applications with advanced "
            "architecture, including authorization, authentication, and user role management."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Mount static files
    app.mount(
        '/static',
        StaticFiles(directory='app/static'),
        name='static'
    )

    # Register routers
    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Register application routers."""
    root_router = APIRouter()

    @root_router.get("/", tags=["root"])
    def home_page():
        return {
            "message": "Welcome to FastAPI Starter Template",
            "version": "1.0.0",
            "docs": "/docs"
        }

    app.include_router(root_router, tags=["root"])
    app.include_router(router_auth, prefix='/auth', tags=['Auth'])


app = create_app()
