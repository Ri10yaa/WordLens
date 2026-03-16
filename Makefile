.PHONY: backend extension agent tests

backend:
	@(cd apps/backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload)

extension:
	@(cd apps/extension && npm install && npm run build)

agent:
	@(cd apps/agent && python -m agent.cli "Explain the meaning of bank")

tests:
	@(cd apps/backend && pytest)
	@(cd apps/agent && pytest)
