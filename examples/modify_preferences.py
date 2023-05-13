import copy
import typing
import pathlib

from apt_preferences.data_structures import AptPreference
from apt_preferences.parse_preferences_files import parse_preferences_path
from apt_preferences.render_preferences_files import render_preferences_files

from constants import EXAMPLE_FILE_PATH


def move_to_file(preference: AptPreference, file_path: pathlib.Path):
    preference.file_path = file_path


def copy_preferences(
    preferences_l: typing.List[AptPreference], new_file_path: pathlib.Path
) -> typing.List[AptPreference]:

    preferences_l_cp = copy.deepcopy(preferences_l)

    for preference in preferences_l_cp:
        move_to_file(preference, new_file_path)

    return preferences_l_cp


if __name__ == "__main__":
    old_preference_path, new_preference_path = (
        EXAMPLE_FILE_PATH,
        pathlib.Path(__file__).parent.joinpath("new_apt_preference_file.pref"),
    )

    old_preferences_l = parse_preferences_path(old_preference_path)

    new_preferences_l = copy_preferences(old_preferences_l, new_preference_path)

    for preference in new_preferences_l:
        preference.explanations["pin"] = ["bla bla bla"]

    render_preferences_files(new_preferences_l, save_files=True)
