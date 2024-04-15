from pathvalidate import sanitize_filename


def test_sanitize_filename():
    assert sanitize_filename("file.md") == "file.md"
    assert sanitize_filename("file") == "file"
    assert sanitize_filename("Україна.md") == "Україна.md"
    assert sanitize_filename('Україна?123*"\/<>:|?".md') == "Україна123.md"
