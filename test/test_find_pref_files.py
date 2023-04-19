from pathlib import Path
from unittest import mock

from app.find_pref_files import is_pref_file


def test_is_pref_file_pref_extension(tmpdir):
    wrong_extension, correct_extension, no_extension = (
        Path(tmpdir.join("hello.txt")),
        Path(tmpdir.join("hello.pref")),
        Path(tmpdir.join("hello")),
    )

    with mock.patch.object(Path, "read_text") as read_text_mock:
        read_text_mock.return_value = ""

        assert is_pref_file(wrong_extension) is False
        assert is_pref_file(correct_extension) is True
        assert is_pref_file(no_extension) is True


def test_is_pref_file_allowed_characters(tmpdir):
    wrong_characters, correct_characters, no_characters = (
        tmpdir.join("invalid_characters.pref"),
        tmpdir.join("correct_characters.pref"),
        tmpdir.join("no_characters.pref"),
    )

    wrong_characters.write_text("!@#$%^&*()", encoding="utf-8")
    correct_characters.write_text("iuahsduhaduhad", encoding="utf-8")
    no_characters.write_text("", encoding="utf-8")

    wrong_characters, correct_characters, no_characters = (
        Path(wrong_characters),
        Path(correct_characters),
        Path(no_characters),
    )

    assert is_pref_file(wrong_characters) is False
    assert is_pref_file(correct_characters) is True
    assert is_pref_file(no_characters) is True
