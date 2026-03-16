from unittest import mock

from agent import tools


def test_define_contextual_handles_request_errors(monkeypatch):
    def _raise(*_args, **_kwargs):
        raise tools.requests.exceptions.ConnectionError("boom")

    monkeypatch.setattr(tools.requests, "post", _raise)

    result = tools.define_contextual("bank", "I deposited cash")
    assert "error" in result
