import json
from pathlib import Path
import pytest

from src import scout_logger


def test_load_leads_file_not_found(tmp_path, monkeypatch):
    non_existent = tmp_path / "warm_leads.json"
    monkeypatch.setattr(scout_logger, "WARM_LEADS_FILE", non_existent)
    
    assert scout_logger._load_leads() == []


def test_load_leads_corrupt_json(tmp_path, monkeypatch):
    corrupt = tmp_path / "warm_leads.json"
    corrupt.write_text("invalid json content{", encoding="utf-8")
    monkeypatch.setattr(scout_logger, "WARM_LEADS_FILE", corrupt)
    
    assert scout_logger._load_leads() == []


def test_log_leads_success_and_deduplication(tmp_path, monkeypatch):
    leads_file = tmp_path / "warm_leads.json"
    leads_file.write_text('{"leads": []}', encoding="utf-8")
    monkeypatch.setattr(scout_logger, "WARM_LEADS_FILE", leads_file)

    leads_to_log = [
        {
            "platform": "reddit",
            "keyword": "VS Code theme",
            "author": "dev1",
            "post_content": "Looking for clean themes.",
            "post_url": "https://reddit.com/r/gamedev/123"
        },
        {
            "platform": "x",
            "keyword": "custom bot",
            "author": "dev2",
            "post_content": "Who makes custom bots?",
            "post_url": "https://x.com/status/456"
        }
    ]

    # First log should add both leads
    added = scout_logger.log_leads(leads_to_log)
    assert added == 2

    # Load and check saved data
    saved = scout_logger._load_leads()
    assert len(saved) == 2
    assert saved[0]["author"] == "dev1"
    assert saved[1]["author"] == "dev2"
    assert "discovered_at" in saved[0]

    # Second log with identical URLs should add 0 new leads
    added_again = scout_logger.log_leads(leads_to_log)
    assert added_again == 0
    assert len(scout_logger._load_leads()) == 2

    # Log a mix of old and one new lead
    mix_leads = [
        leads_to_log[0],  # Duplicate URL
        {
            "platform": "linkedin",
            "keyword": "MCP server",
            "author": "dev3",
            "post_content": "Help setting up MCP.",
            "post_url": "https://linkedin.com/posts/789"
        }
    ]
    added_mix = scout_logger.log_leads(mix_leads)
    assert added_mix == 1
    assert len(scout_logger._load_leads()) == 3
