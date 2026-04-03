# AI Dictionary Agent

Monorepo housing three coordinated apps:

- `apps/backend` – FastAPI service that ranks dictionary senses with SentenceTransformer + CrossEncoder logic and caches results in Redis.
- `apps/extension` – Manifest V3 Chrome overlay that lets users request contextual definitions on any webpage.
- `apps/agent` – Hugging Face embedding client that fetches literal senses from the backend and scores them against the user's sentence.

Shared contracts live in `packages/shared`, while architecture notes and runbooks live under `docs/`.

## Quick Start

| Task | Command |
| --- | --- |
| Install shared venv | `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python -m spacy download en_core_web_sm` |
| Run backend locally | `cd apps/backend && PYTHONPATH=src uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` |
| Build extension | `cd apps/extension && npm install && npm run build` |
| Run agent CLI | `cd apps/agent && python -m agent.cli bank "I deposited money in the bank"` |

See the per-app READMEs for detailed setup, Docker instructions, and tests.
