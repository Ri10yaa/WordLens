"""Pydantic schemas shared across the backend service."""

from .schemas import (
    ContextualMeaningRequest,
    ContextualMeaningResponse,
    EntriesByLanguageAndWord,
    Entry,
    Pronunciation,
    Sense,
    Source,
)

__all__ = [
    "ContextualMeaningRequest",
    "ContextualMeaningResponse",
    "EntriesByLanguageAndWord",
    "Entry",
    "Pronunciation",
    "Sense",
    "Source",
]
