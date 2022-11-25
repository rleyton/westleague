META_KEY_COL = 1
META_VAL_COL = 2
META_MAX_ROW = 9

META_IMPLICIT_GENDER_KEY = "Implicit Gender?"
META_EVENT = "Event"

RESULT_RECORD_ROW = 11
RESULT_TIME_COL = "D"
RESULT_TEAM_COL = "G"
RESULT_GENDER_COL = "H"
RESULT_TIME_RANGE = "{RESULT_TIME_COL}{RESULT_RECORD_ROW}:{RESULT_TIME_COL}".format(
    RESULT_TIME_COL=RESULT_TIME_COL, RESULT_RECORD_ROW=RESULT_RECORD_ROW
)
RESULT_PLACE_TEAM_RANGE = (
    "{RESULT_TEAM_COL}{RESULT_RECORD_ROW}:{RESULT_GENDER_COL}".format(
        RESULT_TEAM_COL=RESULT_TEAM_COL,
        RESULT_RECORD_ROW=RESULT_RECORD_ROW,
        RESULT_GENDER_COL=RESULT_GENDER_COL,
    )
)


# Where to find which competition in the submission spreadsheet
SheetColumns = {
    "U11_Girls": 1,
    "U11_Boys": 3,
    "U13_Girls": 5,
    "U13_Boys": 7,
    "U15_Combined": 9,
    "U17_Combined": 12,
    "U20-Senior-Masters_Combined": 15,
}

# grouping criteria for competitions
CompetitionsBreakouts = {
    "default": ["team", "gender"],
    "U20-Senior-Masters_Combined": ["team", "gender", "AgeCat"],
}

SeniorAgeCats = ["senior", "u20", "master"]

DEFAULT_COUNTERS = 3
AgeCatCounterOverrides = {"SENIOR": 4}
PENALTY_POINTS = 10


NAMES = 1
NAMES_GENDER = 2
NAMES_GENDER_AGECAT = 3

SheetType = {
    "U11_Girls": NAMES,
    "U11_Boys": NAMES,
    "U13_Girls": NAMES,
    "U13_Boys": NAMES,
    "U15_Combined": NAMES_GENDER,
    "U17_Combined": NAMES_GENDER,
    "U20-Senior-Masters_Combined": NAMES_GENDER_AGECAT,
}

GENDER_COMPETITIONS = ["M", "F"]
GENDER_COMPETITION_MAP = {"M": "male", "F": "female"}
NONBINARY = "A"

DataStart = 10


EXT_TIMES = ".times"
EXT_PLACES = ".places"
EXT_META = ".meta"
EXT_CSV = ".csv"
EXT_ADJUSTMENTS = ".adjustments"

# hard-coded for now
DATA_DIR = "data/2022-23/1"
CLUB_SUBMISSIONS = "club-submissions"
CLUB_PARSED = "club-parsed"
RESULTS_DIR = "results/provisional/2022-23/1"
TEAMS = "data/reference/clubs.csv"
GENDERS = "data/reference/genders.csv"
ADJUSTMENTS_DIR = "data/adjustments/2022-23/1"
