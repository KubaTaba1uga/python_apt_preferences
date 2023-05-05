import copy
import typing
import functools
from pathlib import Path

from lark import Lark
from lark import Transformer
from lark import v_args

from app.data_structures import AptPreference
from app.utils import read_file
from app.utils import copy_obj
from app.utils import get_function_name
from app.errors import NoPreferencesFound
from app.find_pref_files import find_pref_files

_EXPLANATIONS_FIELD_ID = "explanations"

_PARENT_DIR_PATH = Path(__file__).parent

LARK_GRAMMAR_PATH = _PARENT_DIR_PATH.joinpath("apt_preferences.lark")

LARK_GRAMMAR = read_file(LARK_GRAMMAR_PATH)


def parse_apt_preferences() -> typing.List[typing.Union[AptPreference, str]]:
    """Find preference files.
    Transform each preference file into AptPreferences' list.
    Merge lists (info about source file is in AptPreference).
    """
    parsed_preferences_l: typing.List[AptPreference] = []

    for file_path in find_pref_files():
        try:
            parsed_file_l = parse_apt_preferences_file(file_path)
        except NoPreferencesFound:
            continue

        parsed_preferences_l.extend(parsed_file_l)

    return parsed_preferences_l


def parse_apt_preferences_file(
    pref_file_path: Path,
) -> typing.List[typing.Union[AptPreference, str]]:
    """ Transforms preference file into AptPreferences' list. """

    pref_file_content: str = read_file(pref_file_path)

    try:
        preferences_l = _parser.parse(pref_file_content)
    except NoPreferencesFound as err:
        raise NoPreferencesFound(pref_file_path) from err

    _populate_preferences_paths(preferences_l, pref_file_path)

    return preferences_l


def _populate_preferences_paths(preferences_l, file_path):
    for preference in preferences_l:
        if isinstance(preference, AptPreference) is True:
            preference.file_path: Path = copy_obj(file_path)


def _create_lark_parser():
    return Lark(
        LARK_GRAMMAR,
        parser="lalr",
        lexer="contextual",  # <- contextual lexer is required to resolve priorities
        propagate_positions=False,  # <- improve speed
        maybe_placeholders=False,  # <- improve speed
        transformer=PreferencesTreeTransformer(),  # <- improve speed
    )


def add_explanations_to_field(func):
    @functools.wraps(func)
    def wrapped_func(_, rule_l) -> dict:
        explanations_exist, rule_is_valid = len(rule_l) == 2, len(rule_l) in (1, 2)

        if rule_is_valid is False:
            raise ValueError(rule_l)

        rule_value = rule_l.pop()

        func_result: dict = func(_, rule_value)

        if explanations_exist is True:
            func_result[_EXPLANATIONS_FIELD_ID] = rule_l.pop()

        return func_result

    return wrapped_func


def _add_explenations_to_kwargs(l, kwargs):
    for value_d in l:
        field_name = _find_field_name(value_d)

        kwargs[field_name] = value_d[field_name]

        if value_d.get(_EXPLANATIONS_FIELD_ID) is not None:
            kwargs[_EXPLANATIONS_FIELD_ID][field_name] = value_d[_EXPLANATIONS_FIELD_ID]


def _find_field_name(value_d):
    for field in value_d.keys():
        if field != _EXPLANATIONS_FIELD_ID:
            return field
    raise NotImplementedError(value_d)


class PreferencesTreeTransformer(Transformer):
    string = v_args(inline=True)(str)
    integer = v_args(inline=True)(int)
    explanation = v_args(inline=True)(str)

    preferences_l = list
    explanations_l = list

    @add_explanations_to_field
    def pin(self, s) -> typing.Dict[str, str]:
        return {get_function_name(): s}

    @add_explanations_to_field
    def package(self, s) -> typing.Dict[str, str]:
        return {get_function_name(): s}

    @add_explanations_to_field
    def pin_priority(self, i) -> typing.Dict[str, int]:
        return {get_function_name(): i}

    # While order is unimportant for apt, Transformer
    #   creates python list for each rule (for which
    #   order is important). To distinguish values
    #   from each other, methods names are mapped to
    #   AptPreferences.__init__ kwargs.

    def preference(self, l) -> AptPreference:
        if len(l) == 0:
            raise NoPreferencesFound()

        kwargs = {_EXPLANATIONS_FIELD_ID: {}}

        _add_explenations_to_kwargs(l, kwargs)

        # one for each field in AptPreference
        kwargs_are_valid = len(kwargs.keys()) == 4

        if kwargs_are_valid is False:
            raise ValueError(kwargs)

        return AptPreference(**kwargs)


_parser = _create_lark_parser()
