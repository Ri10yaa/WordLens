"""FastAPI routes that expose dictionary functionality."""

from fastapi import APIRouter, HTTPException

from app.infrastructure.cache import cache_word, get_cached_word
from app.infrastructure.dictionary_api import fetch_word_data
from app.models import (
    ContextualMeaningRequest,
    ContextualMeaningResponse,
    EntriesByLanguageAndWord,
)
from app.services.normalizer import normalize_response
from app.services.sense_selection import select_best_sense

router = APIRouter(tags=["Dictionary"])


@router.get("/define/{word}")
def define_word(word: str) -> EntriesByLanguageAndWord:
    raw_data = fetch_word_data(word)

    if not raw_data:
        raise HTTPException(status_code=404, detail=f"Word '{word}' not found")

    normalized = normalize_response(word=word, raw_data=raw_data)
    cache_word(word=word, normalized_data=normalized.model_dump())
    return normalized


@router.post("/tools/define_contextual", response_model=ContextualMeaningResponse)
def define_contextual(payload: ContextualMeaningRequest):
    cached = get_cached_word(payload.word)
    if cached:
        normalized = EntriesByLanguageAndWord.model_validate(cached)
    else:
        raw = fetch_word_data(payload.word)
        if not raw:
            raise HTTPException(status_code=404, detail=f"Word '{payload.word}' not found")

        normalized = normalize_response(payload.word, raw)
        cache_word(payload.word, normalized.model_dump())

    all_senses = []
    for entry in normalized.entries:
        for sense in entry.senses:
            sense.partOfSpeech = entry.partOfSpeech
            all_senses.append(sense)

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
