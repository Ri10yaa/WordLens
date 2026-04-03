"""Tool definitions that call the backend API."""

from typing import Any, Dict

import requests

from agent.config import settings


def fetch_literal_senses(word: str) -> Dict[str, Any]:
    payload = {"word": word}

    try:
        response = requests.post(
            f"{settings.backend_url}/tools/list_senses",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        return {"error": f"Backend error: {exc}"}
