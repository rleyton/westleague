#!env python

from dotenv import dotenv_values
from google.oauth2.service_account import Credentials
import logging
import gspread
from src.adapter_sheets import load_volunteers, load_results
from src.utils_consts import META_EVENT
from src.utils_config import DATA_DIR
import pandas as pd
import pathlib

logging.basicConfig(level=logging.INFO)
config = dotenv_values(".env")
gc = gspread.service_account()

sheet = gc.open_by_url(config["EVENTSHEET"])

results = []
volunteers = []

# Create output dir
pathlib.Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# Load the worksheets
for worksheet in sheet.worksheets():
    logging.info(f"Processing worksheet: {worksheet}")
    if worksheet.title in config["IGNORE_SHEETS"].split(","):
        logging.debug("Ignoring as in IGNORE_SHEETS")
        next
    else:
        if worksheet.title in config["VOLUNTEER_SHEETS"]:
            logging.debug("Volunteer sheet")
            volunteers.append(worksheet)
        else:
            logging.debug("Results sheet")
            results.append(worksheet)


# Wrangle the worksheets
volunteers = load_volunteers(volunteers)
race_results = load_results(results)

# Process the event volunteers
volunteers = pd.DataFrame({"volunteers": volunteers})
volunteers.to_csv(DATA_DIR + "/" + "volunteers.csv", index=True)
logging.info(f"Processing volunteers")

# Wrangle each of the race data sets
for race in race_results:
    (meta, times, team) = race_results[race]

    event = meta[META_EVENT].replace(" ", "_").replace(",", "-")
    logging.info(f"Processing event: {event}")

    times = pd.DataFrame({"times": times})
    # TODO: Sanity check time sequence
    times.to_csv(DATA_DIR + "/" + event + ".times.csv", index=True)

    places = pd.DataFrame({"team": team})
    places.to_csv(DATA_DIR + "/" + event + ".places.csv", index=True)

    meta = pd.DataFrame({"meta": meta})
    meta.to_csv(DATA_DIR + "/" + event + ".meta.csv", index=True)


logging.info("Finished")
