#!env python

from dotenv import dotenv_values
import logging
from src.adapter_sheets import load_volunteers, load_results
from src.utils_config import DATA_DIR, CLUB_SUBMISSIONS, CLUB_PARSED
from src.adapter_excel import fetch_clubs_from_dir, extract_range
from src.utils_functions import fetch_events_from_dir
import pandas as pd
import pathlib

logging.basicConfig(level=logging.INFO)
pathlib.Path(DATA_DIR + "/" + CLUB_PARSED).mkdir(parents=True, exist_ok=True)

process_dir = f"{DATA_DIR}/{CLUB_SUBMISSIONS}"
logging.info(f"Processing clubs from: {process_dir}")
clubSubmissions = fetch_clubs_from_dir(process_dir)

clubData = {}
for club, filename in clubSubmissions:
    try:
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
    except ValueError as e:
        logging.error(f"Error processing {filename} for {club}: {e}")


logging.info(f"Finished processing {process_dir}")
