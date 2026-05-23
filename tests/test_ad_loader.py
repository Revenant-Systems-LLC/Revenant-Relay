import json

from src import ad_loader


def test_load_all_ads_finds_ad_json_files(tmp_path, monkeypatch):
    ad1 = tmp_path / "a1" / "ad.json"
    ad1.parent.mkdir(parents=True)
    ad1.write_text(json.dumps({"id": "A1", "approved": True}), encoding="utf-8")
    ad2 = tmp_path / "a2" / "ad.json"
    ad2.parent.mkdir(parents=True)
    ad2.write_text(json.dumps({"id": "A2", "approved": False}), encoding="utf-8")

    monkeypatch.setattr(ad_loader, "ADS_DIR", tmp_path)
    ads = ad_loader.load_all_ads()
    assert {a["id"] for a in ads} == {"A1", "A2"}


def test_load_approved_ads_only_true(tmp_path, monkeypatch):
    for ad_id, approved in (("A1", True), ("A2", False), ("A3", True)):
        p = tmp_path / ad_id / "ad.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps({"id": ad_id, "approved": approved}), encoding="utf-8")
    monkeypatch.setattr(ad_loader, "ADS_DIR", tmp_path)
    assert {a["id"] for a in ad_loader.load_approved_ads()} == {"A1", "A3"}


def test_ads_for_platform_filters_allowed_platforms():
    ads = [
        {"id": "A1", "allowed_platforms": ["x", "reddit"]},
        {"id": "A2", "allowed_platforms": ["linkedin"]},
    ]
    assert [a["id"] for a in ad_loader.ads_for_platform(ads, "reddit")] == ["A1"]


def test_caption_for_prefers_override_then_fallback():
    ad = {"caption": "base", "platform_captions": {"x": "override"}}
    assert ad_loader.caption_for(ad, "x") == "override"
    assert ad_loader.caption_for(ad, "reddit") == "base"
