import copy
import typing
import functools
from pathlib import Path

from lark import Lark
from lark import Transformer
from lark import v_args

from app.data_structures import AptPreference
from app._utils import read_file
from app._utils import copy_obj
from app._utils import get_function_name
from app._utils import get_function_parameters_names
from app.errors import NoPreferencesFound
from app.find_pref_files import find_pref_files
from app._constants import LARK_GRAMMAR
from app._constants import EXPLANATIONS_FIELD_NAME


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
        preference.file_path: Path = copy_obj(file_path)


def _add_explanations_to_rule(func):
    @functools.wraps(func)
    def wrapped_func(_, rule_l) -> dict:
        explanations_exist, rule_is_valid = _explanations_exist(rule_l), _rule_is_valid(
            rule_l
        )

        if rule_is_valid is False:
            raise ValueError(rule_l)

        rule_value = rule_l.pop()

        func_result: dict = func(_, rule_value)

        if explanations_exist is True:
            func_result[EXPLANATIONS_FIELD_NAME] = rule_l.pop()

        return func_result

    return wrapped_func


def _explanations_exist(rule_l) -> bool:
    return len(rule_l) == 2


def _rule_is_valid(rule_l) -> bool:
    return len(rule_l) == 1 or _explanations_exist(rule_l)


class PreferencesTreeTransformer(Transformer):
    string = v_args(inline=True)(str)
    integer = v_args(inline=True)(int)
    explanation = v_args(inline=True)(str)

    preferences_l = list
    explanations_l = list

    @_add_explanations_to_rule
    def pin(self, s) -> typing.Dict[str, str]:
        return {get_function_name(): s}

    @_add_explanations_to_rule
    def package(self, s) -> typing.Dict[str, str]:
        return {get_function_name(): s}

    @_add_explanations_to_rule
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

        kwargs = {EXPLANATIONS_FIELD_NAME: {}}

        _add_explenations_to_kwargs(l, kwargs)

        kwargs_are_valid = _kwargs_are_valid(kwargs)

        if kwargs_are_valid is False:
            raise ValueError(kwargs)

        return AptPreference(**kwargs)


def _add_explenations_to_kwargs(l, kwargs):
    for value_d in l:
        field_name = _find_field_name(value_d)

        kwargs[field_name] = value_d[field_name]

        if value_d.get(EXPLANATIONS_FIELD_NAME) is not None:
            kwargs[EXPLANATIONS_FIELD_NAME][field_name] = value_d[
                EXPLANATIONS_FIELD_NAME
            ]


def _find_field_name(value_d):
    for field in value_d.keys():
        if field != EXPLANATIONS_FIELD_NAME:
            return field
    raise NotImplementedError(value_d)


def _kwargs_are_valid(kwargs) -> bool:
    not_mapped_fields_names = set(["self", "file_path"])

    mapped_fields_names: set = get_function_parameters_names(
        AptPreference.__init__
    ).difference(not_mapped_fields_names)

    return set(kwargs.keys()) == set(mapped_fields_names)


def _create_lark_parser():
    return Lark(
        LARK_GRAMMAR,
        parser="lalr",
        lexer="contextual",  # <- contextual lexer is required to resolve priorities
        propagate_positions=False,  # <- improve speed
        maybe_placeholders=False,  # <- improve speed
        transformer=PreferencesTreeTransformer(),  # <- improve speed
    )


_parser = _create_lark_parser()
