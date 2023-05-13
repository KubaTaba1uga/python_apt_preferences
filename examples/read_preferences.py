import typing
import pathlib

from apt_preferences.data_structures import AptPreference
from apt_preferences.errors import NoPreferencesFound
from apt_preferences.parse_preferences_files import parse_preference
from apt_preferences.parse_preferences_files import parse_preferences_path

from constants import EXAMPLE_FILE_PATH


def read_from_str(s_to_read: str) -> typing.List[AptPreference]:
    try:
        return parse_preference(s_to_read)
    except NoPreferencesFound:
        return []


def read_from_file(file_path: pathlib.Path) -> typing.List[AptPreference]:
    try:
        return parse_preferences_path(file_path)
    except NoPreferencesFound:
        return []


if __name__ == "__main__":
    (preferences_content, preferences_path,) = (
        """
Package: *
Pin: release n=jammy
Pin-Priority: 700

Package: *
Pin: release n=lunar
Pin-Priority: -10
""",
        EXAMPLE_FILE_PATH,
    )

    print("Preferences read from string:")
    for preference in read_from_str(preferences_content):
        print(preference)

    print()

    print("Preferences read from file: {}")
    for preference in read_from_file(preferences_path):
        print(preference)
