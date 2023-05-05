from pathlib import Path

import pytest

_PARENT_DIR_PATH = Path(__file__).parent


@pytest.fixture
def good_pref_file_path():
    return Path("/etc/apt/preferences.d/my-custom-repository")


@pytest.fixture
def e2e_multiple_entries():
    return _PARENT_DIR_PATH.joinpath(Path("test_files/my-custom-repository"))


@pytest.fixture
def e2e_single_entry():
    return _PARENT_DIR_PATH.joinpath(Path("test_files/my-custom-repo-single"))
