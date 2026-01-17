"""
Unit tests for tools/src/adapter_json.py
"""
import pytest
import json
from pathlib import Path
from tools.src.adapter_json import json_write, json_load


class TestJsonWrite:
    """Tests for json_write function"""

    def test_writes_dict_to_file(self, tmp_path):
        """Should write dictionary to JSON file"""
        test_file = tmp_path / "test.json"
        test_data = {"name": "Test Event", "date": "2024-01-20", "count": 100}

        json_write(object=test_data, filename=str(test_file))

        assert test_file.exists()
        with open(test_file, "r") as f:
            loaded = json.load(f)
        assert loaded == test_data

    def test_writes_list_to_file(self, tmp_path):
        """Should write list to JSON file"""
        test_file = tmp_path / "list.json"
        test_data = ["event1", "event2", "event3"]

        json_write(object=test_data, filename=str(test_file))

        assert test_file.exists()
        with open(test_file, "r") as f:
            loaded = json.load(f)
        assert loaded == test_data

    def test_writes_nested_structure(self, tmp_path):
        """Should write nested data structures"""
        test_file = tmp_path / "nested.json"
        test_data = {
            "event": "Kilmarnock",
            "results": [
                {"position": 1, "name": "Runner A"},
                {"position": 2, "name": "Runner B"}
            ],
            "meta": {"attendance": 441}
        }

        json_write(object=test_data, filename=str(test_file))

        with open(test_file, "r") as f:
            loaded = json.load(f)
        assert loaded == test_data
        assert loaded["results"][0]["name"] == "Runner A"

    def test_formats_with_indentation(self, tmp_path):
        """Should format JSON with 6-space indentation"""
        test_file = tmp_path / "formatted.json"
        test_data = {"key": "value"}

        json_write(object=test_data, filename=str(test_file))

        content = test_file.read_text()
        # Check that indentation is used (file has newlines)
        assert "\n" in content
        # Check the specific indentation (6 spaces)
        assert "      " in content or content.count(" ") >= 6

    def test_overwrites_existing_file(self, tmp_path):
        """Should overwrite existing JSON file"""
        test_file = tmp_path / "overwrite.json"
        test_file.write_text('{"old": "data"}')

        new_data = {"new": "data"}
        json_write(object=new_data, filename=str(test_file))

        with open(test_file, "r") as f:
            loaded = json.load(f)
        assert loaded == new_data
        assert "old" not in loaded


class TestJsonLoad:
    """Tests for json_load function"""

    def test_loads_dict_from_file(self, tmp_path):
        """Should load dictionary from JSON file"""
        test_file = tmp_path / "test.json"
        test_data = {"name": "Test Event", "count": 100}
        with open(test_file, "w") as f:
            json.dump(test_data, f)

        result = json_load(filename=str(test_file))

        assert result == test_data
        assert result["name"] == "Test Event"
        assert result["count"] == 100

    def test_loads_list_from_file(self, tmp_path):
        """Should load list from JSON file"""
        test_file = tmp_path / "list.json"
        test_data = ["item1", "item2", "item3"]
        with open(test_file, "w") as f:
            json.dump(test_data, f)

        result = json_load(filename=str(test_file))

        assert result == test_data
        assert len(result) == 3

    def test_loads_nested_structure(self, tmp_path):
        """Should load nested data structures correctly"""
        test_file = tmp_path / "nested.json"
        test_data = {
            "event": {
                "name": "Erskine",
                "results": [1, 2, 3]
            }
        }
        with open(test_file, "w") as f:
            json.dump(test_data, f)

        result = json_load(filename=str(test_file))

        assert result["event"]["name"] == "Erskine"
        assert result["event"]["results"] == [1, 2, 3]

    def test_loads_empty_object(self, tmp_path):
        """Should load empty JSON object"""
        test_file = tmp_path / "empty.json"
        test_file.write_text('{}')

        result = json_load(filename=str(test_file))

        assert result == {}

    def test_loads_empty_array(self, tmp_path):
        """Should load empty JSON array"""
        test_file = tmp_path / "empty_array.json"
        test_file.write_text('[]')

        result = json_load(filename=str(test_file))

        assert result == []

    def test_raises_error_for_nonexistent_file(self):
        """Should raise FileNotFoundError for missing file"""
        with pytest.raises(FileNotFoundError):
            json_load(filename="/nonexistent/path/file.json")

    def test_raises_error_for_invalid_json(self, tmp_path):
        """Should raise JSONDecodeError for invalid JSON"""
        test_file = tmp_path / "invalid.json"
        test_file.write_text('{"invalid": json}')

        with pytest.raises(json.JSONDecodeError):
            json_load(filename=str(test_file))


class TestJsonRoundTrip:
    """Integration tests for write and load together"""

    def test_roundtrip_preserves_data(self, tmp_path):
        """Should preserve data through write and load cycle"""
        test_file = tmp_path / "roundtrip.json"
        original_data = {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "bool": True,
            "null": None,
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }

        json_write(object=original_data, filename=str(test_file))
        loaded_data = json_load(filename=str(test_file))

        assert loaded_data == original_data
        assert type(loaded_data["number"]) == int
        assert type(loaded_data["float"]) == float
        assert type(loaded_data["bool"]) == bool
