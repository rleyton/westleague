## TODO: Tidy this up, rationalise it


META_KEY_COL = 1
META_VAL_COL = 2
META_MAX_ROW = 9

META_IMPLICIT_GENDER_KEY = "Implicit Gender?"
META_EVENT = "Event"

OVERALL = "OVERALL"

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
    "U12_Girls": 1,
    "U12_Boys": 3,
    "U14_Girls": 5,
    "U14_Boys": 7,
    "U16_Combined": 9,
    "U18_Combined": 12,
    "U20-Senior-Masters_Combined": 15,
}

# grouping criteria for competitions
CompetitionsBreakouts = {
    "default": ["team", "gender"],
    "U20-Senior-Masters_Combined": ["team", "gender", "AgeCat"],
}

SeniorAgeCats = ["senior", "u20", "master"]

DEFAULT_COUNTERS = 3
AgeCatCounterOverrides = {"SENIOR": 4, "OVERALL": 4}
PENALTY_POINTS = 10


NAMES = 1
NAMES_GENDER = 2
NAMES_GENDER_AGECAT = 3

SheetType = {
    "U12_Girls": NAMES,
    "U12_Boys": NAMES,
    "U14_Girls": NAMES,
    "U14_Boys": NAMES,
    "U16_Combined": NAMES_GENDER,
    "U18_Combined": NAMES_GENDER,
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

HTML_DIR = "/html"
MARKDOWN_DIR = "/markdown"
PDF_DIR = "/pdf"
