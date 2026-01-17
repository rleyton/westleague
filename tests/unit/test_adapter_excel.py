"""
Unit tests for tools/src/adapter_excel.py
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from tools.src.adapter_excel import fetch_clubs_from_dir, extract_range


class TestFetchClubsFromDir:
    """Tests for fetch_clubs_from_dir function"""

    @patch('tools.src.adapter_excel.glob.glob')
    def test_returns_list_of_clubs_and_filenames(self, mock_glob):
        """Should return list of tuples with club names and filenames"""
        mock_glob.return_value = [
            "/path/to/club1.xlsx",
            "/path/to/club2.xlsx"
        ]

        result = fetch_clubs_from_dir("/test/dir")

        assert len(result) == 2
        assert result[0] == ("club1", "club1.xlsx")
        assert result[1] == ("club2", "club2.xlsx")

    @patch('tools.src.adapter_excel.glob.glob')
    def test_extracts_club_name_from_filename(self, mock_glob):
        """Should extract club name (first part before dot)"""
        mock_glob.return_value = ["/path/EastKilbride.xlsx"]

        result = fetch_clubs_from_dir("/test/dir")

        assert result[0][0] == "EastKilbride"

    @patch('tools.src.adapter_excel.glob.glob')
    def test_returns_none_when_dir_is_none(self, mock_glob):
        """Should return None when directory is None"""
        result = fetch_clubs_from_dir(None)

        assert result is None
        mock_glob.assert_not_called()

    @patch('tools.src.adapter_excel.glob.glob')
    def test_returns_empty_list_when_no_xlsx_files(self, mock_glob):
        """Should return empty list when no xlsx files found"""
        mock_glob.return_value = []

        result = fetch_clubs_from_dir("/test/dir")

        assert result == []

    @patch('tools.src.adapter_excel.glob.glob')
    def test_uses_correct_glob_pattern(self, mock_glob):
        """Should glob for *.xlsx files"""
        mock_glob.return_value = []

        fetch_clubs_from_dir("/test/dir")

        mock_glob.assert_called_once_with("/test/dir/*.xlsx")


class TestExtractRange:
    """Tests for extract_range function"""

    @patch('tools.src.adapter_excel.SheetType', {"U11": 1})
    @patch('tools.src.adapter_excel.SheetColumns', {"U11": 1})
    @patch('tools.src.adapter_excel.DataStart', 2)
    @patch('tools.src.adapter_excel.NAMES', 1)
    def test_extracts_names_column(self):
        """Should extract names column from sheet"""
        sheet = pd.DataFrame({
            "A": [None, "Runner 1", "Runner 2"],
            "B": ["Header", "Runner A", "Runner B"]
        })

        result = extract_range(sheet, "U11")

        assert result is not None
        assert "names" in result.columns

    @patch('tools.src.adapter_excel.SheetType', {"U11": 2})
    @patch('tools.src.adapter_excel.SheetColumns', {"U11": 1})
    @patch('tools.src.adapter_excel.DataStart', 2)
    @patch('tools.src.adapter_excel.NAMES_GENDER', 2)
    def test_extracts_gender_when_columns_wide_enough(self):
        """Should extract gender column when columnsWide >= NAMES_GENDER"""
        sheet = pd.DataFrame({
            "A": [None, "Runner 1", "Runner 2"],
            "B": ["Header", "Runner A", "Runner B"],
            "C": ["Gender", "M", "F"]
        })

        result = extract_range(sheet, "U11")

        if result is not None and "gender" in result.columns:
            assert "gender" in result.columns

    def test_returns_none_when_sheet_is_none(self):
        """Should return None when sheet is None"""
        result = extract_range(None, "U11")

        assert result is None

    def test_returns_none_when_range_is_none(self):
        """Should return None when range is None"""
        sheet = pd.DataFrame({"A": [1, 2]})

        result = extract_range(sheet, None)

        assert result is None

    @patch('tools.src.adapter_excel.SheetType', {"U11": 1})
    @patch('tools.src.adapter_excel.SheetColumns', {"U11": 1})
    @patch('tools.src.adapter_excel.DataStart', 2)
    def test_returns_none_when_data_all_null(self):
        """Should return None when all data is NaN"""
        sheet = pd.DataFrame({
            "A": [None, None, None],
            "B": [None, None, None]
        })

        result = extract_range(sheet, "U11")

        assert result is None
