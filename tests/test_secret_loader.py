from pathlib import Path

from src import secret_loader


def test_secrets_file_prefers_dpapi_default(monkeypatch, tmp_path):
    monkeypatch.delenv("RR_SECRETS_FILE", raising=False)
    dpapi = tmp_path / "revenant-relay.dpapi"
    env = tmp_path / "revenant-relay.env"
    dpapi.write_text("{}", encoding="utf-8")
    env.write_text("RR_TEST=1\n", encoding="utf-8")
    monkeypatch.setattr(secret_loader, "_DEFAULT_DPAPI_FILE", dpapi)
    monkeypatch.setattr(secret_loader, "_DEFAULT_PLAINTEXT_FILE", env)
    assert secret_loader._secrets_file_path() == dpapi


def test_secrets_file_falls_back_to_env(monkeypatch, tmp_path):
    monkeypatch.delenv("RR_SECRETS_FILE", raising=False)
    env = tmp_path / "revenant-relay.env"
    env.write_text("RR_TEST=1\n", encoding="utf-8")
    dpapi = tmp_path / "revenant-relay.dpapi"
    monkeypatch.setattr(secret_loader, "_DEFAULT_DPAPI_FILE", dpapi)
    monkeypatch.setattr(secret_loader, "_DEFAULT_PLAINTEXT_FILE", env)
    assert secret_loader._secrets_file_path() == env


def test_secrets_file_respects_env(monkeypatch):
    monkeypatch.setenv("RR_SECRETS_FILE", "~/custom.dpapi")
    assert secret_loader._secrets_file_path().name == "custom.dpapi"
