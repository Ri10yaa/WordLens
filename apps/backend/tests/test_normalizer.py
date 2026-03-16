from app.models import Sense
from app.services.normalizer import normalize_response
from app.services import sense_selection


def test_normalize_response_groups_senses_by_part_of_speech():
    raw = [
        {
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {"definition": "A financial institution", "example": "Bank loan"},
                        {"definition": "The edge of a river"},
                    ],
                }
            ],
            "phonetics": [{"text": "bæŋk"}],
        }
    ]

    normalized = normalize_response("bank", raw)

    assert normalized.word == "bank"
    assert len(normalized.entries) == 1
    assert normalized.entries[0].partOfSpeech == "noun"
    assert len(normalized.entries[0].senses) == 2


def test_select_best_sense_returns_candidate_when_available(monkeypatch):
    senses = [
        Sense(
            sense_id="bank.n.01",
            definition="A financial institution that accepts deposits",
            partOfSpeech="NOUN",
            examples=[],
            tags=[],
            synonyms=[],
            antonyms=[],
        ),
        Sense(
            sense_id="bank.n.02",
            definition="The side of a river",
            partOfSpeech="NOUN",
            examples=[],
            tags=[],
            synonyms=[],
            antonyms=[],
        ),
    ]

    class DummyEncoder:
        def encode(self, text, normalize_embeddings=True):  # noqa: ARG002
            return [1.0, 0.0] if "deposit" in text else [0.0, 1.0]

    class DummyCross:
        def predict(self, pair):  # noqa: ARG002
            return 2.0

    monkeypatch.setattr(sense_selection, "get_semantic_model", lambda: DummyEncoder())
    monkeypatch.setattr(sense_selection, "get_cross_encoder", lambda: DummyCross())
    monkeypatch.setattr(sense_selection, "get_nlp", lambda: lambda text: [])

    best_sense, confidence = sense_selection.select_best_sense(
        sentence="She deposited money in the bank",
        target_word="bank",
        senses=senses,
    )

    assert best_sense is not None
    assert best_sense.sense_id == "bank.n.01"
    assert 0 <= confidence <= 1
