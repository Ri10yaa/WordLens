# Shared Models

Source of truth for the `ContextualMeaningResponse` contract that both the backend and clients consume.

- `schema/contextual_meaning.json` – JSON Schema describing the payload.
- `ts/context.ts` – TypeScript type definition imported by frontend builds.
- `python/context.py` – Pydantic model that can be reused by Python consumers.

Sync workflow:

1. Update the JSON schema.
2. Regenerate TS/Python helpers (manual for now).
3. Bump dependent packages if distributing independently.
