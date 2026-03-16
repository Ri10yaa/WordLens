# Backend Service

FastAPI application that powers the AI Dictionary Agent. It exposes `/health`, `/define/{word}`, and `/tools/define_contextual` endpoints, wraps the Free Dictionary API, ranks senses with SentenceTransformer + CrossEncoder models, and caches responses in Redis.

## Getting Started

1. **Install dependencies**

   ```bash
   cd apps/backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. **Configure environment**

   ```bash
   cp .env.example .env
   # adjust Redis host/port if needed
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
