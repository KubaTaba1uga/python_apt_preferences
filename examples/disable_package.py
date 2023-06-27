# Example usage:
#    python disable_packages.py ncurses ncurses-bin ncurses-term

# Example description:
#  Create preference file which disables upgrade for specified packages.
#  If any package has corresponding preference already, delete the entry.

import sys

from apt_preferences.parse_preferences_files import (
    parse_preferences_files as _parse_preferences_files,
)
from apt_preferences.render_preferences_files import render_preferences_files
from apt_preferences.data_structures import AptPreference


def parse_preferences_files():
    try:
        return _parse_preferences_files()
    except FileNotFoundError:
        return []


def get_packages_from_cli():
    return sys.argv[1:]


def delete_related_preferences(packages, preferences):
    i = 0
    for _ in preferences:
        preference = preferences[i]

        if preference.package in packages:
            preferences.pop(i)
        else:
            i += 1


def main():
    packages, preferences = get_packages_from_cli(), parse_preferences_files()

    delete_related_preferences(packages, preferences)

    for package in packages:
        not_upgradable_package = AptPreference(
            package, pin='origin "*"', pin_priority=1
        )

        preferences.append(not_upgradable_package)

    new_preferences_map = render_preferences_files(preferences, False)

    file_content = new_preferences_map[AptPreference.FILE_PATH_NONE_FIELD_NAME]

    print(file_content)


if __name__ == "__main__":
    main()
