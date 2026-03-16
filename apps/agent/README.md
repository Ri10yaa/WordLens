# LLM Agent

Wraps the backend API with OpenAI function calling so you can query contextual definitions via CLI or integrate with other tools.

## Setup

```bash
cd apps/agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `OPENAI_API_KEY` and optionally override `BACKEND_URL`.

## Usage

```bash
python -m agent.cli "Explain the meaning of bank when I deposited money"
```

## Tests

```bash
pytest
```
