# Backend Service

FastAPI application that powers the AI Dictionary Agent. It exposes `/health`, `/define/{word}`, and `/tools/define_contextual` endpoints, wraps the Merriam-Webster Collegiate Dictionary API, ranks senses with SentenceTransformer + CrossEncoder models, and caches responses in Redis.
The upstream data source is the [Merriam-Webster Collegiate Dictionary API](https://dictionaryapi.com/) configured via `DICTIONARY_API_URL` and `DICTIONARY_API_KEY`.

## Getting Started

1. **Install dependencies (from repo root)**

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Configure environment**

   ```bash
   cp .env.example .env
   # add your Merriam-Webster API key
   ```

3. **Run the API**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Docker Compose

Use the provided `docker-compose.yml` to start FastAPI and Redis together:

```bash
docker compose up --build
```

## Tests

```bash
pytest
```
