"""Data contracts used by the AI Dictionary backend."""

from typing import List, Optional

from pydantic import BaseModel, Field


class Pronunciation(BaseModel):
    type: str = Field(..., description="Pronunciation system (e.g. ipa, enpr)")
    text: str = Field(..., description="Pronunciation text")
    tags: List[str] = Field(default_factory=list, description="Dialect or usage tags")


class Sense(BaseModel):
    sense_id: str
    definition: str = Field(..., description="Definition of this sense")
    partOfSpeech: str = Field(..., description="Part of speech (noun, verb, etc.)")
    examples: List[str] = Field(default_factory=list, description="Example sentences")
    tags: List[str] = Field(default_factory=list, description="Usage tags")
    synonyms: List[str] = Field(default_factory=list, description="Sense-level synonyms")
    antonyms: List[str] = Field(default_factory=list, description="Sense-level antonyms")


class Entry(BaseModel):
    partOfSpeech: str = Field(..., description="Part of speech (noun, verb, etc.)")
    pronunciations: Optional[List[Pronunciation]] = Field(
        default_factory=list,
        description="Pronunciations for this word",
    )
    senses: List[Sense]


class Source(BaseModel):
    url: str = Field(..., description="Original dictionary source URL")


class EntriesByLanguageAndWord(BaseModel):
    word: str = Field(..., description="The word being looked up")
    entries: List[Entry]
    source: Source


class ContextualMeaningRequest(BaseModel):
    word: str
    sentence: str = ""


class ContextualMeaningResponse(BaseModel):
    word: str
    definition: Optional[str]
    confidence: float
    sense_id: Optional[str]


class WordLookupRequest(BaseModel):
    word: str


class LiteralSensesResponse(BaseModel):
    word: str
    senses: List[Sense]
