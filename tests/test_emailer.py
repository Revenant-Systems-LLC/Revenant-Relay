from src.emailer import _is_valid_email


def test_is_valid_email_accepts_standard_address():
    assert _is_valid_email("user@example.com")


def test_is_valid_email_rejects_invalid_values():
    assert not _is_valid_email("")
    assert not _is_valid_email("invalid")
    assert not _is_valid_email("user@localhost")
