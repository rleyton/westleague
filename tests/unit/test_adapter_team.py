"""
Unit tests for tools/src/adapter_team.py
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from tools.src.adapter_team import process_teams, load_team_submissions


class TestProcessTeams:
    """Tests for process_teams function"""

    def test_adds_clubnumber_column_from_team(self):
        """Should extract club number from team column"""
        df = pd.DataFrame({
            "position": [1, 2, 3],
            "team": ["1M", "2F", "3M"]
        })
        teamdf = pd.DataFrame({
            "Club name": ["Club A", "Club B", "Club C"]
        }, index=[1, 2, 3])
        teamdf.index.name = "clubnumber"

        result = process_teams(df, teamdf)

        assert "clubnumber" in result.columns
        assert list(result["clubnumber"]) == [1, 2, 3]

    def test_joins_with_team_dataframe(self):
        """Should join with team dataframe on clubnumber"""
        df = pd.DataFrame({
            "position": [1, 2],
            "team": ["1M", "2F"]
        })
        teamdf = pd.DataFrame({
            "Club name": ["East Kilbride AC", "Kilmarnock H&AC"]
        }, index=[1, 2])
        teamdf.index.name = "clubnumber"

        result = process_teams(df, teamdf)

        assert "Club name" in result.columns
        assert result.loc[0, "Club name"] == "East Kilbride AC"
        assert result.loc[1, "Club name"] == "Kilmarnock H&AC"

    def test_raises_exception_when_team_column_missing(self):
        """Should raise Exception when 'team' column is missing"""
        df = pd.DataFrame({
            "position": [1, 2, 3]
        })
        teamdf = pd.DataFrame()

        with pytest.raises(Exception) as exc_info:
            process_teams(df, teamdf)

        assert "Not a placings dataframe - expecting team column" in str(exc_info.value)

    def test_returns_joined_dataframe_when_both_inputs_valid(self):
        """Should return properly joined dataframe"""
        df = pd.DataFrame({
            "position": [1, 2, 3],
            "name": ["Runner A", "Runner B", "Runner C"],
            "team": ["5M", "6F", "5M"]
        })
        teamdf = pd.DataFrame({
            "Club name": ["Westerlands CCC", "Cambuslang Harriers"],
            "Website": ["https://westerlandsccc.co.uk/", "https://cambuslangharriers.org/"]
        }, index=[5, 6])
        teamdf.index.name = "clubnumber"

        result = process_teams(df, teamdf)

        assert len(result) == 3
        assert "clubnumber" in result.columns
        assert "Club name" in result.columns
        assert "Website" in result.columns
        assert result.loc[0, "clubnumber"] == 5
        assert result.loc[1, "clubnumber"] == 6

    def test_extracts_numeric_part_from_team_code(self):
        """Should extract numeric club number, removing gender suffix"""
        df = pd.DataFrame({
            "team": ["12M", "345F", "1A"]
        })
        teamdf = pd.DataFrame({
            "Club name": ["Club A", "Club B", "Club C"]
        }, index=[12, 345, 1])
        teamdf.index.name = "clubnumber"

        result = process_teams(df, teamdf)

        assert list(result["clubnumber"]) == [12, 345, 1]

    def test_handles_multi_digit_club_numbers(self):
        """Should correctly parse multi-digit club numbers"""
        df = pd.DataFrame({
            "team": ["123M", "456F", "789M"]
        })
        teamdf = pd.DataFrame({"Club name": ["A", "B", "C"]}, index=[123, 456, 789])
        teamdf.index.name = "clubnumber"

        result = process_teams(df, teamdf)

        assert list(result["clubnumber"]) == [123, 456, 789]

    def test_preserves_original_columns(self):
        """Should preserve all original columns from input dataframe"""
        df = pd.DataFrame({
            "position": [1, 2],
            "name": ["Runner A", "Runner B"],
            "time": ["12:30", "12:45"],
            "team": ["1M", "2F"]
        })
        teamdf = pd.DataFrame({"Club name": ["Club A", "Club B"]}, index=[1, 2])
        teamdf.index.name = "clubnumber"

        result = process_teams(df, teamdf)

        assert "position" in result.columns
        assert "name" in result.columns
        assert "time" in result.columns
        assert "team" in result.columns

    def test_handles_missing_team_data_for_club(self):
        """Should handle case where club number doesn't exist in teamdf"""
        df = pd.DataFrame({
            "team": ["1M", "999F"]  # 999 doesn't exist in teamdf
        })
        teamdf = pd.DataFrame({"Club name": ["Club A"]}, index=[1])
        teamdf.index.name = "clubnumber"

        result = process_teams(df, teamdf)

        # Should still have 2 rows, but club 999 will have NaN values
        assert len(result) == 2
        assert pd.isna(result.loc[1, "Club name"])


class TestLoadTeamSubmissions:
    """Tests for load_team_submissions function"""

    @patch('tools.src.adapter_team.glob.glob')
    @patch('tools.src.adapter_team.pd.read_csv')
    @patch('tools.src.adapter_team.DATA_DIR', '/test/data')
    @patch('tools.src.adapter_team.CLUB_PARSED', 'parsed')
    def test_loads_team_submissions_for_event(self, mock_read_csv, mock_glob):
        """Should load all team submissions for given event"""
        mock_glob.return_value = [
            "/test/data/parsed/1.event1.csv",
            "/test/data/parsed/2.event1.csv"
        ]
        mock_read_csv.side_effect = [
            pd.DataFrame({"name": ["Runner A"]}),
            pd.DataFrame({"name": ["Runner B"]})
        ]

        result = load_team_submissions("event1")

        assert isinstance(result, dict)
        assert len(result) == 2
        assert 1 in result
        assert 2 in result

    @patch('tools.src.adapter_team.glob.glob')
    @patch('tools.src.adapter_team.pd.read_csv')
    @patch('tools.src.adapter_team.DATA_DIR', '/test/data')
    @patch('tools.src.adapter_team.CLUB_PARSED', 'parsed')
    def test_extracts_club_number_from_filename(self, mock_read_csv, mock_glob):
        """Should extract club number from filename correctly"""
        mock_glob.return_value = [
            "/test/data/parsed/123.event1.csv",
            "/test/data/parsed/456.event1.csv"
        ]
        mock_read_csv.return_value = pd.DataFrame({"name": ["Runner"]})

        result = load_team_submissions("event1")

        assert 123 in result
        assert 456 in result

    @patch('tools.src.adapter_team.glob.glob')
    def test_returns_empty_dict_when_no_submissions(self, mock_glob):
        """Should return empty dict when no submissions found"""
        mock_glob.return_value = []

        result = load_team_submissions("event1")

        assert result == {}

    @patch('tools.src.adapter_team.glob.glob')
    @patch('tools.src.adapter_team.pd.read_csv')
    @patch('tools.src.adapter_team.DATA_DIR', '/test/data')
    @patch('tools.src.adapter_team.CLUB_PARSED', 'parsed')
    def test_stores_dataframe_by_club_number(self, mock_read_csv, mock_glob):
        """Should store each club's dataframe by club number as key"""
        mock_glob.return_value = ["/test/data/parsed/5.event1.csv"]
        expected_df = pd.DataFrame({"name": ["Runner A", "Runner B"]})
        mock_read_csv.return_value = expected_df

        result = load_team_submissions("event1")

        assert result[5].equals(expected_df)

    @patch('tools.src.adapter_team.glob.glob')
    @patch('tools.src.adapter_team.DATA_DIR', '/test/data')
    @patch('tools.src.adapter_team.CLUB_PARSED', 'parsed')
    def test_uses_correct_glob_pattern(self, mock_glob):
        """Should use correct glob pattern with DATA_DIR and CLUB_PARSED"""
        mock_glob.return_value = []

        load_team_submissions("event1")

        mock_glob.assert_called_once_with("/test/data/parsed/*event1.csv")
