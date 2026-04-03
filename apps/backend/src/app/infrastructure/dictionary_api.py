"""Adapters for third-party dictionary APIs."""

from typing import Any, Optional

import requests

from app.core.config import settings


def fetch_word_data(word: str) -> Optional[Any]:
    response = requests.get(
        f"{settings.dictionary_api_url}{word}",
        params={"key": settings.dictionary_api_key},
        timeout=10,
    )
    if response.status_code != 200:
        return None
    return response.json()
