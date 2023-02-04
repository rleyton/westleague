#!env python

from dotenv import dotenv_values
import logging
from src.adapter_sheets import load_volunteers, load_results
from src.adapter_json import json_load
from src.adapter_format import export_results
from src.utils_consts import (
    GENDER_COMPETITION_MAP,
    HTML_DIR,
)
from src.utils_config import TEAMS, GENDERS, BASE_RESULTS, YEAR_RESULTS, RESULTS_DIR
from src.utils_functions import fetch_events
from src.adapter_team_results import (
    load_team_results,
    extract_race_results,
    calculate_team_standings,
)
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

# hard-coded to same location for now
teams = pd.read_csv(TEAMS, index_col="Number")
genders = pd.read_csv(GENDERS, index_col="shortcode")

logging.info(f"Processing year: {YEAR_RESULTS}")
eventDirectories = fetch_events(dir=YEAR_RESULTS)

events = {}
event_meta = {}
# Load the team results from available events
for event in eventDirectories:
    eventNumber = int(event.split("/")[-1:][0])
    logging.info(f"Processing: {event}")
    events[eventNumber] = load_team_results(dir=event)
    event_meta[eventNumber] = json_load(filename=event + "/meta.json")

baseEvent = list(events.keys())[0]

theFiles = []
for competition in events[baseEvent]:
    for gender in GENDER_COMPETITION_MAP:
        logging.info(f"Processing {competition}:{GENDER_COMPETITION_MAP[gender]}")
        raceResults = extract_race_results(
            allEvents=events,
            requiredCompetition=competition,
            requiredGender=GENDER_COMPETITION_MAP[gender],
        )

        teamStandings = calculate_team_standings(
            raceResults=raceResults,
            eventMeta=event_meta,
            competition=competition,
            gender=gender,
        )

        normalisedTeamStandings = teamStandings.join(other=teams)
        resultPages = export_results(
            results=normalisedTeamStandings,
            base_file_name=f"{competition}_{gender}",
            suffix=".team.standings",
        )

        theFiles.append(resultPages["html"].split("/")[-1:][0])


# Render a basic HTML index


def make_clickable(val):
    return f'<a target="_blank" href="{val}">{val}</a>'


filesDF = pd.DataFrame({"teamStandings": theFiles})
filesDF = filesDF.style.format({"teamStandings": make_clickable})

filesDF.to_html(
    RESULTS_DIR + HTML_DIR + "/" + "teamStandings.html",
    index=False,
    render_links=True,
    escape=False,
)

logging.info(f"Finished processing year: {YEAR_RESULTS}")
