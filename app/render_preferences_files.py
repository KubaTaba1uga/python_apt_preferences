import typing
import functools

from app.data_structures import AptPreference
from app._constants import DELIMETER
from app._constants import EXPLANATIONS_FIELD_NAME
from app._constants import FIELDS_TO_RENDER
from app._constants import FIELD_TO_SNIPPET_MAP


def render_preferences_files(
    preferences_l: typing.List[AptPreference], save_files: bool = True
) -> typing.Dict[str, str]:
    """Creates files paths -> files contents map. If save files set to True,
    files contents will be automaticly save to a file system."""
    paths_excluded_from_save = [AptPreference.FILE_PATH_NONE_FIELD_NAME]

    results: typing.Dict[str, str] = {}

    file_to_snippet_map: typing.Dict[str, typing.List[str]] = _init_file_to_snippet_map(
        preferences_l
    )

    for abs_file_path_s in file_to_snippet_map:
        results[abs_file_path_s] = file_content = DELIMETER.join(
            file_to_snippet_map[abs_file_path_s]
        )

        if save_files is True and abs_file_path_s not in paths_excluded_from_save:
            with open(abs_file_path_s, "w") as pref_fp:
                pref_fp.write(file_content)

    return results


def _init_file_to_snippet_map(
    preferences_l: typing.List[AptPreference],
) -> typing.Dict[str, typing.List[str]]:
    file_to_snippet_map: typing.Dict[str, typing.List[str]] = {}

    for preference in preferences_l:

        rendered_preference: str = render_preference(preference)

        file_path_s: str = (
            str(preference.file_path.absolute())
            if preference.file_path is not None
            else AptPreference.FILE_PATH_NONE_FIELD_NAME
        )

        if file_to_snippet_map.get(file_path_s) is None:
            file_to_snippet_map[file_path_s] = []

        file_to_snippet_map[file_path_s].append(rendered_preference)

    return file_to_snippet_map


def render_preference(preference: AptPreference) -> str:

    results_l: typing.List[str] = []

    for field_name in FIELDS_TO_RENDER:
        rendered_s: str = _render_field_with_explanation(preference, field_name)

        results_l.append(rendered_s)

    return DELIMETER.join(results_l)


def _render_field_with_explanation(preference: AptPreference, field_name: str) -> str:
    field_s = _format_snippet(field_name, getattr(preference, field_name))

    results_sorted_l: list = [field_s]

    if len(preference.explanations) > 0:
        field_explanations_s = _render_explanations_l(
            preference.explanations, field_name
        )
        results_sorted_l = [field_explanations_s, field_s]

    return DELIMETER.join(results_sorted_l)


def _format_snippet(field_name, value) -> str:
    return FIELD_TO_SNIPPET_MAP[field_name].format(value=value)


def _render_explanations_l(
    all_explanations_d: typing.Dict[str, typing.List[str]],
    field_name: str,
) -> str:
    explanations_l: typing.List[str] = all_explanations_d[field_name]

    explanations_snippets = (
        _format_explanation(explanation) for explanation in explanations_l
    )

    return DELIMETER.join(explanations_snippets)


def _format_explanation(explanation_value: str) -> str:
    return _format_snippet(field_name=EXPLANATIONS_FIELD_NAME, value=explanation_value)
