from collections.abc import Callable
from typing import Any, Protocol

from ._alias import CustomJsonable, Jsonable


class JsonDumper(Protocol):
    @staticmethod
    def __call__(
        obj: CustomJsonable,
        *,
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        indent: int | None = None,
        separators: tuple[str, str] | None = None,
        default: Callable[[Any], Jsonable] = None,
        sort_keys: bool = False,
        **kw,
    ) -> str:
        pass
