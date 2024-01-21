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
            raise Exception(
                "Mismatch on number of times and places (check right source spreadsheet?)"
            )


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
            gender_prefix=gender[:1].upper()

            # Non-Binary in team spreadsheets to A
            if gender_prefix in ['A','N']:
                gender_prefix='A'

            return gender_prefix
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
                if agecat.lower().replace(" ", "").__contains__(category):
                    return category.upper()
            # Some clubs put full agecat or similar, eg. V40, FV40, M40; normalise these down
            if (
                agecat.lower()[:1] == "v"
                or agecat.lower()[:1] == "m"
                or agecat.lower().find("v")
            ):
                return "MASTER"
            elif agecat.lower()[:1] == "s":
                return "SENIOR"
            raise Exception("Unxpected age category: {agecat}")
        else:
            return coreEvent
    else:
        return "SENIOR"


def merge_runners(results=None, clubSubmissions=None, event: str = None):
    reset_club_positions()

    if results is not None and clubSubmissions is not None and len(clubSubmissions) > 0:
        rowCount = 0
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
                    genderMismatch = False
                    for key in tidyColumns.keys():
                        # younger age categories don't have some of these
                        if key in clubSubmissions[clubnum]:
                            col = tidyColumns[key]
                            newValue = clubSubmissions[clubnum].at[clubPosition, key]

                            # TODO: rework as a Lambda?
                            if key == "gender":
                                newValue = normalise_gender_record(
                                    clubSubmissions[clubnum].at[clubPosition, key]
                                )
                                # in the case of Gender, do the submissions match?
                                if newValue != results.at[i, key]:
                                    genderMismatch = True
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
                    results.at[i, col] = "Unknown: {clubname}".format(
                        clubname=results.at[i, "Club name"]
                    )

                if genderMismatch is True:
                    logging.error(
                        f"Event {event}: Mismatched gender for club {row['Club name']} at gendered result position {rowCount+1}, club submission position {clubPosition+1}, Name: {results.at[i,'Name']}. Results gender: {results.at[i,'gender']}, Submitted: {results.at[i,'Gender']}"
                    )

                set_club_position(clubnum, clubPosition + 1)

    # if no age category in the results, add it from the implict event name
    if "AgeCat" not in results.columns:
        results["AgeCat"] = event[:3].upper()

    # check that all submissions have been 'used'
    for club in clubSubmissions:
        lastPosition = get_club_position(clubnum=club)
        if len(clubSubmissions[club]) > lastPosition:
            logging.error(
                f"Event {event}: Club number: {club} has too many submissions - position recording issue?"
            )

    return results


def get_missing_teams(results=None, submissions=None):
    missingTeams = set()
    if results is not None and submissions is not None:
        try:
            theMissingResults = (
                results[results["Name"].isna()]["clubnumber"].unique().tolist()
            )
            for missingResult in theMissingResults:
                if missingResult not in submissions:
                    missingTeams.add(missingResult)
            return missingTeams
        except KeyError as e:
            logging.error(f"No teams received yet? {e}")
            return []
    else:
        return None
