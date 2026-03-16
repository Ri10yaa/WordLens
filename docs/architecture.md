# Architecture

```
Chrome Extension  ──►  FastAPI Backend  ──►  Free Dictionary API
        │                    │                     │
        │                    ├──► Redis Cache ◄────┘
        │
        └──► OpenAI Agent (function call) ─────────────────┘
```

- The Chrome extension injects a floating dialog on every page and sends `/define` and `/tools/define_contextual` requests to the backend.
- The backend fetches baseline data from `dictionaryapi.dev`, normalizes entries, embeds definitions, and ranks senses using SentenceTransformer + CrossEncoder with heuristic boosts.
- Definitions are cached in Redis for a day; subsequent contextual lookups reuse the cached structure.
- The OpenAI agent exposes the same contextual tool via function calling so textual prompts get routed to the backend.
