from __future__ import annotations

from functools import reduce
from typing import Any, Iterable


def extract_keys(d: dict[str, Any], keys: Iterable[str]) -> dict[str, Any]:
    """
    Extract keys from a dictionary, specialized for the `str` key case.

    >>> extract_keys({'a': 'b', 'c': 'd'}, ['a'])
    {'a': 'b'}

    >>> extract_keys({'a': 'b', 'c': 'd'}, [])
    {}

    >>> extract_keys({'a': 'b', 'c': 'd'}, ['e'])
    Traceback (most recent call last):
        ...
    KeyError: 'e'
    """

    return {k: d[k] for k in keys}


def transform_str(
    string: str,
    transforms: Iterable[tuple[str, str]],
) -> str:
    """
    Replace substrings of `string` defined in the first position of `transforms` tuple
    with the second one.

    Note that the transformation is order-dependent and case-sensitive!

    >>> transform_str('abcd', [])
    'abcd'

    >>> transform_str('abcd', [('A', 'not-matched')])
    'abcd'

    >>> transform_str('godot', [('dot', '.'), ('god', 'Eminem')])
    'go.'

    >>> transform_str('godot', [('god', 'Eminem'), ('dot', '.')])
    'Eminemot'
    """
    return reduce(lambda s, kv: s.replace(kv[0], kv[1]), transforms, string)
