#!env python

from dotenv import dotenv_values
import logging
from src.adapter_sheets import load_volunteers, load_results
from src.adapter_json import json_load
from src.adapter_format import export_results
from src.utils_consts import (
    DATA_DIR,
    TEAMS,
    EXT_TIMES,
    EXT_PLACES,
    EXT_META,
    EXT_ADJUSTMENTS,
    EXT_CSV,
    GENDERS,
    RESULTS_DIR,
    GENDER_COMPETITION_MAP,
    HTML_DIR,
    MARKDOWN_DIR,
    YEAR,
    EVENT,
    BASE_RESULTS
)
from src.utils_functions import fetch_events
from src.adapter_gender import gender_process
from src.adapter_team import process_teams, load_team_submissions
from src.adapter_results import results_merge, tidy_results, merge_runners
from src.adapter_times import adjust_times
from src.adapter_places import adjust_places, process_final_results
from src.adapter_points import calculate_competition_points
from src.adapter_pretty_html import render
from src.adapter_team_results import load_team_results, extract_race_results, calculate_team_standings
import pandas as pd
import pathlib
from pretty_html_table import build_table

logging.basicConfig(level=logging.DEBUG)
config = dotenv_values(".env")

# hard-coded to same location for now
teams = pd.read_csv(TEAMS, index_col="Number")
genders = pd.read_csv(GENDERS, index_col="shortcode")

eventDirectories = fetch_events(
    dir=BASE_RESULTS+"/"+config['PROCESS_YEAR']+"/")

events = {}
event_meta = {}
# Load the team results from available events
for event in eventDirectories:
    eventNumber = int(event.split("/")[-1:][0])
    logging.info(f"Processing: {event}")
    events[eventNumber] = load_team_results(dir=event)
    event_meta[eventNumber] = json_load(filename=event+"/meta.json")

baseEvent = list(events.keys())[0]

theFiles = []
for competition in events[baseEvent]:
    for gender in GENDER_COMPETITION_MAP:
        logging.info(
            f"Processing {competition}:{GENDER_COMPETITION_MAP[gender]}")
        raceResults = extract_race_results(
            allEvents=events, requiredCompetition=competition, requiredGender=GENDER_COMPETITION_MAP[gender])

        teamStandings = calculate_team_standings(
            raceResults=raceResults, eventMeta=event_meta, competition=competition, gender=gender)

        normalisedTeamStandings = teamStandings.join(other=teams)
        resultPages = export_results(results=normalisedTeamStandings,
                                 base_file_name=f"{competition}_{gender}", suffix=".team.standings")
        
        theFiles.append(resultPages["html"].split("/")[-1:][0])


# Render a basic HTML index

def make_clickable(val):
    return f'<a target="_blank" href="{val}">{val}</a>'


filesDF = pd.DataFrame({'teamStandings': theFiles})
filesDF = filesDF.style.format({'teamStandings': make_clickable})

filesDF.to_html(RESULTS_DIR+HTML_DIR+"/"+"teamStandings.html",
                index=False, render_links=True, escape=False)
