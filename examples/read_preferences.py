import typing

from apt_preferences.parse_preferences_files import parse_preference
from apt_preferences.errors import NoPreferencesFound
from apt_preferences.data_structures import AptPreference


def read_from_str(s_to_read: str):
    try:
        return parse_preference(s_to_read)
    except NoPreferencesFound:
        return []


if __name__ == "__main__":
    preferences_str = """
Package: *
Pin: release n=jammy
Pin-Priority: 700

Package: *
Pin: release n=lunar
Pin-Priority: -10
"""
    preferences_str_l: typing.List[AptPreference] = parse_preference(preferences_str)

    print("Preferences read from string:")
    for preference in preferences_str_l:
        print(preference)
    print()
