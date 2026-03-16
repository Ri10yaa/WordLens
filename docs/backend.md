# Backend Notes

- Environment variables defined in `apps/backend/.env.example` (Redis host/port, dictionary URL, optional CORS origins).
- Models required: install via `python -m spacy download en_core_web_sm`.
- Endpoints:
  - `GET /health` – status probe
  - `GET /define/{word}` – raw normalized dictionary entries
  - `POST /tools/define_contextual` – best matching definition with probability
- Cache TTL defaults to 24h; adjust via `CACHE_TTL` env var if necessary.
