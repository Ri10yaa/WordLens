"""Adapters for third-party dictionary APIs."""

import requests

from app.core.config import settings


def fetch_word_data(word: str):
    response = requests.get(f"{settings.free_dictionary_url}{word}")
    if response.status_code != 200:
        return None
    return response.json()
