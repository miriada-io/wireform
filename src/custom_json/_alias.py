import datetime
from decimal import Decimal
from typing import TypeAlias

from typeful import DataclassProtocol

from .repr_in_dumps import ReprInDumps

JsonLoaded: TypeAlias = list["JsonLoaded"] | dict[str, "JsonLoaded"] | str | int | float | None
Jsonable: TypeAlias = JsonLoaded | list["Jsonable"] | tuple["Jsonable", ...] | dict[str | int, "Jsonable"]
CustomJsonable: TypeAlias = (
    Jsonable
    | list["CustomJsonable"]
    | tuple["CustomJsonable", ...]
    | dict[str | int, "CustomJsonable"]
    | set["CustomJsonable"]
    | frozenset["CustomJsonable"]
    | bytes
    | ReprInDumps
    | type
    | DataclassProtocol
    | datetime.datetime
    | datetime.date
    | datetime.time
    | Decimal
    | Exception
)
