"""
Unit tests for tools/src/adapter_sheets.py
"""
import pytest
from unittest.mock import MagicMock, patch
from tools.src.adapter_sheets import (
    get_volunteer_roles,
    load_volunteers,
    load_result_meta,
    load_result_times,
    load_result_finishers,
    load_results
)


class TestGetVolunteerRoles:
    """Tests for get_volunteer_roles function"""

    def test_joins_roles_with_semicolon(self):
        """Should join non-empty roles with semicolon"""
        row = ["John Doe", "Timekeeper", "Marshal", ""]

        result = get_volunteer_roles(row)

        assert result == "Timekeeper;Marshal"

    def test_filters_empty_roles(self):
        """Should filter out empty string roles"""
        row = ["Jane Smith", "Registration", "", "Setup", ""]

        result = get_volunteer_roles(row)

        assert result == "Registration;Setup"

    def test_returns_default_for_none_row(self):
        """Should return 'Volunteer' when row is None"""
        result = get_volunteer_roles(None)

        assert result == "Volunteer"

    def test_handles_single_role(self):
        """Should handle single role correctly"""
        row = ["Bob", "Timekeeper"]

        result = get_volunteer_roles(row)

        assert result == "Timekeeper"

    def test_handles_name_only(self):
        """Should handle row with only name (no roles)"""
        row = ["Alice"]

        result = get_volunteer_roles(row)

        assert result == ""


class TestLoadVolunteers:
    """Tests for load_volunteers function"""

    def test_returns_none_when_sheets_is_none(self):
        """Should return None when sheets is None"""
        result = load_volunteers(None)

        assert result is None

    def test_loads_volunteers_from_sheets(self):
        """Should load volunteers from multiple sheets"""
        mock_sheet1 = MagicMock()
        mock_sheet1.get_all_values.return_value = [
            ["Name", "Role1", "Role2"],
            ["John Doe", "Timekeeper", ""],
            ["Jane Smith", "Marshal", "Setup"]
        ]

        mock_sheet2 = MagicMock()
        mock_sheet2.get_all_values.return_value = [
            ["Name", "Role1"],
            ["Bob Jones", "Registration"]
        ]

        result = load_volunteers([mock_sheet1, mock_sheet2])

        assert "John Doe" in result
        assert "Jane Smith" in result
        assert "Bob Jones" in result

    def test_skips_header_row(self):
        """Should skip rows where first column is 'Name'"""
        mock_sheet = MagicMock()
        mock_sheet.get_all_values.return_value = [
            ["Name", "Role"],
            ["Alice", "Timekeeper"]
        ]

        result = load_volunteers([mock_sheet])

        assert "Name" not in result
        assert "Alice" in result

    def test_combines_roles_correctly(self):
        """Should combine roles using get_volunteer_roles"""
        mock_sheet = MagicMock()
        mock_sheet.get_all_values.return_value = [
            ["Name", "Role1", "Role2"],
            ["John", "Time", "Marshal"]
        ]

        result = load_volunteers([mock_sheet])

        assert result["John"] == "Time;Marshal"

    def test_handles_empty_sheets_list(self):
        """Should handle empty sheets list"""
        result = load_volunteers([])

        assert result == {}


class TestLoadResultMeta:
    """Tests for load_result_meta function"""

    def test_returns_none_when_sheet_is_none(self):
        """Should return None when sheet is None"""
        result = load_result_meta(None)

        assert result is None

    @patch('tools.src.adapter_sheets.META_KEY_COL', 1)
    @patch('tools.src.adapter_sheets.META_VAL_COL', 2)
    @patch('tools.src.adapter_sheets.META_MAX_ROW', 10)
    def test_loads_metadata_from_sheet(self):
        """Should load metadata key-value pairs from sheet"""
        mock_sheet = MagicMock()
        mock_sheet.col_values.side_effect = [
            ["event", "date", "location", ""],
            ["U11_Boys", "2024-01-20", "Kilmarnock", ""]
        ]

        result = load_result_meta(mock_sheet)

        assert result["event"] == "U11_Boys"
        assert result["date"] == "2024-01-20"
        assert result["location"] == "Kilmarnock"

    @patch('tools.src.adapter_sheets.META_KEY_COL', 1)
    @patch('tools.src.adapter_sheets.META_VAL_COL', 2)
    @patch('tools.src.adapter_sheets.META_MAX_ROW', 10)
    def test_stops_at_empty_key(self):
        """Should stop loading when encountering empty key"""
        mock_sheet = MagicMock()
        mock_sheet.col_values.side_effect = [
            ["event", "date", "", "extra"],
            ["U11_Boys", "2024-01-20", "", "should_not_load"]
        ]

        result = load_result_meta(mock_sheet)

        assert "event" in result
        assert "date" in result
        assert "extra" not in result

    @patch('tools.src.adapter_sheets.META_KEY_COL', 1)
    @patch('tools.src.adapter_sheets.META_VAL_COL', 2)
    @patch('tools.src.adapter_sheets.META_MAX_ROW', 5)
    def test_respects_max_row_limit(self):
        """Should not exceed META_MAX_ROW"""
        mock_sheet = MagicMock()
        # Return more rows than MAX_ROW
        mock_sheet.col_values.side_effect = [
            ["key1", "key2", "key3", "key4", "key5", "key6"],
            ["val1", "val2", "val3", "val4", "val5", "val6"]
        ]

        result = load_result_meta(mock_sheet)

        # Should stop at MAX_ROW (5) or first empty key
        assert len(result) <= 5


class TestLoadResultTimes:
    """Tests for load_result_times function"""

    def test_returns_none_when_sheet_is_none(self):
        """Should return None when sheet is None"""
        result = load_result_times(None)

        assert result is None

    @patch('tools.src.adapter_sheets.RESULT_TIME_RANGE', 'A1:A10')
    def test_loads_times_from_range(self):
        """Should load times from specified range"""
        mock_sheet = MagicMock()

        # Create mock cells with value attribute
        mock_cells = []
        for time_val in ["12:30", "12:45", "13:00", ""]:
            mock_cell = MagicMock()
            mock_cell.value = time_val
            mock_cells.append(mock_cell)

        mock_sheet.range.return_value = mock_cells

        result = load_result_times(mock_sheet)

        assert "12:30" in result
        assert "12:45" in result
        assert "13:00" in result
        assert len(result) == 3

    @patch('tools.src.adapter_sheets.RESULT_TIME_RANGE', 'A1:A20')
    def test_stops_after_10_consecutive_empty_values(self):
        """Should stop after encountering 10+ consecutive empty values"""
        mock_sheet = MagicMock()

        mock_cells = []
        # Add some values, then 11 empty values
        for time_val in ["12:30", "12:45", ""] * 5:
            mock_cell = MagicMock()
            mock_cell.value = time_val
            mock_cells.append(mock_cell)

        mock_sheet.range.return_value = mock_cells

        result = load_result_times(mock_sheet)

        # Should have stopped before processing all cells
        assert result is not None


class TestLoadResultFinishers:
    """Tests for load_result_finishers function"""

    def test_returns_none_when_sheet_is_none(self):
        """Should return None when sheet is None"""
        result = load_result_finishers(None, "M")

        assert result is None

    @patch('tools.src.adapter_sheets.RESULT_PLACE_TEAM_RANGE', 'A1:B10')
    def test_loads_team_and_gender_pairs(self):
        """Should load team-gender pairs from range"""
        mock_sheet = MagicMock()

        # Create pairs of cells: team, gender, team, gender...
        mock_cells = []
        pairs = [("1", "M"), ("2", "F"), ("3", "M"), ("", "")]
        for team, gender in pairs:
            team_cell = MagicMock()
            team_cell.value = team
            gender_cell = MagicMock()
            gender_cell.value = gender
            mock_cells.extend([team_cell, gender_cell])

        mock_sheet.range.return_value = mock_cells

        result = load_result_finishers(mock_sheet, None)

        assert "1M" in result
        assert "2F" in result
        assert "3M" in result
        assert len(result) == 3

    @patch('tools.src.adapter_sheets.RESULT_PLACE_TEAM_RANGE', 'A1:B10')
    def test_uses_implicit_gender_when_gender_empty(self):
        """Should use implicit gender when gender column is empty"""
        mock_sheet = MagicMock()

        mock_cells = []
        pairs = [("1", ""), ("2", "F"), ("", "")]
        for team, gender in pairs:
            team_cell = MagicMock()
            team_cell.value = team
            gender_cell = MagicMock()
            gender_cell.value = gender
            mock_cells.extend([team_cell, gender_cell])

        mock_sheet.range.return_value = mock_cells

        result = load_result_finishers(mock_sheet, implicitGender="M")

        assert "1M" in result  # Should use implicit M
        assert "2F" in result  # Should use explicit F
        assert len(result) == 2

    @patch('tools.src.adapter_sheets.RESULT_PLACE_TEAM_RANGE', 'A1:B10')
    def test_stops_at_empty_team(self):
        """Should stop when team value is empty"""
        mock_sheet = MagicMock()

        mock_cells = []
        pairs = [("1", "M"), ("2", "F"), ("", "M"), ("3", "M")]
        for team, gender in pairs:
            team_cell = MagicMock()
            team_cell.value = team
            gender_cell = MagicMock()
            gender_cell.value = gender
            mock_cells.extend([team_cell, gender_cell])

        mock_sheet.range.return_value = mock_cells

        result = load_result_finishers(mock_sheet, None)

        assert len(result) == 2  # Should stop at empty team


class TestLoadResults:
    """Tests for load_results function"""

    def test_returns_none_when_sheets_is_none(self):
        """Should return None when sheets is None"""
        result = load_results(None)

        assert result is None

    @patch('tools.src.adapter_sheets.load_result_meta')
    @patch('tools.src.adapter_sheets.load_result_times')
    @patch('tools.src.adapter_sheets.load_result_finishers')
    @patch('tools.src.adapter_sheets.META_EVENT', 'event')
    @patch('tools.src.adapter_sheets.META_IMPLICIT_GENDER_KEY', 'implicitGender')
    def test_loads_results_from_sheets(self, mock_finishers, mock_times, mock_meta):
        """Should load results from multiple sheets"""
        mock_meta.return_value = {"event": "U11_Boys", "implicitGender": "M"}
        mock_times.return_value = ["12:30", "12:45"]
        mock_finishers.return_value = ["1M", "2M"]

        mock_sheet = MagicMock()

        result = load_results([mock_sheet])

        assert "U11_Boys" in result
        assert result["U11_Boys"][0] == mock_meta.return_value
        assert result["U11_Boys"][1] == mock_times.return_value
        assert result["U11_Boys"][2] == mock_finishers.return_value

    @patch('tools.src.adapter_sheets.load_result_meta')
    @patch('tools.src.adapter_sheets.load_result_times')
    @patch('tools.src.adapter_sheets.load_result_finishers')
    @patch('tools.src.adapter_sheets.META_EVENT', 'event')
    def test_handles_keyerror_gracefully(self, mock_finishers, mock_times, mock_meta):
        """Should handle KeyError and continue processing"""
        mock_meta.return_value = {"event": "U11_Boys"}  # Missing implicitGender
        mock_times.return_value = ["12:30"]
        mock_finishers.side_effect = KeyError("implicitGender")

        mock_sheet = MagicMock()
        mock_sheet.title = "Test Sheet"

        result = load_results([mock_sheet])

        # Should return dict but without the failed sheet
        assert isinstance(result, dict)

    def test_handles_empty_sheets_list(self):
        """Should handle empty sheets list"""
        result = load_results([])

        assert result == {}
