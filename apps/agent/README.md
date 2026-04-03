# LLM Agent

Wraps the backend API with a lightweight Hugging Face Inference model (default: `google/flan-t5-base`) so you can fetch literal senses from `/tools/list_senses` and let the model pick the contextual meaning. Provide an optional `HF_API_TOKEN` if you need higher rate limits on inference; otherwise the public endpoint works for light usage.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp apps/agent/.env.example apps/agent/.env
```

Fill in `BACKEND_URL` (defaults to localhost), `HF_MODEL_NAME`, and optionally `HF_API_TOKEN` if using a private Hugging Face token.

## Usage

```bash
python -m agent.cli bank "I deposited money in the bank"
```

## Tests

```bash
pytest
```
