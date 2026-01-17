"""
Unit tests for tools/src/utils_functions.py
"""
import pytest
from pathlib import Path
from tools.src.utils_functions import (
    fetch_events_from_dir,
    fetch_volunteers_from_dir,
    fetch_events,
    fetch_results_filenames
)


class TestFetchEventsFromDir:
    """Tests for fetch_events_from_dir function"""

    def test_returns_none_when_dir_is_none(self):
        """Should return None when no directory provided"""
        result = fetch_events_from_dir(None)
        assert result is None

    def test_returns_empty_list_when_no_meta_files(self, tmp_path):
        """Should return empty list when directory has no .meta.csv files"""
        result = fetch_events_from_dir(str(tmp_path))
        assert result == []

    def test_returns_event_names_from_meta_files(self, tmp_path):
        """Should extract event names from .meta.csv files"""
        # Create test meta files
        (tmp_path / "event1.meta.csv").touch()
        (tmp_path / "event2.meta.csv").touch()
        (tmp_path / "event3.meta.csv").touch()

        result = fetch_events_from_dir(str(tmp_path))

        assert len(result) == 3
        assert "event1" in result
        assert "event2" in result
        assert "event3" in result

    def test_ignores_non_meta_csv_files(self, tmp_path):
        """Should only process files matching *.meta.csv pattern"""
        (tmp_path / "event1.meta.csv").touch()
        (tmp_path / "results.csv").touch()
        (tmp_path / "data.txt").touch()

        result = fetch_events_from_dir(str(tmp_path))

        assert len(result) == 1
        assert result[0] == "event1"

    def test_handles_nested_filenames(self, tmp_path):
        """Should handle complex filenames and extract first part"""
        (tmp_path / "complex_event_name.meta.csv").touch()

        result = fetch_events_from_dir(str(tmp_path))

        assert result == ["complex_event_name"]


class TestFetchVolunteersFromDir:
    """Tests for fetch_volunteers_from_dir function"""

    def test_returns_none_when_dir_is_none(self):
        """Should return None when no directory provided"""
        result = fetch_volunteers_from_dir(None)
        assert result is None

    def test_returns_none_when_no_volunteers_file(self, tmp_path):
        """Should return None when volunteers.csv doesn't exist"""
        result = fetch_volunteers_from_dir(str(tmp_path))
        assert result is None

    def test_returns_volunteers_file_path(self, tmp_path):
        """Should return path to volunteers.csv when it exists"""
        volunteers_file = tmp_path / "volunteers.csv"
        volunteers_file.touch()

        result = fetch_volunteers_from_dir(str(tmp_path))

        assert result == str(volunteers_file)

    def test_returns_first_volunteers_file_if_multiple(self, tmp_path):
        """Should return first match if somehow multiple exist"""
        volunteers_file = tmp_path / "volunteers.csv"
        volunteers_file.touch()

        result = fetch_volunteers_from_dir(str(tmp_path))

        assert result is not None
        assert "volunteers.csv" in result


class TestFetchEvents:
    """Tests for fetch_events function"""

    def test_returns_none_when_dir_is_none(self):
        """Should return None when no directory provided"""
        result = fetch_events(None)
        assert result is None

    def test_returns_sorted_event_directories(self, tmp_path):
        """Should return sorted list matching glob pattern dir?"""
        # Create directories/files that match pattern "base_path?"
        # The function appends "?" to the path, so we need files/dirs like "path1", "path2"
        base = tmp_path / "event"
        (tmp_path / "event1").mkdir()
        (tmp_path / "event3").mkdir()
        (tmp_path / "event2").mkdir()

        # Pass path without trailing char
        result = fetch_events(str(tmp_path / "event"))

        assert result is not None
        assert len(result) == 3
        # Should be sorted
        assert result[0].endswith("event1")
        assert result[1].endswith("event2")
        assert result[2].endswith("event3")

    def test_returns_empty_list_when_no_matches(self, tmp_path):
        """Should return empty list when no single-char directories exist"""
        (tmp_path / "event").mkdir()
        (tmp_path / "data").mkdir()

        result = fetch_events(str(tmp_path / ""))

        assert result == []


class TestFetchResultsFilenames:
    """Tests for fetch_results_filenames function"""

    def test_returns_none_when_dir_is_none(self):
        """Should return None when no directory provided"""
        result = fetch_results_filenames(None)
        assert result is None

    def test_returns_empty_list_when_no_team_results(self, tmp_path):
        """Should return empty list when no .team.results.csv files"""
        result = fetch_results_filenames(str(tmp_path))
        assert result == []

    def test_parses_team_results_filenames_correctly(self, tmp_path):
        """Should parse team results files and extract metadata"""
        # Create test files with proper naming pattern
        (tmp_path / "U11.M.team.results.csv").touch()
        (tmp_path / "U13.F.team.results.csv").touch()

        result = fetch_results_filenames(str(tmp_path))

        assert len(result) == 2

        # Check first result
        assert result[0]["eventname"] == "U11"
        assert result[0]["agecat"] == "M"
        assert result[0]["gender"] == "team"
        assert "U11.M.team.results.csv" in result[0]["filename"]

        # Check second result
        assert result[1]["eventname"] == "U13"
        assert result[1]["agecat"] == "F"
        assert result[1]["gender"] == "team"

    def test_ignores_non_team_results_files(self, tmp_path):
        """Should only process files matching *.team.results.csv pattern"""
        (tmp_path / "U11.M.team.results.csv").touch()
        (tmp_path / "other_data.csv").touch()
        (tmp_path / "results.txt").touch()

        result = fetch_results_filenames(str(tmp_path))

        assert len(result) == 1
        assert result[0]["eventname"] == "U11"

    def test_handles_complex_event_names(self, tmp_path):
        """Should handle event names with underscores"""
        (tmp_path / "U20-Senior-Masters_Combined.SENIOR.team.results.csv").touch()

        result = fetch_results_filenames(str(tmp_path))

        assert len(result) == 1
        assert result[0]["eventname"] == "U20-Senior-Masters_Combined"
        assert result[0]["agecat"] == "SENIOR"
        assert result[0]["gender"] == "team"

    def test_filename_includes_full_path(self, tmp_path):
        """Should include full directory path in filename field"""
        (tmp_path / "U11.M.team.results.csv").touch()

        result = fetch_results_filenames(str(tmp_path))

        assert result[0]["filename"].startswith(str(tmp_path))
        assert result[0]["filename"].endswith("U11.M.team.results.csv")
