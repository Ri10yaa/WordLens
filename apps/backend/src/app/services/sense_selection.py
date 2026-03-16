"""Logic for selecting the best word sense based on context."""

from functools import lru_cache
from typing import List, Tuple

import numpy as np
import spacy
import torch
from sentence_transformers import CrossEncoder, SentenceTransformer

from app.models import Sense


@lru_cache
def get_nlp():
    return spacy.load("en_core_web_sm")


@lru_cache
def get_semantic_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@lru_cache
def get_cross_encoder():
    return CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def select_best_sense(sentence: str, target_word: str, senses: List[Sense]) -> Tuple[Sense, float]:
    if not senses:
        return None, 0.0

    doc = get_nlp()(sentence)
    detected_pos = next((t.pos_ for t in doc if t.text.lower() == target_word.lower()), None)
    candidates = [s for s in senses if s.partOfSpeech.upper() == detected_pos] or senses

    domain_triggers = {
        "FINANCE": ["deposit", "money", "account", "withdraw", "bank", "interest", "stock", "capital"],
        "GEOGRAPHY": ["river", "shore", "water", "flow", "stream", "mountain", "sea", "earth"],
        "TECH": ["memory", "data", "storage", "software", "hardware", "process", "digital"],
        "LEGAL": ["court", "judge", "trial", "law", "case", "brief", "sentence"],
    }

    raw_scores = []
    sentence_low = sentence.lower()
    semantic_model = get_semantic_model()
    cross_encoder = get_cross_encoder()

    sentence_embedding = semantic_model.encode(
        sentence,
        normalize_embeddings=True,
    )

    for sense in candidates:
        definition_low = sense.definition.lower()
        pair = [sentence, f"[{sense.partOfSpeech}] {sense.definition}"]
        cross_score = cross_encoder.predict(pair)
        definition_embedding = semantic_model.encode(
            sense.definition,
            normalize_embeddings=True,
        )
        similarity = float(np.dot(sentence_embedding, definition_embedding))
        score = cross_score + similarity

        for keywords in domain_triggers.values():
            sentence_in_domain = any(kw in sentence_low for kw in keywords)
            def_in_domain = any(kw in definition_low for kw in keywords)

            if sentence_in_domain and def_in_domain:
                score += 5.0
            elif sentence_in_domain and "slang" in definition_low:
                score -= 3.0

        raw_scores.append(score)

    probs = torch.nn.functional.softmax(torch.tensor(raw_scores), dim=0).tolist()
    best_idx = int(np.argmax(probs))
    return candidates[best_idx], round(float(probs[best_idx]), 3)
