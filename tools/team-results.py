#!env python

from dotenv import dotenv_values
import logging
from src.adapter_sheets import load_volunteers, load_results
from src.adapter_json import json_load
from src.adapter_format import export_results, get_html
from src.utils_consts import (
    GENDER_COMPETITION_MAP,
    HTML_DIR,
)
from src.utils_config import (
    TEAMS,
    GENDERS,
    BASE_RESULTS,
    YEAR_RESULTS,
    RESULTS_DIR,
    YEAR_RESULTS_OUTPUT,
)
from src.utils_functions import fetch_events
from src.adapter_team_results import (
    load_team_results,
    extract_race_results,
    calculate_team_standings,
)
from src.adapter_clubs import load_clubs
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.DEBUG)

# hard-coded to same location for now
teams = load_clubs()
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
the_team_standings = {}
clubParticipantsColumns = ["club", "participants"]
totalClubParticipation = None
for competition in dict(sorted(events[baseEvent].items())):

    if competition not in the_team_standings:
        the_team_standings[competition] = {}

    for gender in GENDER_COMPETITION_MAP:
        logging.info(f"Processing {competition}:{GENDER_COMPETITION_MAP[gender]}")
        raceResults = extract_race_results(
            allEvents=events,
            requiredCompetition=competition,
            requiredGender=GENDER_COMPETITION_MAP[gender],
        )

        (teamStandings, clubParticipation) = calculate_team_standings(
            raceResults=raceResults,
            eventMeta=event_meta,
            competition=competition,
            gender=gender,
        )

        if competition not in ["OVERALL"]:
            if totalClubParticipation is None:
                totalClubParticipation = clubParticipation
            else:
                totalClubParticipation = pd.concat(
                    [totalClubParticipation, clubParticipation], axis=0
                )
        else:
            logging.info(
                "Skipping OVERALL event for club participation, as combination of Senior and Masters"
            )

        normalisedTeamStandings = teamStandings.join(other=teams)

        resultPages = export_results(
            results=normalisedTeamStandings,
            results_dir=YEAR_RESULTS_OUTPUT,
            base_file_name=f"{competition}_{gender}",
            suffix=".team.standings",
        )

        theFiles.append(
            {
                "competition": competition,
                "gender": gender,
                "results": get_html(resultPages),
            }
        )

        # convenience reference for lookup, add a position column
        normalisedTeamStandings["position"] = np.arange(len(normalisedTeamStandings))
        the_team_standings[competition][gender] = normalisedTeamStandings


def lookup_team_position(
    standings=None, club_number=None, competition=None, gender=None
):
    if competition in standings:
        if gender in standings[competition]:
            # the event isn't indexed, so fetch it, with a new index
            standings = standings[competition][gender]
            try:
                club_position = int(
                    standings.loc[[club_number]]["position"].astype(int) + 1
                )
            except KeyError as e:
                club_position = None

            return club_position


club_table = {}
for club_number, row in teams.iterrows():
    club_name = row["Club name"]
    club_results = {}
    for competition in dict(sorted(events[baseEvent].items())):
        for gender in GENDER_COMPETITION_MAP:
            key = f"{competition}:{gender}"

            position = lookup_team_position(
                standings=the_team_standings,
                competition=competition,
                gender=gender,
                club_number=club_number,
            )
            if position is not None:
                club_results[key] = int(position)
                logging.info(
                    f"{club_name} holds position {position} in {competition}:{gender}"
                )

    if len(club_results) > 0:
        club_table[club_number] = club_results

display_order = [
    "Club name",
    "U11:M",
    "U11:F",
    "U13:M",
    "U13:F",
    "U15:M",
    "U15:F",
    "U17:M",
    "U17:F",
    "U20:M",
    "U20:F",
    "SENIOR:M",
    "SENIOR:F",
    "MASTER:M",
    "MASTER:F",
    "OVERALL:M",
    "OVERALL:F",
]
club_table_DF = (
    (
        pd.DataFrame.from_dict(club_table, orient="index")
        .join(other=teams)[display_order]
        .replace(np.nan, "n/a")
    )
    .sort_index()
    .style.format(precision=0)
)
pd.set_option("styler.format.precision", 0)
club_table_DF.to_html(
    f"{YEAR_RESULTS_OUTPUT}/html/club_position_summary.html",
    index=True,
    index_names=False,
    render_links=True,
    escape=False,
)


# Render a basic HTML index
def make_clickable(val):
    return f'<a target="_blank" href="{val}">{val}</a>'


# summaries

breakouts = {
    "by_club": totalClubParticipation.groupby(["club"], as_index=True)
    .sum()
    .join(other=teams),
    "by_gender": totalClubParticipation.groupby(["gender"], as_index=False)
    .sum()
    .drop(columns="club"),
    "by_competition": totalClubParticipation.groupby(["competition"], as_index=False)
    .sum()
    .drop(columns="club"),
    "by_competition_gender": totalClubParticipation.groupby(
        ["competition", "gender"], as_index=False
    )
    .sum()
    .drop(columns="club"),
}
for breakout in breakouts:
    breakouts[breakout].style.format({"results": make_clickable}).to_html(
        f"{YEAR_RESULTS_OUTPUT}/html/{breakout}.html"
    )


filesDF = pd.DataFrame(theFiles)
filesDF = filesDF.style.format({"results": make_clickable})

filesDF.hide(axis="index").to_html(
    f"{YEAR_RESULTS_OUTPUT}/html/index.html",
    index=False,
    index_names=False,
    render_links=True,
    escape=False,
)


logging.info(
    f"Finished processing year: {YEAR_RESULTS} - output to {YEAR_RESULTS_OUTPUT}"
)
