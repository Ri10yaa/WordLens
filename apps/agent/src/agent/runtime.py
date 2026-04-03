"""High level helpers to run the dictionary agent using Hugging Face embeddings."""

from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer, util

from agent.config import settings
from agent.tools import fetch_literal_senses


@lru_cache
def get_encoder() -> SentenceTransformer:
    return SentenceTransformer(settings.hf_model_name)


def run_agent(word: str, sentence: str) -> str:
    literal = fetch_literal_senses(word)
    if "error" in literal:
        return literal["error"]

    senses = literal.get("senses", [])
    if not senses:
        return f"No senses available for {word}."

    encoder = get_encoder()
    sentence_embedding = encoder.encode(sentence, convert_to_tensor=True)

    best_sense = None
    best_score = -1.0
    for sense in senses:
        sense_embedding = encoder.encode(sense["definition"], convert_to_tensor=True)
        score = util.cos_sim(sentence_embedding, sense_embedding).item()
        if score > best_score:
            best_score = score
            best_sense = sense

    if not best_sense:
        return "Unable to determine contextual meaning."

    explanation = (
        f"Sense {best_sense['sense_id']} ({best_sense['partOfSpeech']}): {best_sense['definition']}\n"
        f"Reasoning: the sentence talks about '{sentence}', which aligns with this definition"
        f" (similarity score {best_score:.2f})."
    )
    return explanation
