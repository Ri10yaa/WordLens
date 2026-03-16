"""Shared Pydantic contract for contextual meaning responses."""

from typing import Optional

from pydantic import BaseModel


class ContextualMeaningResponse(BaseModel):
    word: str
    definition: Optional[str]
    confidence: float
    sense_id: Optional[str]
