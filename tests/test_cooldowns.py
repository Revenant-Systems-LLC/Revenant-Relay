import json
from datetime import date

from src import cooldowns


def test_load_clean_cooldowns_removes_expired_entries(tmp_path, monkeypatch):
    file = tmp_path / "cooldowns.json"
    file.write_text(json.dumps({"platform_cooldowns": {"x": {"A1": "2020-01-01", "A2": "2099-01-01"}, "reddit": {"r/test": {"B1": "2020-01-01", "B2": "2099-01-01"}}}}), encoding="utf-8")
    monkeypatch.setattr(cooldowns, "COOLDOWNS_FILE", file)
    cleaned = cooldowns.load_clean_cooldowns(today=date(2026, 1, 1))
    assert cleaned == {"x": {"A2": "2099-01-01"}, "reddit": {"r/test": {"B2": "2099-01-01"}}}


def test_add_cooldown_writes_flat_platform(tmp_path, monkeypatch):
    file = tmp_path / "cooldowns.json"
    file.write_text('{"platform_cooldowns": {}}', encoding="utf-8")
    monkeypatch.setattr(cooldowns, "COOLDOWNS_FILE", file)
    cooldowns.add_cooldown("x", "A1", days=3, today=date(2026, 1, 1))
    data = json.loads(file.read_text(encoding="utf-8"))
    assert data["platform_cooldowns"]["x"]["A1"] == "2026-01-04"


def test_add_reddit_cooldown_writes_nested_reddit(tmp_path, monkeypatch):
    file = tmp_path / "cooldowns.json"
    file.write_text('{"platform_cooldowns": {}}', encoding="utf-8")
    monkeypatch.setattr(cooldowns, "COOLDOWNS_FILE", file)
    cooldowns.add_reddit_cooldown("r/test", "A1", days=2, today=date(2026, 1, 1))
    data = json.loads(file.read_text(encoding="utf-8"))
    assert data["platform_cooldowns"]["reddit"]["r/test"]["A1"] == "2026-01-03"


def test_ads_in_cooldown_and_reddit_ads_in_cooldown():
    buckets = {"x": {"A1": "2099-01-01"}, "reddit": {"r/test": {"A2": "2099-01-01"}}}
    assert cooldowns.ads_in_cooldown(buckets, "x") == {"A1"}
    assert cooldowns.reddit_ads_in_cooldown(buckets, "r/test") == {"A2"}
