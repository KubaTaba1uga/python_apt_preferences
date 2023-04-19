"""

   Find paths to all preference files.

"""
import string
import typing
from pathlib import Path


_APT_PREF_FILE_PATH_S: str = "/etc/apt/preferences"

_APT_PREF_DIR_PATH_S: str = _APT_PREF_FILE_PATH_S + ".d"


def find_pref_files() -> typing.List[Path]:
    """ Find paths to files used by APT to set up preferences. """

    pref_files_paths: typing.List[Path] = [_get_default_pref_file_path()]

    for file_name in _get_default_pref_dir_path().rglob("*"):
        file_path = Path(file_name)

        if is_pref_file(file_path) is True:
            pref_files_paths.append(file_path)

    return pref_files_paths


def _get_default_pref_file_path() -> Path:
    """ The APT preferences file '/etc/apt/preferences'. """
    return Path(_APT_PREF_FILE_PATH_S)


def _get_default_pref_dir_path() -> Path:
    """ The APT preferences fragment files in the '/etc/apt/preferences.d/'."""
    return Path(_APT_PREF_DIR_PATH_S)


def is_pref_file(path: Path) -> bool:
    """According docs:
    `The files have either no or "pref" as filename extension and only
    contain alphanumeric, hyphen (-), underscore (_) and period (.) characters.`
    """
    allowed_extensions, allowed_characters = ["", ".pref"], [
        *string.ascii_letters,
        *string.digits,
        "-",
        "_",
        ".",
    ]

    file_extension, file_content = path.suffix, path.read_text()

    if file_extension not in allowed_extensions:
        return False

    for character in file_content:
        if character not in allowed_characters:
            return False

    return True
