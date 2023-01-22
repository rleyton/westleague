#!env python

from dotenv import dotenv_values
import logging
from src.adapter_sheets import load_volunteers, load_results
from src.utils_consts import (
    DATA_DIR,
    ADJUSTMENTS_DIR,
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
    MARKDOWN_DIR
)
from src.utils_functions import fetch_events_from_dir
from src.adapter_gender import gender_process
from src.adapter_team import process_teams, load_team_submissions
from src.adapter_results import results_merge, tidy_results, merge_runners
from src.adapter_times import adjust_times
from src.adapter_places import adjust_places, process_final_results
from src.adapter_points import calculate_competition_points
from src.adapter_pretty_html import render
import pandas as pd
import pathlib
from pretty_html_table import build_table

logging.basicConfig(level=logging.DEBUG)
config = dotenv_values(".env")

# hard-coded to same location for now
SOURCE_DATA = DATA_DIR

pathlib.Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(RESULTS_DIR+MARKDOWN_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(RESULTS_DIR+HTML_DIR).mkdir(parents=True, exist_ok=True)


teams = pd.read_csv(TEAMS, index_col="Number")
genders = pd.read_csv(GENDERS, index_col="shortcode")

results = {}
leagueResults = {}
teamResults = {}

# for each event we have files for
for event in fetch_events_from_dir(DATA_DIR):
    logging.debug(f"Processing: {event}")

    clubSubmissions = None

    record = {}

    # Check if we have adjustments
    try:
        record["adjustments"] = pd.read_csv(
            ADJUSTMENTS_DIR + "/" + event + EXT_ADJUSTMENTS + EXT_CSV
        )
    except FileNotFoundError as e:
        record["adjustments"] = None
        logging.debug(f"No adjustments for {event}")

    # apply the adjustments
    record["times"] = adjust_times(
        pd.read_csv(DATA_DIR + "/" + event + EXT_TIMES + EXT_CSV),
        adjustments=record["adjustments"],
    )

    # read the csv, and build a places (finish order) DataFrame
    record["places"] = process_teams(
        adjust_places(
            gender_process(
                pd.read_csv(DATA_DIR + "/" + event + EXT_PLACES + EXT_CSV),
                genderdf=genders,
            ),
            adjustments=record["adjustments"],
        ),
        teamdf=teams,
    )

    # Load the meta record
    record["meta"] = pd.read_csv(DATA_DIR + "/" + event + EXT_META + EXT_CSV)

    # Build a team submissions (finish order, per club) DataFrame
    clubSubmissions = load_team_submissions(event=event)

    # Do the main results processing:
    #  * Join the times to the finish order
    #  * Apply the club names to the resulting data frame
    #  * do some tidy-up
    try:
        results[event] = process_final_results(
            tidy_results(
                merge_runners(
                    results_merge(
                        times=record["times"], places=record["places"]),
                    clubSubmissions=clubSubmissions,
                    event=event,
                )
            ),
            adjustments=record["adjustments"],
        )
    except Exception as e:
        raise Exception(f"Problem processing event {event}: {e}")

    # Now we have a results DataFrame, so process the competition results
    teamResults[event] = calculate_competition_points(
        results=results[event], teams=teams, event=event
    )

    # Produce the CSV outputs

    # core results
    if results[event] is not None:
        results[event].to_csv(RESULTS_DIR + "/" + event +
                              ".results.csv", index=False)
        results[event].to_markdown(
            RESULTS_DIR+MARKDOWN_DIR + "/" + event + ".results.md", index=False)
        render(df=results[event], style='blue_light',
               filename=RESULTS_DIR+HTML_DIR + "/" + event + ".results.html")
    else:
        raise Exception(f"Unexpectedly no merged results for event {event}")

    # team results
    if teamResults[event] is not None:
        for gender in teamResults[event]:
            for competition in teamResults[event][gender]:
                teamResults[event][gender][competition].to_csv(
                    RESULTS_DIR
                    + "/"
                    + event
                    + "."
                    + competition
                    + "."
                    + GENDER_COMPETITION_MAP[gender]
                    + ".team.results.csv",
                    index=False,
                )
                teamResults[event][gender][competition].to_markdown(
                    RESULTS_DIR+MARKDOWN_DIR
                    + "/"
                    + event
                    + "."
                    + competition
                    + "."
                    + GENDER_COMPETITION_MAP[gender]
                    + ".team.results.md",
                    index=False,
                )
                render(df=teamResults[event][gender][competition], style='blue_light', filename=RESULTS_DIR+HTML_DIR
                       + "/"
                       + event
                       + "."
                       + competition
                       + "."
                       + GENDER_COMPETITION_MAP[gender]
                       + ".team.results.html")
    else:
        raise Exception(
            f"Unexpectedly no merged results for team results in event {event}"
        )


logging.info("Finished")
