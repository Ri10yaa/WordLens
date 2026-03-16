# AI Dictionary Agent

Monorepo housing three coordinated apps:

- `apps/backend` – FastAPI service that ranks dictionary senses with SentenceTransformer + CrossEncoder and caches results in Redis.
- `apps/extension` – Manifest V3 Chrome overlay that lets users request contextual definitions on any webpage.
- `apps/agent` – OpenAI function-calling client that routes natural-language prompts through the backend tool endpoint.

Shared contracts live in `packages/shared`, while architecture notes and runbooks live under `docs/`.

## Quick Start

| Task | Command |
| --- | --- |
| Install backend deps | `cd apps/backend && pip install -r requirements.txt` |
| Run backend locally | `scripts/run-backend.sh` |
| Build extension | `scripts/build-extension.sh` |
| Run agent CLI | `scripts/run-agent.sh "Explain bank in finance"` |

See the per-app READMEs for detailed setup, Docker instructions, and tests.
