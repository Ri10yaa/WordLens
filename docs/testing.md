# Testing Checklist

## Backend

- `pytest` in `apps/backend` (covers normalization + sense selection).
- `uvicorn app.main:app` then hit `/health` and `/define/test`.
- Optional: run `docker compose up` to ensure Redis + API boot inside containers.

## Chrome Extension

- `npm run build` in `apps/extension`.
- Load `dist` as unpacked extension, confirm background worker has no errors.
- Highlight a word, trigger context menu, verify floating dialog shows cached/remote responses.

## LLM Agent

- Provide mock backend by exporting `BACKEND_URL` pointing to running API.
- `python -m agent.cli "Explain the meaning of bank when I deposited money"` should call backend and print contextual meaning.
