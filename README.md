# custom-json

[![PyPI](https://img.shields.io/pypi/v/custom-json.svg?label=PyPI)](https://pypi.org/project/custom-json/)
[![Python](https://img.shields.io/pypi/pyversions/custom-json.svg?label=Python)](https://pypi.org/project/custom-json/)
[![Tests](https://github.com/miriada-io/custom-json/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/miriada-io/custom-json/actions/workflows/tests.yml)
[![License](https://img.shields.io/pypi/l/custom-json.svg?label=License)](https://github.com/miriada-io/custom-json/blob/master/LICENSE)

A `json.dumps` drop-in that serializes dataclasses, `datetime`, `Decimal`, `bytes`, sets, exceptions, and anything you give a `__repr_in_dumps__` to.

## Installation

```bash
pip install custom-json
```

Requires Python 3.11+.

## Why custom-json?

The stdlib `json.dumps` refuses most real-world Python values:

- `json.dumps(MyDataclass(...))` → `TypeError` — dataclasses are not serializable out of the box.
- `json.dumps(datetime.now())` → `TypeError`; same for `date`, `time`, `Decimal`, `bytes`, `set`, `frozenset`, exceptions, and class objects.
- Silently accepting naive `datetime` is a trap — the reader can't tell if the timestamp is UTC or local. `custom-json` refuses naive datetimes by design.
- `dataclasses.asdict` exists, but doesn't respect `field(repr=False)` and can't coexist with custom encoders for other types.

`custom_dumps` is a single callable that handles all of these without schemas, models, or configuration.

## Quick Start

```python
import datetime
from dataclasses import dataclass
from decimal import Decimal

from custom_json import custom_dumps

@dataclass
class Payment:
    amount: Decimal
    currency: str
    paid_at: datetime.datetime

payment = Payment(
    amount=Decimal("19.99"),
    currency="EUR",
    paid_at=datetime.datetime(2026, 4, 18, 12, 0, tzinfo=datetime.UTC),
)

custom_dumps(payment)
# '{"amount": "19.99", "currency": "EUR", "paid_at": "2026-04-18T12:00:00+00:00"}'

custom_dumps({"tags": {"admin", "editor"}, "blob": b"hello"})
# '{"tags": ["admin", "editor"], "blob": "data:application/octet-stream;base64,aGVsbG8="}'

# Naive datetime — refused by design:
custom_dumps(datetime.datetime.now())
# TypeError: datetime.datetime WITHOUT tzinfo is not JSON serializable
```

## Overview

**Serialization:** [`custom_dumps`](#custom_dumps) | [`EnhancedJSONEncoder`](#enhancedjsonencoder) | [`ReprInDumps`](#reprindumps)

**File I/O:** [`read_json_file_by_path`](#read_json_file_by_path)

**Types:** [`JsonLoaded`](#type-aliases) | [`Jsonable`](#type-aliases) | [`CustomJsonable`](#type-aliases) | [`JsonDumper`](#jsondumper)

---

## Serialization

### `custom_dumps`

A `partial(json.dumps, cls=EnhancedJSONEncoder)`. Same signature as `json.dumps`, same return type (`str`), but accepts the extended set of Python values listed below.

```python
from custom_json import custom_dumps

custom_dumps({"a": 1, "b": [1, 2, 3]})
# '{"a": 1, "b": [1, 2, 3]}'
```

Supported values beyond stdlib JSON:

| Python value             | JSON representation                                                       |
|--------------------------|---------------------------------------------------------------------------|
| `@dataclass` instance    | object of fields with `repr=True` (skips `ClassVar`, `InitVar`, `repr=False`) |
| `datetime` (tz-aware)    | ISO 8601 string — `"2026-04-18T12:00:00+00:00"`                           |
| `datetime` (naive)       | raises `TypeError`                                                        |
| `date`, `time`           | ISO 8601 string                                                           |
| `Decimal`                | string — `"19.99"`                                                        |
| `bytes`                  | data URL — `"data:application/octet-stream;base64,..."`                   |
| `set`, `frozenset`       | JSON array (unordered)                                                    |
| `type` (class object)    | `{"_t": "PY::class", "key": "<qualname>"}`                                |
| `Exception` instance     | `{"_t": "PY::Exception", "key": "<type qualname>", "args": [...]}`        |
| `ReprInDumps` subclass   | value returned by `__repr_in_dumps__()`                                   |

### `EnhancedJSONEncoder`

The underlying `json.JSONEncoder` subclass. Pass it to `json.dumps(..., cls=EnhancedJSONEncoder)` if you need the extra `dumps` kwargs directly rather than through `custom_dumps`.

```python
import json
from custom_json import EnhancedJSONEncoder

json.dumps({"x": {1, 2, 3}}, cls=EnhancedJSONEncoder, indent=2)
```

### `ReprInDumps`

Mixin that lets a class control its own JSON form. Subclass it and either (a) override `__repr_in_dumps__` to return any `Jsonable` value, or (b) rely on the default, which delegates to `repr(self)` and produces a JSON string.

```python
from custom_json import ReprInDumps, custom_dumps

class Tag(ReprInDumps):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Tag({self.name!r})"

custom_dumps(Tag("admin"))
# '"Tag(\'admin\')"'


class Version(ReprInDumps):
    def __init__(self, major: int, minor: int):
        self.major = major
        self.minor = minor

    def __repr_in_dumps__(self):
        return {"major": self.major, "minor": self.minor}

custom_dumps(Version(1, 2))
# '{"major": 1, "minor": 2}'
```

## File I/O

### `read_json_file_by_path`

Open a file at the given path and parse it as JSON.

```python
from custom_json import read_json_file_by_path

data = read_json_file_by_path("config.json")
```

Returns a `JsonLoaded` — the exact tree shape you get from `json.load`.

## Type Aliases

- `JsonLoaded` — the strict output shape of `json.load` / `json.loads`: `list`, `dict[str, ...]`, `str`, `int`, `float`, `None`.
- `Jsonable` — anything the **stdlib** `json.dumps` accepts: `JsonLoaded` plus `tuple`, and dicts with `int` keys.
- `CustomJsonable` — anything **`custom_dumps`** accepts: `Jsonable` plus `set`, `frozenset`, `bytes`, `ReprInDumps`, `type`, dataclasses, `datetime`, `date`, `time`, `Decimal`, `Exception`.

### `JsonDumper`

`typing.Protocol` matching the `json.dumps` signature. Use it when you want to type-hint a "something that behaves like `json.dumps`" parameter (e.g. to let callers swap `custom_dumps` for the stdlib version).

```python
from custom_json import JsonDumper, custom_dumps

def render(data, *, dumper: JsonDumper = custom_dumps) -> str:
    return dumper(data, indent=2)
```

## A Note on Roundtripping

`custom_dumps` is a **one-way** encoder. Values like `set`, `bytes`, `Decimal`, class objects and exceptions are encoded to JSON-compatible forms, but `json.loads` will give you back the *encoded* shape (`list`, `str`, etc.), not the original Python type. Use `custom-json` when you need to emit JSON — not when you need a serializer/deserializer round-trip.

## License

[MIT](https://github.com/miriada-io/custom-json/blob/master/LICENSE)
