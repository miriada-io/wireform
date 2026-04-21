import datetime
from decimal import Decimal
from typing import TypeAlias, Union

from typeful import DataclassProtocol

from .repr_in_dumps import ReprInDumps

JsonLoaded: TypeAlias = Union[list['JsonLoaded'], dict[str, 'JsonLoaded'], str, int, float, None]
Jsonable: TypeAlias = Union[JsonLoaded, list['Jsonable'], tuple['Jsonable', ...], dict[str | int, 'Jsonable']]
CustomJsonable: TypeAlias = Union[
    Jsonable, list['CustomJsonable'], tuple['CustomJsonable', ...], dict[str | int, 'CustomJsonable'],
    set['CustomJsonable'], frozenset['CustomJsonable'],
    bytes, ReprInDumps, type, DataclassProtocol, datetime.datetime, datetime.date, datetime.time, Decimal, Exception
]
