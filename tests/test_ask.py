from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=8),
        text="回答です",
    )

    class FakeClient:
        models = SimpleNamespace(generate_content=lambda **kwargs: response)

    monkeypatch.setattr(ask.genai, "Client", lambda **kwargs: FakeClient())
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問です") == "回答です"
    assert capsys.readouterr().out == "[tokens] input=12 output=8\n"