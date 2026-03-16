"""Tool definitions that call the backend API."""

from typing import Any, Dict, Optional

import requests

from agent.config import settings


def define_contextual(word: str, sentence: Optional[str] = None) -> Dict[str, Any]:
    payload = {"word": word, "sentence": sentence or ""}

    try:
        response = requests.post(
            f"{settings.backend_url}/tools/define_contextual",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        return {"error": f"Backend error: {exc}"}
