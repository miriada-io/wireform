#  Copyright (C) 2026
#  ABM, Moscow
#
#  UNPUBLISHED PROPRIETARY MATERIAL.
#  ALL RIGHTS RESERVED.
#
#  Authors: Mike Orlov <m.orlov@abm-jsc.ru>
import base64
import datetime
import json
from dataclasses import is_dataclass
from decimal import Decimal
from functools import partial

from type_cast import get_dataclass_field_name_to_field

from .repr_in_dumps import ReprInDumps
from .json_dumper import JsonDumper


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ReprInDumps):
            return o.__repr_in_dumps__()
        if isinstance(o, type):
            return {'_t': 'PY::class', 'key': o.__qualname__}
        if is_dataclass(o):
            return {
                key: getattr(o, key)
                for key, field in get_dataclass_field_name_to_field(type(o), with_init_vars=False).items()
                if field.repr
            }
        if isinstance(o, datetime.datetime):
            if o.tzinfo is None or o.tzinfo.utcoffset(o) is None:  # PROHIBIT naive datetime serialisation
                raise TypeError("TypeError: datetime.datetime WITHOUT tzinfo is not JSON serializable")
        if isinstance(o, datetime.date | datetime.time):  # date or time or datetime
            return o.isoformat()
        if isinstance(o, set | frozenset):
            return tuple(o)
        if isinstance(o, bytes):
            return f'data:application/octet-stream;base64,{base64.b64encode(o).decode("utf-8")}'
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, Exception):
            return {'_t': 'PY::Exception', 'key': type(o).__qualname__, 'args': o.args}
        return super().default(o)


custom_dumps: JsonDumper = partial(json.dumps, cls=EnhancedJSONEncoder)
