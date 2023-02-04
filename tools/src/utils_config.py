from dotenv import dotenv_values

BASE_RESULTS = "results/provisional"
BASE_DATA_DIR = "data"
BASE_ADJUSTMENTS = f"{BASE_DATA_DIR}/adjustments"
DEFAULT_START_YEAR = 2022
DEFAULT_EVENT = 2


config = dotenv_values(".env")

# hard-coded for now
year = config["PROCESS_YEAR"]
event = config["PROCESS_EVENT"]
DATA_DIR = f"{BASE_DATA_DIR}/{year}/{event}"
CLUB_SUBMISSIONS = "club-submissions"
CLUB_PARSED = "club-parsed"
RESULTS_DIR = f"{BASE_RESULTS}/{year}/{event}"
TEAMS = "data/reference/clubs.csv"
GENDERS = "data/reference/genders.csv"
ADJUSTMENTS_DIR = f"data/adjustments/{year}/{event}"
YEAR_RESULTS = f"{BASE_RESULTS}/{year}/"
YEAR_RESULTS_OUTPUT = f"{YEAR_RESULTS}/teamStandings"
