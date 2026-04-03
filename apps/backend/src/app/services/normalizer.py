"""Utilities for shaping third-party dictionary data into internal schemas."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from app.models import EntriesByLanguageAndWord, Entry, Pronunciation, Sense, Source

MW_TOKEN_REPLACEMENTS = {
    "bc": ": ",
    "ldquo": '"',
    "rdquo": '"',
    "lsquo": "'",
    "rsquo": "'",
    "it": "",
    "/it": "",
    "sc": "",
    "/sc": "",
    "b": "",
    "/b": "",
    "inf": "",
    "/inf": "",
}

TOKEN_PATTERN = re.compile(r"{([^}]+)}")


def clean_markup(text: str) -> str:
    if not text:
        return ""

    def _replace(match: re.Match[str]) -> str:
        inner = match.group(1)
        parts = inner.split("|")
        token = parts[0]
        if token in MW_TOKEN_REPLACEMENTS:
            return MW_TOKEN_REPLACEMENTS[token]
        if len(parts) > 1:
            return parts[-1]
        return ""

    cleaned = TOKEN_PATTERN.sub(_replace, text)
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def generate_sense_id(word: str, pos: str, index: int) -> str:
    safe_pos = pos or "unknown"
    return f"{word.lower()}.{safe_pos.lower()}.{index:02d}"


def _extract_pronunciations(entry: Dict[str, Any]) -> List[Pronunciation]:
    pronunciations: List[Pronunciation] = []
    hwi = entry.get("hwi") or {}
    for pr in hwi.get("prs", []):
        text = pr.get("mw") or pr.get("ipa")
        if not text:
            continue
        pronunciations.append(
            Pronunciation(
                type="merriam-webster",
                text=text,
                tags=[],
            )
        )
    return pronunciations


def _flatten_word_lists(collection: Iterable) -> List[str]:
    words: List[str] = []
    if not collection:
        return words
    for group in collection:
        if isinstance(group, list):
            for item in group:
                if isinstance(item, dict) and item.get("wd"):
                    words.append(item["wd"])
    return words


def _parse_dt(dt_items: Iterable) -> tuple[str, List[str]]:
    definition_fragments: List[str] = []
    examples: List[str] = []

    for entry in dt_items or []:
        if not isinstance(entry, list) or len(entry) < 2:
            continue
        dtype, value = entry[0], entry[1]

        if dtype == "text" and isinstance(value, str):
            cleaned = clean_markup(value)
            if cleaned:
                definition_fragments.append(cleaned)
        elif dtype == "vis" and isinstance(value, list):
            for vis in value:
                if not isinstance(vis, dict):
                    continue
                vis_text = clean_markup(vis.get("t", ""))
                if vis_text:
                    examples.append(vis_text)
        elif dtype in {"uns", "snote"} and isinstance(value, list):
            nested_definition, nested_examples = _parse_dt(value)
            if nested_definition:
                definition_fragments.append(nested_definition)
            examples.extend(nested_examples)

    definition = " ".join(definition_fragments).strip()
    return definition, examples


def _collect_senses_from_entry(
    word: str,
    part_of_speech: str,
    entry: Dict[str, Any],
    start_index: int,
) -> List[Sense]:
    senses: List[Sense] = []

    def _visit(node: Any):
        if isinstance(node, list):
            if node and isinstance(node[0], str) and node[0] == "sense" and len(node) >= 2:
                sense_data = node[1] or {}
                definition, examples = _parse_dt(sense_data.get("dt"))
                if not definition:
                    return
                synonyms = _flatten_word_lists(sense_data.get("syn_list"))
                antonyms = _flatten_word_lists(sense_data.get("ant_list"))
                tags = sense_data.get("sls", []) or []

                index = start_index + len(senses)
                senses.append(
                    Sense(
                        sense_id=generate_sense_id(word, part_of_speech, index),
                        definition=definition,
                        partOfSpeech=part_of_speech,
                        examples=examples,
                        tags=tags,
                        synonyms=synonyms,
                        antonyms=antonyms,
                    )
                )
            else:
                for item in node:
                    _visit(item)

    for definition_block in entry.get("def", []):
        if isinstance(definition_block, dict):
            _visit(definition_block.get("sseq"))

    return senses


def normalize_response(word: str, raw_data) -> EntriesByLanguageAndWord:
    entries_map: Dict[str, Entry] = {}

    for item in raw_data:
        if not isinstance(item, dict):
            continue

        part_of_speech = item.get("fl", "") or "unknown"
        pronunciations = _extract_pronunciations(item)

        start_index = 1
        if part_of_speech in entries_map:
            start_index = len(entries_map[part_of_speech].senses) + 1

        senses = _collect_senses_from_entry(word, part_of_speech, item, start_index)
        if not senses:
            continue

        if part_of_speech in entries_map:
            entries_map[part_of_speech].senses.extend(senses)
        else:
            entries_map[part_of_speech] = Entry(
                partOfSpeech=part_of_speech,
                pronunciations=pronunciations,
                senses=senses,
            )

    return EntriesByLanguageAndWord(
        word=word,
        entries=list(entries_map.values()),
        source=Source(url=f"https://www.merriam-webster.com/dictionary/{word}"),
    )
