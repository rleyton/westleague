"""
Unit tests for tools/src/adapter_places.py
"""
import pytest
import pandas as pd
import datetime
from tools.src.adapter_places import (
    adjust_places,
    check_time_sequence,
    check_gender_match,
    process_final_results
)


class TestAdjustPlaces:
    """Tests for adjust_places function"""

    def test_returns_places_when_adjustments_is_none(self):
        """Should return original places when adjustments is None"""
        places = pd.DataFrame({"position": [1, 2], "team": ["1M", "2F"]})

        result = adjust_places(places, None)

        assert result.equals(places)

    def test_returns_places_when_places_is_none(self):
        """Should return None when places is None"""
        adjustments = pd.DataFrame({"dataset": ["places"]})

        result = adjust_places(None, adjustments)

        assert result is None

    def test_changes_team_number_when_action_is_change(self):
        """Should change team number when action is 'change'"""
        places = pd.DataFrame({
            "position": [1, 2, 3],
            "team": ["1M", "2F", "3M"]
        })
        adjustments = pd.DataFrame({
            "dataset": ["places"],
            "action": ["change"],
            "recordno": [2],  # Change record 2 (index 1)
            "adjustment": [5]  # Change to club 5
        })

        result = adjust_places(places, adjustments)

        # Team at position 2 (index 1) should now be "5F" (number changed, gender preserved)
        assert result.at[1, "team"] == "5F"

    def test_ignores_non_places_dataset_adjustments(self):
        """Should ignore adjustments not for 'places' dataset"""
        places = pd.DataFrame({"position": [1, 2], "team": ["1M", "2F"]})
        adjustments = pd.DataFrame({
            "dataset": ["times", "results"],
            "action": ["change", "change"],
            "recordno": [1, 2],
            "adjustment": [5, 6]
        })

        result = adjust_places(places, adjustments)

        # Should be unchanged
        assert result["team"].tolist() == ["1M", "2F"]

    def test_preserves_gender_suffix_when_changing_club(self):
        """Should preserve gender suffix (last character) when changing club number"""
        places = pd.DataFrame({
            "position": [1, 2, 3],
            "team": ["12M", "34F", "56A"]
        })
        adjustments = pd.DataFrame({
            "dataset": ["places"],
            "action": ["change"],
            "recordno": [1],
            "adjustment": [99]
        })

        result = adjust_places(places, adjustments)

        # Should change 12M to 99M
        assert result.at[0, "team"] == "99M"

    def test_handles_remove_action(self):
        """Should handle 'remove' action (currently just logs)"""
        places = pd.DataFrame({"position": [1, 2], "team": ["1M", "2F"]})
        adjustments = pd.DataFrame({
            "dataset": ["places"],
            "action": ["remove"],
            "recordno": [1],
            "adjustment": [0]
        })

        # Should not raise exception
        result = adjust_places(places, adjustments)

        # Current implementation doesn't actually remove, just logs
        assert len(result) == 2

    def test_handles_insert_action(self):
        """Should handle 'insert' or 'add' action (currently just logs)"""
        places = pd.DataFrame({"position": [1, 2], "team": ["1M", "2F"]})
        adjustments = pd.DataFrame({
            "dataset": ["places"],
            "action": ["insert"],
            "recordno": [1],
            "adjustment": [0]
        })

        # Should not raise exception
        result = adjust_places(places, adjustments)

        # Current implementation doesn't actually insert, just logs
        assert len(result) == 2

    def test_processes_multiple_adjustments(self):
        """Should process multiple adjustments in sequence"""
        places = pd.DataFrame({
            "position": [1, 2, 3],
            "team": ["1M", "2F", "3M"]
        })
        adjustments = pd.DataFrame({
            "dataset": ["places", "places"],
            "action": ["change", "change"],
            "recordno": [1, 3],
            "adjustment": [10, 20]
        })

        result = adjust_places(places, adjustments)

        assert result.at[0, "team"] == "10M"
        assert result.at[2, "team"] == "20M"


class TestCheckTimeSequence:
    """Tests for check_time_sequence function"""

    def test_passes_for_correct_time_sequence(self):
        """Should return True when times are in correct sequence"""
        results = pd.DataFrame({
            "position": [1, 2, 3],
            "times": ["00:12:30", "00:12:45", "00:13:00"]
        })

        result = check_time_sequence(results)

        assert result is True

    def test_passes_for_equal_times(self):
        """Should allow equal consecutive times"""
        results = pd.DataFrame({
            "position": [1, 2, 3],
            "times": ["00:12:30", "00:12:30", "00:12:45"]
        })

        result = check_time_sequence(results)

        assert result is True

    def test_raises_exception_for_out_of_order_times(self):
        """Should raise Exception when times go backwards"""
        results = pd.DataFrame({
            "position": [1, 2, 3],
            "times": ["00:12:30", "00:12:45", "00:12:20"]  # Third time is earlier
        })

        with pytest.raises(Exception) as exc_info:
            check_time_sequence(results)

        assert "Time sequence issue at position 3" in str(exc_info.value)

    def test_handles_single_record(self):
        """Should handle single record without error"""
        results = pd.DataFrame({
            "position": [1],
            "times": ["00:12:30"]
        })

        result = check_time_sequence(results)

        assert result is True

    def test_handles_times_spanning_hour(self):
        """Should correctly compare times across hour boundaries"""
        results = pd.DataFrame({
            "position": [1, 2, 3],
            "times": ["00:59:50", "01:00:10", "01:00:30"]
        })

        result = check_time_sequence(results)

        assert result is True


class TestCheckGenderMatch:
    """Tests for check_gender_match function"""

    def test_passes_when_genders_match(self):
        """Should return True when team gender matches gender column"""
        results = pd.DataFrame({
            "position": [1, 2, 3],
            "team": ["1M", "2F", "3M"],
            "gender": ["M", "F", "M"]
        })

        result = check_gender_match(results)

        assert result is True

    def test_raises_exception_when_genders_mismatch(self):
        """Should raise Exception when genders don't match"""
        results = pd.DataFrame({
            "position": [1, 2],
            "team": ["1M", "2F"],
            "gender": ["M", "M"]  # Second should be F
        })

        with pytest.raises(Exception) as exc_info:
            check_gender_match(results)

        assert "Gender does not match at: 2" in str(exc_info.value)

    def test_handles_case_insensitive_comparison(self):
        """Should handle different cases (M/m, F/f)"""
        results = pd.DataFrame({
            "position": [1, 2],
            "team": ["1M", "2f"],  # lowercase f
            "gender": ["m", "F"]   # lowercase m, uppercase F
        })

        # Should pass as comparison is case-insensitive (uppercased)
        result = check_gender_match(results)

        assert result is True

    def test_handles_non_binary_gender_code(self):
        """Should handle A (non-binary) gender code"""
        results = pd.DataFrame({
            "position": [1, 2],
            "team": ["1A", "2M"],
            "gender": ["A", "M"]
        })

        result = check_gender_match(results)

        assert result is True


class TestProcessFinalResults:
    """Tests for process_final_results function"""

    def test_removes_dnf_record(self):
        """Should remove DNF (did not finish) record"""
        results = pd.DataFrame({
            "position": [1, 2, 3],
            "times": ["00:12:30", "00:12:45", "00:13:00"],
            "team": ["1M", "2M", "3M"],
            "gender": ["M", "M", "M"]
        })
        adjustments = pd.DataFrame({
            "dataset": ["results"],
            "action": ["dnf"],
            "recordno": [2],  # Remove position 2
            "adjustment": [0]
        })

        result = process_final_results(results, adjustments)

        # Should have 2 records instead of 3
        assert len(result) == 2

    def test_adjusts_positions_after_dnf(self):
        """Should adjust positions after removing DNF"""
        results = pd.DataFrame({
            "position": [1, 2, 3, 4],
            "times": ["00:12:30", "00:12:45", "00:13:00", "00:13:15"],
            "team": ["1M", "2M", "3M", "4M"],
            "gender": ["M", "M", "M", "M"]
        })
        adjustments = pd.DataFrame({
            "dataset": ["results"],
            "action": ["dnf"],
            "recordno": [2],  # Remove position 2
            "adjustment": [0]
        })

        result = process_final_results(results, adjustments)

        # Positions 3 and 4 should become 2 and 3
        assert result["position"].tolist() == [1, 2, 3]

    def test_runs_time_sequence_check(self):
        """Should run time sequence check and raise if invalid"""
        results = pd.DataFrame({
            "position": [1, 2],
            "times": ["00:13:00", "00:12:00"],  # Out of order
            "team": ["1M", "2M"],
            "gender": ["M", "M"]
        })
        adjustments = pd.DataFrame(columns=["dataset", "action", "recordno", "adjustment"])

        with pytest.raises(Exception) as exc_info:
            process_final_results(results, adjustments)

        assert "Time sequence issue" in str(exc_info.value)

    def test_runs_gender_match_check(self):
        """Should run gender match check and raise if invalid"""
        results = pd.DataFrame({
            "position": [1, 2],
            "times": ["00:12:30", "00:12:45"],
            "team": ["1M", "2F"],
            "gender": ["M", "M"]  # Mismatch on second
        })
        adjustments = pd.DataFrame(columns=["dataset", "action", "recordno", "adjustment"])

        with pytest.raises(Exception) as exc_info:
            process_final_results(results, adjustments)

        assert "Gender does not match" in str(exc_info.value)

    def test_ignores_non_results_adjustments(self):
        """Should only process 'results' dataset adjustments"""
        results = pd.DataFrame({
            "position": [1, 2],
            "times": ["00:12:30", "00:12:45"],
            "team": ["1M", "2M"],
            "gender": ["M", "M"]
        })
        adjustments = pd.DataFrame({
            "dataset": ["places", "times"],
            "action": ["change", "remove"],
            "recordno": [1, 1],
            "adjustment": [5, 0]
        })

        result = process_final_results(results, adjustments)

        # Should be unchanged (except for validation)
        assert len(result) == 2
