"""
Unit tests for tools/src/adapter_gender.py
"""
import pytest
import pandas as pd
import numpy as np
from tools.src.adapter_gender import gender_process


class TestGenderProcess:
    """Tests for gender_process function"""

    def test_returns_dataframe_with_gender_column(self):
        """Should add 'gender' column extracted from 'team' column"""
        df = pd.DataFrame({
            "position": [1, 2, 3],
            "name": ["Runner A", "Runner B", "Runner C"],
            "team": ["Team1M", "Team2F", "Team3M"]
        })
        genderdf = pd.DataFrame()  # Mock gender dataframe

        result = gender_process(df, genderdf)

        assert "gender" in result.columns
        assert list(result["gender"]) == ["M", "F", "M"]

    def test_extracts_last_character_from_team(self):
        """Should extract last character from team name as gender"""
        df = pd.DataFrame({
            "team": ["EastKilbrideM", "KilmarnockF", "BellahoustonM", "InverclydeF"]
        })
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert list(result["gender"]) == ["M", "F", "M", "F"]

    def test_handles_single_character_team_names(self):
        """Should handle team names that are single character"""
        df = pd.DataFrame({
            "team": ["M", "F", "A"]
        })
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert list(result["gender"]) == ["M", "F", "A"]

    def test_returns_none_when_df_is_none(self):
        """Should return None when input dataframe is None"""
        genderdf = pd.DataFrame()

        result = gender_process(None, genderdf)

        assert result is None

    def test_returns_unmodified_df_when_genderdf_is_none(self):
        """Should return unmodified dataframe when gender dataframe is None"""
        df = pd.DataFrame({"team": ["Team1M"]})

        result = gender_process(df, None)

        # Function returns original df without adding gender column
        assert result is not None
        assert "gender" not in result.columns
        assert list(result["team"]) == ["Team1M"]

    def test_returns_none_when_both_inputs_are_none(self):
        """Should return None when both inputs are None"""
        result = gender_process(None, None)

        assert result is None

    def test_raises_exception_when_team_column_missing(self):
        """Should raise Exception when 'team' column is missing"""
        df = pd.DataFrame({
            "position": [1, 2, 3],
            "name": ["Runner A", "Runner B", "Runner C"]
        })
        genderdf = pd.DataFrame()

        with pytest.raises(Exception) as exc_info:
            gender_process(df, genderdf)

        assert "Not a placings dataframe - expecting team column" in str(exc_info.value)

    def test_preserves_existing_columns(self):
        """Should preserve all existing columns in dataframe"""
        df = pd.DataFrame({
            "position": [1, 2],
            "name": ["Runner A", "Runner B"],
            "team": ["Team1M", "Team2F"],
            "time": ["12:30", "12:45"]
        })
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert "position" in result.columns
        assert "name" in result.columns
        assert "team" in result.columns
        assert "time" in result.columns
        assert list(result["position"]) == [1, 2]
        assert list(result["name"]) == ["Runner A", "Runner B"]

    def test_handles_empty_dataframe(self):
        """Should handle empty dataframe with team column"""
        # Create empty dataframe with string dtype to avoid .str accessor issues
        df = pd.DataFrame({"team": pd.Series([], dtype=str)})
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert "gender" in result.columns
        assert len(result) == 0

    def test_handles_special_characters_in_team_names(self):
        """Should extract last character even with special chars"""
        df = pd.DataFrame({
            "team": ["Team-1M", "Team_2F", "Team.3A"]
        })
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert list(result["gender"]) == ["M", "F", "A"]

    def test_preserves_dataframe_index(self):
        """Should preserve the original dataframe index"""
        df = pd.DataFrame({
            "team": ["Team1M", "Team2F", "Team3M"]
        }, index=[10, 20, 30])
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert list(result.index) == [10, 20, 30]

    def test_handles_numeric_endings(self):
        """Should extract numeric characters if they are last"""
        df = pd.DataFrame({
            "team": ["Team1", "Team2", "Team9"]
        })
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert list(result["gender"]) == ["1", "2", "9"]

    def test_gender_column_is_string_type(self):
        """Should create gender column as string type"""
        df = pd.DataFrame({
            "team": ["Team1M", "Team2F"]
        })
        genderdf = pd.DataFrame()

        result = gender_process(df, genderdf)

        assert result["gender"].dtype == object  # pandas string type
