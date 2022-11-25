import pandas as pd
import numpy as np
import logging
from .utils_consts import SeniorAgeCats


def results_merge(times=None, places=None):
    if times is not None and places is not None:
        if len(times) == len(places):
            results = times.join(other=places, lsuffix="times", rsuffix="places")
            return results
        else:
            raise Exception("Mismatch on number of times and places")


def get_all_possible_columns(results):
    idealCols = [
        "times",
        "team",
        "Name",
        "gender",
        "AgeCat",
        "clubnumber",
        "Club name",
        "Website",
    ]
    columns = []
    for col in idealCols:
        if col in results:
            columns.append(col)
    return columns


def tidy_results(results=None):
    if results is not None:
        availCols = get_all_possible_columns(results)
        returnResults = results[availCols]
        returnResults.insert(
            loc=0, column="position", value=np.arange(len(results)) + 1
        )
        return returnResults
    else:
        return None


# ugh. rework
clubPositions = {}


def reset_club_positions():
    for club in clubPositions:
        clubPositions[club] = 0


def get_club_position(clubnum):
    if clubnum in clubPositions:
        currentClubPosition = clubPositions[clubnum]
    else:
        currentClubPosition = 0
    return currentClubPosition


def set_club_position(clubnum, position):
    clubPositions[clubnum] = position


def normalise_gender_record(gender):
    if gender is not None:
        if type(gender) is str:
            return gender[:1].upper()
        elif np.isnan(gender) is True:
            return ""
    else:
        return ""


def normalise_agecat_record(agecat, event):
    if agecat is not None and type(agecat) is str:
        coreEvent = event[:3].upper()

        # U20_Seniors
        if coreEvent == "U20":
            for category in SeniorAgeCats:
                if agecat.lower().__contains__(category):
                    return category.upper()
            if agecat.lower()[:1] == "v":
                return "MASTER"
            raise Exception("Unxpected age category")
        else:
            return coreEvent
    else:
        return "SENIOR"


def merge_runners(results=None, clubSubmissions=None, event: str = None):

    reset_club_positions()

    if results is not None and clubSubmissions is not None and len(clubSubmissions) > 0:
        for i, row in results.iterrows():
            clubnum = int(row["clubnumber"])
            if clubnum in clubSubmissions:
                clubPosition = get_club_position(clubnum)
                try:
                    tidyColumns = {
                        "names": "Name",
                        "gender": "Gender",
                        "agecat": "AgeCat",
                    }
                    for key in ["names", "gender", "agecat"]:
                        # younger age categories don't have some of these
                        if key in clubSubmissions[clubnum]:
                            col = tidyColumns[key]
                            newValue = clubSubmissions[clubnum].at[clubPosition, key]

                            # TODO: rework as a Lambda?
                            if key == "gender":
                                newValue = normalise_gender_record(
                                    clubSubmissions[clubnum].at[clubPosition, key]
                                )
                            elif key == "agecat":
                                newValue = normalise_agecat_record(
                                    clubSubmissions[clubnum].at[clubPosition, key],
                                    event,
                                )
                            elif key == "names":
                                newValue = (
                                    clubSubmissions[clubnum]
                                    .at[clubPosition, key]
                                    .strip()
                                )

                            results.at[i, col] = newValue

                except KeyError as e:
                    logging.error(
                        f"Insufficient names for club {clubnum} in event {event}"
                    )
                set_club_position(clubnum, clubPosition + 1)

    # if no age category in the results, add it from the implict event name
    if "AgeCat" not in results.columns:
        results["AgeCat"] = event[:3].upper()

    return results
