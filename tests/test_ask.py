from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    class Models:
        def generate_content(self, **kwargs):
            return SimpleNamespace(
                text="answer",
                usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=5),
            )

    class Client:
        def __init__(self, api_key):
            self.models = Models()

    monkeypatch.setattr(ask.genai, "Client", Client)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("question") == "answer"
    assert capsys.readouterr().out.strip() == "[usage] input_tokens=12 output_tokens=5"