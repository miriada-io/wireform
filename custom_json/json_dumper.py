#  Copyright (C) 2026
#  ABM, Moscow
#
#  UNPUBLISHED PROPRIETARY MATERIAL.
#  ALL RIGHTS RESERVED.
#
#  Authors: Mike Orlov <m.orlov@abm-jsc.ru>
from typing import Protocol, Callable, Any

from ._alias import Jsonable, CustomJsonable


class JsonDumper(Protocol):
    @staticmethod
    def __call__(
            obj: CustomJsonable, *, skipkeys: bool = False, ensure_ascii: bool = True, check_circular: bool = True,
            allow_nan: bool = True, indent: int | None = None, separators: tuple[str, str] | None = None,
            default: Callable[[Any], Jsonable] = None, sort_keys: bool = False, **kw
    ) -> str:
        pass
