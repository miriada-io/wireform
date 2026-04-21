# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-04-21

### Added
- Initial public release
- `custom_dumps` — `json.dumps` drop-in with extended type support
- `EnhancedJSONEncoder` — `json.JSONEncoder` subclass handling dataclasses, `datetime`/`date`/`time`, `Decimal`, `bytes`, `set`/`frozenset`, `Exception`, class objects, and any `ReprInDumps` subclass
- `ReprInDumps` — mixin that lets a class declare how it appears inside `custom_dumps` output
- `read_json_file_by_path` — read and parse a JSON file by path
- `JsonDumper` — `Protocol` matching the `json.dumps` signature
- Type aliases: `JsonLoaded`, `Jsonable`, `CustomJsonable`
- Naive `datetime` values raise `TypeError` on serialization (timezone-aware only)
- Support for Python 3.11 through 3.14
