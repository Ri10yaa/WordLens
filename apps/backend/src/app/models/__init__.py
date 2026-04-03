"""Pydantic schemas shared across the backend service."""

from .schemas import (
    ContextualMeaningRequest,
    ContextualMeaningResponse,
    EntriesByLanguageAndWord,
    Entry,
    LiteralSensesResponse,
    Pronunciation,
    Sense,
    Source,
    WordLookupRequest,
)

__all__ = [
    "ContextualMeaningRequest",
    "ContextualMeaningResponse",
    "EntriesByLanguageAndWord",
    "Entry",
    "LiteralSensesResponse",
    "Pronunciation",
    "Sense",
    "Source",
    "WordLookupRequest",
]
