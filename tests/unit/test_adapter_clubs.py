"""
Unit tests for tools/src/adapter_clubs.py
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from tools.src.adapter_clubs import load_clubs


class TestLoadClubs:
    """Tests for load_clubs function"""

    @patch('tools.src.adapter_clubs.pd.read_csv')
    @patch('tools.src.adapter_clubs.TEAMS', 'data/reference/clubs.csv')
    def test_load_clubs_reads_from_teams_constant(self, mock_read_csv):
        """Should read clubs from the TEAMS constant path"""
        # Create a mock dataframe
        mock_df = pd.DataFrame({
            "Number": [1, 2, 3],
            "Club name": ["Club A", "Club B", "Club C"],
            "Website": ["http://a.com", "http://b.com", "http://c.com"]
        })
        mock_read_csv.return_value = mock_df.set_index("Number")

        result = load_clubs()

        # Verify read_csv was called with correct path
        mock_read_csv.assert_called_once_with('data/reference/clubs.csv', index_col="Number")
        assert result is not None

    @patch('tools.src.adapter_clubs.pd.read_csv')
    def test_load_clubs_sets_number_as_index(self, mock_read_csv):
        """Should set 'Number' column as the index"""
        mock_df = pd.DataFrame({
            "Number": [1, 2, 3],
            "Club name": ["Club A", "Club B", "Club C"]
        }).set_index("Number")
        mock_read_csv.return_value = mock_df

        result = load_clubs()

        # Verify index_col parameter was used
        mock_read_csv.assert_called_once()
        call_args = mock_read_csv.call_args
        assert call_args[1]["index_col"] == "Number"

    @patch('tools.src.adapter_clubs.pd.read_csv')
    def test_load_clubs_returns_dataframe(self, mock_read_csv):
        """Should return a pandas DataFrame"""
        mock_df = pd.DataFrame({
            "Club name": ["Club A", "Club B"],
            "Website": ["http://a.com", "http://b.com"]
        })
        mock_read_csv.return_value = mock_df

        result = load_clubs()

        assert isinstance(result, pd.DataFrame)

    def test_load_clubs_with_real_file(self, sample_clubs_csv):
        """Integration test: Should load actual CSV file correctly"""
        # Temporarily patch TEAMS constant to use our test file
        with patch('tools.src.adapter_clubs.TEAMS', sample_clubs_csv):
            result = load_clubs()

            assert isinstance(result, pd.DataFrame)
            assert len(result) == 3
            assert "Club name" in result.columns
            assert "Website" in result.columns
            # Check index is set correctly
            assert result.index.name == "Number"
            assert list(result.index) == [1, 2, 3]

    def test_load_clubs_contains_expected_columns(self, sample_clubs_csv):
        """Should load dataframe with expected columns"""
        with patch('tools.src.adapter_clubs.TEAMS', sample_clubs_csv):
            result = load_clubs()

            expected_columns = ["Club name", "Website"]
            for col in expected_columns:
                assert col in result.columns

    def test_load_clubs_data_integrity(self, sample_clubs_csv):
        """Should preserve data integrity from CSV"""
        with patch('tools.src.adapter_clubs.TEAMS', sample_clubs_csv):
            result = load_clubs()

            # Check first club
            assert result.loc[1, "Club name"] == "East Kilbride AC"
            assert result.loc[1, "Website"] == "http://www.ekac.org.uk/"

            # Check second club
            assert result.loc[2, "Club name"] == "Kilmarnock H&AC"
            assert result.loc[2, "Website"] == "http://www.kilmarnockharriers.com/"

    @patch('tools.src.adapter_clubs.pd.read_csv')
    def test_load_clubs_handles_file_not_found(self, mock_read_csv):
        """Should propagate FileNotFoundError if CSV doesn't exist"""
        mock_read_csv.side_effect = FileNotFoundError("clubs.csv not found")

        with pytest.raises(FileNotFoundError):
            load_clubs()
