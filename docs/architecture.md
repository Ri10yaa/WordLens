# Architecture

```
Chrome Extension  ──►  FastAPI Backend  ──►  Merriam-Webster API
        │                    │                     │
        │                    ├──► Redis Cache ◄────┘
        │
        └──► OpenAI Agent (function call) ─────────────────┘
```

- The Chrome extension injects a floating dialog on every page and sends `/define` and `/tools/define_contextual` requests to the backend.
- The backend fetches baseline data from the Merriam-Webster Collegiate Dictionary API, normalizes entries, embeds definitions, and ranks senses using SentenceTransformer + CrossEncoder with heuristic boosts.
- Definitions are cached in Redis for a day; subsequent contextual lookups reuse the cached structure.
- The OpenAI agent first calls `/tools/list_senses` to fetch all literal meanings, then reasons over that list to deliver the contextual sense back to the user via function calling.
