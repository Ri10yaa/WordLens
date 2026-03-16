"""Utilities for shaping third-party dictionary data into internal schemas."""

from typing import Dict, List

from app.models import EntriesByLanguageAndWord, Entry, Pronunciation, Sense, Source


def generate_sense_id(word: str, pos: str, index: int) -> str:
    return f"{word.lower()}.{pos.lower()}.{index:02d}"


def normalize_response(word: str, raw_data) -> EntriesByLanguageAndWord:
    entries_map: Dict[str, Entry] = {}

    for item in raw_data:
        meanings = item.get("meanings", [])
        phonetics = item.get("phonetics", [])

        pronunciations = [
            Pronunciation(type="ipa", text=ph["text"], tags=[])
            for ph in phonetics
            if "text" in ph
        ]

        for meaning in meanings:
            part_of_speech = meaning.get("partOfSpeech", "")

            new_senses: List[Sense] = []
            start_index = 1

            if part_of_speech in entries_map:
                start_index = len(entries_map[part_of_speech].senses) + 1

            for i, definition in enumerate(
                meaning.get("definitions", []), start=start_index
            ):
                sense = Sense(
                    sense_id=generate_sense_id(word, part_of_speech, i),
                    definition=definition.get("definition", ""),
                    partOfSpeech=part_of_speech,
                    examples=[definition["example"]] if "example" in definition else [],
                    tags=[],
                    synonyms=definition.get("synonyms", []),
                    antonyms=definition.get("antonyms", []),
                )
                new_senses.append(sense)

            if part_of_speech in entries_map:
                entries_map[part_of_speech].senses.extend(new_senses)
            else:
                entries_map[part_of_speech] = Entry(
                    partOfSpeech=part_of_speech,
                    pronunciations=pronunciations,
                    senses=new_senses,
                )

    return EntriesByLanguageAndWord(
        word=word,
        entries=list(entries_map.values()),
        source=Source(
            url=f"https://en.wiktionary.org/wiki/{word}",
        ),
    )
