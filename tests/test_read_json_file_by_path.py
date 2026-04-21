import json
from unittest import mock

from wireform import read_json_file_by_path


def test_read_json_file_by_path() -> None:
    with mock.patch("wireform.read_json_file_by_path.open") as open_:
        file = mock.MagicMock()
        open_.return_value.__enter__.return_value = file
        value = {"some": "json"}
        file.read.return_value = json.dumps(value)
        path = mock.Mock()
        assert read_json_file_by_path(path) == value
        open_.assert_called_once_with(path)
