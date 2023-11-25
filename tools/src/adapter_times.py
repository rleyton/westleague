import pandas as pd
import logging


# merge with other adjustment?
def adjust_times(times, adjustments):
    if times is not None and adjustments is not None:
        newtimes = times["times"]
        for index, row in adjustments.iterrows():
            # most commonly we're going to be inserting a time, based on another
            # logging.debug(f"Processing adjustment {index}")

            if row["dataset"] == "times":
                # get as vars for easier reference, ditto adjustment for zero index
                refrecord = row["refrecord"] - 1

                if row["adjustment"].startswith("="):
                    # records will be by position,  not 0 indexed, so subtract 1
                    recordNum = int(row["adjustment"].replace("=", "")) - 1
                    theTime = times["times"][recordNum]
                    times.loc[refrecord] = (refrecord, theTime)
                    logging.info(f"Added new time record at {recordNum}")
                elif row["adjustment"] == "remove":
                    logging.debug(f"Removing row {row['refrecord']}")
                    times = times.drop(int(row["refrecord"]))

                else:
                    logging.debug(f"Adjustment of {row['adjustment']} ignored")

        returnTimes = times.sort_index().reset_index(drop=True)
        return returnTimes
    else:
        return times
