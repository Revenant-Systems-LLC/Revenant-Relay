import json

from src import ad_selector, history, platform_selector


def test_new_run_has_required_fields():
    run = history.new_run("dev")
    for key in ("run_id", "date", "mode", "started_at", "attempts", "successes", "failures"):
        assert key in run


def test_append_run_last_run_and_yesterdays(tmp_path, monkeypatch):
    history_file = tmp_path / "runs.json"
    history_file.write_text('{"runs": []}', encoding="utf-8")
    monkeypatch.setattr(history, "RUN_HISTORY_FILE", history_file)

    r1 = history.new_run("dev")
    r1["date"] = "2026-05-21"
    r2 = history.new_run("dev")
    r2["date"] = "2026-05-23"
    history.append_run(r1)
    history.append_run(r2)
    assert history.last_run()["date"] == "2026-05-23"
    assert history.yesterdays_run()["date"] == "2026-05-21"


def test_platform_history_helpers(tmp_path, monkeypatch):
    history_file = tmp_path / "runs.json"
    history_file.write_text(json.dumps({"runs": [{"date": "2026-05-22", "attempts": [{"platform": "x", "success": True, "ad_id": "A1"}, {"platform": "reddit", "success": False, "ad_id": "A2"}]}]}), encoding="utf-8")
    monkeypatch.setattr(history, "RUN_HISTORY_FILE", history_file)
    succeeded, failed, attempted = history.platforms_used_yesterday()
    assert succeeded == {"x"}
    assert failed == {"reddit"}
    assert attempted == {"x", "reddit"}
    assert history.successful_ad_on_platform_yesterday("x") == "A1"


def test_build_tiers_and_select_next_platform(tmp_path, monkeypatch):
    pf = tmp_path / "platforms.json"
    dis = tmp_path / "disabled.json"
    pf.write_text(json.dumps({"platforms": {"x": {"enabled": True}, "reddit": {"enabled": True}, "linkedin": {"enabled": True}, "tiktok": {"enabled": False}}}), encoding="utf-8")
    dis.write_text(json.dumps({"disabled_platforms": ["linkedin"]}), encoding="utf-8")
    monkeypatch.setattr(platform_selector, "PLATFORMS_FILE", pf)
    monkeypatch.setattr(platform_selector, "DISABLED_FILE", dis)
    monkeypatch.setattr(platform_selector, "platforms_used_yesterday", lambda: ({"x"}, {"reddit"}, {"x", "reddit"}))
    tiers = platform_selector.build_tiers()
    assert tiers["tier1"] == []
    assert tiers["tier2"] == ["reddit"]
    assert tiers["tier3a"] == ["x"]
    p, label = platform_selector.select_next_platform(tiers, used_today={"reddit"}, unavailable_today=set())
    assert (p, label) == ("x", "tier3a")


def test_ad_selector_eligibility_and_tier3a(monkeypatch):
    monkeypatch.setattr(ad_selector, "load_approved_ads", lambda: [
        {"id": "A1", "allowed_platforms": ["x"]},
        {"id": "A2", "allowed_platforms": ["x"]},
    ])
    monkeypatch.setattr(ad_selector, "successful_ad_on_platform_yesterday", lambda platform: "A1")
    pick = ad_selector.select_ad_for_platform("x", "tier3a", {"x": {"A2": "2099-01-01"}})
    assert pick is None
    pick2 = ad_selector.select_ad_for_platform("x", "tier1", {"x": {"A2": "2099-01-01"}})
    assert pick2["id"] == "A1"
