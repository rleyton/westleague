#!env python

from dotenv import dotenv_values
import logging
from src.adapter_sheets import load_volunteers, load_results
from src.utils_consts import (
    META_EVENT,
    DATA_DIR,
    CLUB_SUBMISSIONS,
    SheetColumns,
    DataStart,
    CLUB_PARSED,
)
from src.adapter_excel import fetch_clubs_from_dir, extract_range
from src.utils_functions import fetch_events_from_dir
import pandas as pd
import pathlib

logging.basicConfig(level=logging.INFO)
config = dotenv_values(".env")
pathlib.Path(DATA_DIR + "/" + CLUB_PARSED).mkdir(parents=True, exist_ok=True)


clubSubmissions = fetch_clubs_from_dir(DATA_DIR + "/" + CLUB_SUBMISSIONS)

clubData = {}
for club, filename in clubSubmissions:
    if club == "7":
        logging.debug("Break")
        True

    sheet = pd.read_excel(
        io=DATA_DIR + "/" + CLUB_SUBMISSIONS + "/" + filename,
        sheet_name="Submission",
    )
    for event in fetch_events_from_dir(DATA_DIR):
        clubData[event] = extract_range(sheet, event)
        if clubData[event] is not None:
            logging.info(
                f"Processed: club {club} {event} - {len(clubData[event])} records"
            )
            clubData[event].to_csv(
                DATA_DIR + "/" + CLUB_PARSED + "/" + club + "." + event + ".csv",
                index=True,
            )
        else:
            logging.debug("No submissions for event {event}")


logging.info("Finished")
