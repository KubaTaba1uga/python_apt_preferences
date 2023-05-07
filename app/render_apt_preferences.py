import typing
import functools

from app.data_structures import AptPreference
from app._constants import DELIMETER
from app._constants import FIELDS_TO_RENDER
from app._constants import FIELD_TO_SNIPPET_MAP


def render_preferences_l(
    preferences_l: typing.List[AptPreference],
) -> typing.Dict[str, str]:
    results: typing.Dict[str, str] = {}

    file_to_snippet_map: typing.Dict[str, typing.List[str]] = _init_file_to_snippet_map(
        preferences_l
    )

    for abs_file_path_s in file_to_snippet_map:
        with open(abs_file_path_s, "w") as pref_fp:
            results[abs_file_path_s] = file_content = DELIMETER.join(
                file_to_snippet_map[abs_file_path_s]
            )
            pref_fp.write(file_content)

    return results


def _init_file_to_snippet_map(
    preferences_l: typing.List[AptPreference],
) -> typing.Dict[str, typing.List[str]]:
    file_to_snippet_map: typing.Dict[str, typing.List[str]] = {}

    for preference in preferences_l:
        if preference.file_path is None:
            continue

        abs_file_path = str(preference.file_path.absolute())
        if file_to_snippet_map.get(abs_file_path) is None:
            file_to_snippet_map[abs_file_path] = []

        rendered_preference: str = render_preference(preference)

        file_to_snippet_map[abs_file_path].append(rendered_preference)

    return file_to_snippet_map


def render_preference(preference: AptPreference) -> str:

    results_l: typing.List[str] = []

    for field_name in FIELDS_TO_RENDER:
        rendered_s: str = _render_field_with_explanation(preference, field_name)

        results_l.append(rendered_s)

    return DELIMETER.join(results_l)


def _render_field_with_explanation(preference: AptPreference, field_name: str) -> str:
    field_s, field_explanations = (
        _format_snippet(field_name, getattr(preference, field_name)),
        _render_explanations_l(preference.explanations, field_name),
    )

    results_sorted_l: list = [field_s]

    if field_explanations is not None:
        results_sorted_l = [field_explanations, field_s]

    return DELIMETER.join(results_sorted_l)


def _format_snippet(field_name, value) -> str:
    return FIELD_TO_SNIPPET_MAP[field_name].format(value=value)


def _render_explanations_l(
    all_explanations_d: dict, field_name: str
) -> typing.Optional[str]:
    explanations_l: typing.Optional[typing.List[str]] = all_explanations_d.get(
        field_name
    )

    explanations_are_valid: bool = (explanations_l is not None) and (
        len(explanations_l) > 0
    )

    if explanations_are_valid is False:
        return None

    explanations_snippets = (
        _format_explanation(explanation) for explanation in explanations_l
    )

    return DELIMETER.join(explanations_snippets)


def _format_explanation(explanation_value: str) -> str:
    return _format_snippet(field_name="explanation", value=explanation_value)
