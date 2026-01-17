"""
Shared pytest fixtures for West League XC Results tests
"""
import pytest
import pandas as pd
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def sample_clubs_csv(tmp_path):
    """Create a sample clubs.csv file for testing"""
    csv_content = """Number,Club name,Website
1,East Kilbride AC,http://www.ekac.org.uk/
2,Kilmarnock H&AC,http://www.kilmarnockharriers.com/
3,Bellahouston RR,https://www.bellahoustonroadrunners.co.uk/
"""
    csv_file = tmp_path / "clubs.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def sample_clubs_df():
    """Create a sample clubs dataframe for testing"""
    data = {
        "Number": [1, 2, 3],
        "Club name": ["East Kilbride AC", "Kilmarnock H&AC", "Bellahouston RR"],
        "Website": [
            "http://www.ekac.org.uk/",
            "http://www.kilmarnockharriers.com/",
            "https://www.bellahoustonroadrunners.co.uk/"
        ]
    }
    return pd.DataFrame(data).set_index("Number")


@pytest.fixture
def sample_results_df():
    """Create a sample results dataframe for testing"""
    data = {
        "position": [1, 2, 3, 4, 5],
        "name": ["Runner A", "Runner B", "Runner C", "Runner D", "Runner E"],
        "team": ["Team1M", "Team2F", "Team1M", "Team3F", "Team2F"],
        "time": ["12:30", "12:45", "13:00", "13:15", "13:30"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory structure for testing"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Create subdirectories
    (data_dir / "2023-24" / "1").mkdir(parents=True)
    (data_dir / "reference").mkdir(parents=True)

    return str(data_dir)


@pytest.fixture
def temp_results_dir(tmp_path):
    """Create a temporary results directory for testing"""
    results_dir = tmp_path / "results" / "provisional" / "2023-24" / "1"
    results_dir.mkdir(parents=True)
    return str(results_dir)


@pytest.fixture
def sample_meta_csv(tmp_path):
    """Create sample meta CSV files for event testing"""
    event_dir = tmp_path / "events"
    event_dir.mkdir()

    # Create sample event meta files
    (event_dir / "event1.meta.csv").write_text("event,date\nevent1,2023-11-18")
    (event_dir / "event2.meta.csv").write_text("event,date\nevent2,2024-01-20")

    return str(event_dir)


@pytest.fixture
def sample_team_results_csv(tmp_path):
    """Create sample team results CSV file"""
    csv_content = """position,team,points,runners
1,Team1,15,5
2,Team2,35,5
3,Team3,45,4
"""
    csv_file = tmp_path / "U11.M.team.results.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def sample_volunteers_csv(tmp_path):
    """Create sample volunteers CSV file"""
    csv_content = """name,role
Volunteer A,Timekeeper
Volunteer B,Marshal
Volunteer C,Registration
"""
    csv_file = tmp_path / "volunteers.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


@pytest.fixture
def mock_env_config(monkeypatch):
    """Mock environment configuration values"""
    test_config = {
        "PROCESS_YEAR": "2023-24",
        "PROCESS_EVENT": "1"
    }

    # Mock dotenv_values to return test config
    monkeypatch.setattr(
        "tools.src.utils_config.config",
        test_config
    )

    return test_config
