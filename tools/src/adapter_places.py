import pandas as pd
import logging
import re
import numpy as np
import datetime


def adjust_places(places, adjustments):
    if places is not None and adjustments is not None:
        for index, row in adjustments.iterrows():
            # most commonly we're going to be inserting a time, based on another
            # logging.debug(f"Processing adjustment")

            if row["dataset"] == "places":
                # get as vars for easier reference, ditto adjustment for zero index

                if row["action"] == "change":
                    # records will be by position,  not 0 indexed, so subtract 1
                    recordNum = int(row["recordno"]) - 1
                    curTeam = places.at[recordNum, "team"]
                    places.at[recordNum, "team"] = re.sub(
                        "\d+", str(row["adjustment"]), curTeam
                    )
                    newVal = places.at[recordNum, "team"]
                    logging.info(
                        f"Changing recorded club for place {recordNum} from {curTeam} to {newVal}"
                    )
                if row["action"] == "remove":
                    logging.info(f"Remove record?")
                else:
                    logging.debug(f"Adjustment of {row['adjustment']} ignored")

        return places
    else:
        return places


def check_time_sequence(results):
    previousTime = datetime.datetime.strptime("00:00:00", "%H:%M:%S")
    for index, row in results.iterrows():
        theTime = datetime.datetime.strptime(row["times"], "%H:%M:%S")
        if theTime < previousTime:
            raise Exception(f"Time sequence issue at position {row['position']}")
        else:
            previousTime = theTime

    return True


def check_gender_match(results):
    for index, row in results.iterrows():
        placeGender = str(row["team"][-1:]).upper()
        teamGender = str(row["gender"]).upper()
        if teamGender != placeGender:
            raise Exception(f"Gender does not match at: {row['position']}")

    return True


def process_final_results(results, adjustments):
    if results is not None and adjustments is not None:
        for index, row in adjustments.iterrows():
            # most commonly we're going to be inserting a time, based on another
            # logging.debug(f"Processing adjustment {index}")

            if row["dataset"] == "results":
                # get as vars for easier reference, ditto adjustment for zero index

                if row["action"] == "dnf":
                    # TODO: name match?
                    record = row["recordno"]

                    logging.info(f"Remove finishing position {record}")
                    # zero index adjustment
                    results = results.drop([record - 1])

                    # results["position"] = np.where(results["position"] >= record, results["position"]-1 , results["position"])
                    results["position"] = results["position"].apply(
                        lambda x: x - 1 if x >= record else x
                    )
                else:
                    logging.debug(f"Adjustment of {row['adjustment']} ignored")

    check_time_sequence(results)
    check_gender_match(results)
    return results
