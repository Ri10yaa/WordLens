from unittest import mock

from agent import tools


def test_fetch_literal_senses_handles_request_errors(monkeypatch):
    def _raise(*_args, **_kwargs):
        raise tools.requests.exceptions.ConnectionError("boom")

    monkeypatch.setattr(tools.requests, "post", _raise)

    result = tools.fetch_literal_senses("bank")
    assert "error" in result
