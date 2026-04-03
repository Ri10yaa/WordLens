"""FastAPI routes that expose dictionary functionality."""

from fastapi import APIRouter, HTTPException

from app.infrastructure.cache import cache_word, get_cached_word
from app.infrastructure.dictionary_api import fetch_word_data
from app.models import (
    ContextualMeaningRequest,
    ContextualMeaningResponse,
    EntriesByLanguageAndWord,
    LiteralSensesResponse,
    WordLookupRequest,
)
from app.services.normalizer import normalize_response
from app.services.sense_selection import select_best_sense

router = APIRouter(tags=["Dictionary"])


def _load_normalized_word(word: str) -> EntriesByLanguageAndWord:
    cached = get_cached_word(word)
    if cached:
        return EntriesByLanguageAndWord.model_validate(cached)

    raw = fetch_word_data(word)
    if not raw:
        raise HTTPException(status_code=404, detail=f"Word '{word}' not found")

    normalized = normalize_response(word=word, raw_data=raw)
    cache_word(word=word, normalized_data=normalized.model_dump())
    return normalized


def _collect_senses(normalized: EntriesByLanguageAndWord):
    senses = []
    for entry in normalized.entries:
        for sense in entry.senses:
            sense.partOfSpeech = entry.partOfSpeech
            senses.append(sense)
    return senses


@router.get("/define/{word}")
def define_word(word: str) -> EntriesByLanguageAndWord:
    return _load_normalized_word(word)


@router.post("/tools/list_senses", response_model=LiteralSensesResponse)
def list_senses(payload: WordLookupRequest):
    normalized = _load_normalized_word(payload.word)
    senses = _collect_senses(normalized)

    if not senses:
        raise HTTPException(status_code=404, detail=f"Word '{payload.word}' has no senses")

    return {"word": payload.word, "senses": senses}


@router.post("/tools/define_contextual", response_model=ContextualMeaningResponse)
def define_contextual(payload: ContextualMeaningRequest):
    normalized = _load_normalized_word(payload.word)
    all_senses = _collect_senses(normalized)

    if not all_senses:
        raise HTTPException(status_code=400, detail="No senses found for word")

    best_sense, confidence = select_best_sense(
        sentence=payload.sentence,
        target_word=payload.word,
        senses=all_senses,
    )

    return {
        "word": payload.word,
        "definition": best_sense.definition if best_sense else None,
        "confidence": float(confidence),
        "sense_id": best_sense.sense_id if best_sense else None,
    }
