"""Collection of API routers for the backend service."""

from fastapi import APIRouter

from app.api.routes import dictionary

api_router = APIRouter()
api_router.include_router(dictionary.router)

__all__ = ["api_router"]
