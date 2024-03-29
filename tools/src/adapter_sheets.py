from gspread import Worksheet
import logging
from .utils_consts import (
    META_KEY_COL,
    META_VAL_COL,
    META_EVENT,
    META_MAX_ROW,
    RESULT_TIME_RANGE,
    RESULT_PLACE_TEAM_RANGE,
    META_IMPLICIT_GENDER_KEY,
)


def get_volunteer_roles(row):
    if row is not None:
        roles = ";".join([x for x in row[1:] if len(x) > 0])
        return roles
    else:
        return "Volunteer"


def load_volunteers(sheets):
    returnVolunteers = None
    if sheets is not None:
        returnVolunteers = {}
        for sheet in sheets:
            volunteers = sheet.get_all_values()
            for volunteer in volunteers:
                if volunteer[0] != "Name":
                    returnVolunteers[volunteer[0]] = get_volunteer_roles(row=volunteer)

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
        missingValues = 0
        for time in times:
            if len(time.value) == 0:
                missingValues += 1
            else:
                returnTimes.append(time.value)

            if missingValues > 10:
                break

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
            try:
                raceMeta = load_result_meta(sheet)
                times = load_result_times(sheet)
                team = load_result_finishers(
                    sheet=sheet, implicitGender=raceMeta[META_IMPLICIT_GENDER_KEY]
                )
                race = (raceMeta, times, team)
                returnResults[raceMeta[META_EVENT]] = race
            except KeyError as e:
                logging.error(f"Error processing sheet {sheet.title}: {e}")

    return returnResults
