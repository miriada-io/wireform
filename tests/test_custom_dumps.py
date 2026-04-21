import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import ClassVar, Any

import pytest
from _pytest.mark import param

from custom_json import ReprInDumps, custom_dumps


class ExampleReprInDumpsClass(ReprInDumps):
    def __repr_in_dumps__(self):
        return 42


class ExampleReprClass(ReprInDumps):
    def __init__(self, a: int):
        self.a = a

    def __repr__(self):
        return f"ExampleReprClass(a={self.a})"


class Outer:
    @dataclass
    class SubDataclass:
        url: str


@dataclass
class ExampleDataclass:
    class_field: ClassVar[int]
    some_field: int
    other_field: str
    hidden_field: bool = field(repr=False)


@dataclass
class InnerDataclass:
    val: int


@dataclass
class OuterDataclass:
    inners: list[InnerDataclass]


@pytest.mark.parametrize(['value', 'expected'], [
    param(1, '1'),
    param(ExampleReprInDumpsClass(), '42'),
    param(ExampleReprClass(1), '"ExampleReprClass(a=1)"'),
    param(int, '{"_t": "PY::class", "key": "int"}'),
    param(ExampleReprClass, '{"_t": "PY::class", "key": "ExampleReprClass"}'),
    param(Outer.SubDataclass, '{"_t": "PY::class", "key": "Outer.SubDataclass"}'),
    param(ExampleDataclass(42, "check", False), '{"some_field": 42, "other_field": "check"}'),
    param(OuterDataclass([InnerDataclass(2), InnerDataclass(3)]), '{"inners": [{"val": 2}, {"val": 3}]}'),
    param(ValueError('Test'), '{"_t": "PY::Exception", "key": "ValueError", "args": ["Test"]}'),
    param(frozenset({1, 2, 3}), '[1, 2, 3]'),
    param({1, 2, 3}, '[1, 2, 3]'),
    param(Decimal('0.030'), '"0.030"'),
    param(b'Hello', '"data:application/octet-stream;base64,SGVsbG8="'),
    param(datetime.date(year=2025, month=1, day=1), '"2025-01-01"'),
    param(datetime.time(hour=12, minute=15, second=0), '"12:15:00"'),
    param(datetime.datetime(year=2025, month=1, day=1, hour=12, minute=15, second=0),
          TypeError('datetime.datetime WITHOUT tzinfo is not JSON serializable')),
    param(datetime.datetime.fromtimestamp(1234567890.1),
          TypeError('datetime.datetime WITHOUT tzinfo is not JSON serializable')),
    param(datetime.datetime(year=2025, month=1, day=1, hour=12, minute=15, second=0, tzinfo=datetime.timezone.utc),
          '"2025-01-01T12:15:00+00:00"'),
])
def test_custom_dumps(value: Any, expected: str | Exception) -> None:
    if isinstance(expected, Exception):
        with pytest.raises(type(expected), match=expected.args[0]):
            custom_dumps(value)
    else:
        assert custom_dumps(value) == expected
