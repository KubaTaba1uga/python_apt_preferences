from pathlib import Path

import pytest


def good_pref_file_path():
    return Path("/etc/apt/preferences.d/my-custom-repository")


def good_pref_file_content():
    pass
