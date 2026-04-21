import json

from ._alias import JsonLoaded


def read_json_file_by_path(path: str) -> JsonLoaded:
    with open(path) as file:
        return json.load(file)
