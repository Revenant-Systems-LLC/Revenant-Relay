from src import secret_loader


def test_secrets_file_default_path(monkeypatch):
    monkeypatch.delenv("RR_SECRETS_FILE", raising=False)
    assert str(secret_loader._secrets_file_path()) == "config/secrets.env"


def test_secrets_file_respects_env(monkeypatch):
    monkeypatch.setenv("RR_SECRETS_FILE", "~/custom-secrets.env")
    assert secret_loader._secrets_file_path().name == "custom-secrets.env"
