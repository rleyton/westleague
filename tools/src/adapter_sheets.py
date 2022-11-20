from gspread import Worksheet
from .utils_consts import (
    META_KEY_COL,
    META_VAL_COL,
    META_EVENT,
    META_MAX_ROW,
    RESULT_TIME_RANGE,
    RESULT_PLACE_TEAM_RANGE,
    META_IMPLICIT_GENDER_KEY,
)


def load_volunteers(sheets):
    returnVolunteers = None
    if sheets is not None:
        returnVolunteers = {}
        for sheet in sheets:
            volunteers = sheet.get_all_values()
            for volunteer in volunteers:
                if volunteer[0] != "Name":
                    returnVolunteers[volunteer[0]] = volunteer[1]

    return returnVolunteers


def load_meta_row(sheet: Worksheet = None, rowNum: int = None):
    if rowNum is not None and sheet is not None:
        key = sheet.cell()


def load_result_meta(sheet: Worksheet = None):
    returnMeta = None
    if sheet is not None:
        returnMeta = {}

        keys = sheet.col_values(META_KEY_COL)
        values = sheet.col_values(META_VAL_COL)

        rowNum = 0

        while len(keys[rowNum]) > 0 and rowNum < META_MAX_ROW:
            returnMeta[keys[rowNum]] = values[rowNum]
            rowNum += 1

    return returnMeta


def load_result_times(sheet: Worksheet = None):
    returnTimes = None
    if sheet is not None:
        returnTimes = []
        times = sheet.range(RESULT_TIME_RANGE)
        for time in times:
            if len(time.value) == 0:
                # reached the end
                break
            else:
                returnTimes.append(time.value)

    return returnTimes


def load_result_finishers(sheet: Worksheet = None, implicitGender: str = None):
    returnTimes = None
    if sheet is not None:
        returnTimes = []
        places = sheet.range(RESULT_PLACE_TEAM_RANGE)
        placesIterator = iter(places)
        for place in placesIterator:
            (team, gender) = (place.value, next(placesIterator).value)
            if len(gender) == 0:
                gender = implicitGender
            if len(team) == 0:
                # reached the end
                break
            else:
                returnTimes.append(f"{team}{gender}")
    return returnTimes


def load_results(sheets):
    returnResults = None
    if sheets is not None:
        returnResults = {}
        for sheet in sheets:
            raceMeta = load_result_meta(sheet)
            times = load_result_times(sheet)
            team = load_result_finishers(
                sheet=sheet, implicitGender=raceMeta[META_IMPLICIT_GENDER_KEY]
            )
            race = (raceMeta, times, team)
            returnResults[raceMeta[META_EVENT]] = race

    return returnResults
