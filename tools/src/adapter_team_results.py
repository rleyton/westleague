import pandas as pd
import numpy as np
from .utils_functions import fetch_results_filenames
import logging


def load_team_results(dir: str = None):
    teamResults = fetch_results_filenames(dir)
    eventResults = {}
    for race in teamResults:
        logging.info(f"Loading {race['filename']}")
        teamResult = pd.read_csv(race["filename"])
        if race["agecat"] not in eventResults:
            eventResults[race["agecat"]] = {}
        eventResults[race["agecat"]][race["gender"]] = teamResult

    return eventResults


def extract_race_results(
    allEvents: dict = None, requiredCompetition: str = None, requiredGender: str = None
):
    """Fetch ALL of the relevant races from the structure, return as list"""
    results = {}
    for event in allEvents:
        results[event] = allEvents[event][requiredCompetition][requiredGender]
    return results


def calculate_team_standings(
    raceResults: dict = None,
    eventMeta: dict = None,
    competition: str = None,
    gender: str = None,
):
    """For the results we have, roll up the results"""
    table = {}
    for race in raceResults:
        for index, teamResult in raceResults[race].iterrows():
            team = teamResult["team"]
            teamPoints = int(teamResult["totalPoints"])
            clubName = teamResult["Club name"]
            if race not in table:
                table[race] = {}

            table[race][team] = teamPoints

    results = pd.DataFrame(table)

    results["Total"] = 0
    clubParticipantsColumns = ["club", "participations"]
    clubParticipants = None
    for race in raceResults:
        raceMeta = eventMeta[race]["races"][competition][gender]

        participantMeta = pd.DataFrame(
            raceMeta["clubparticipation"].items(), columns=clubParticipantsColumns
        )
        # cast to int
        participantMeta["club"] = participantMeta["club"].astype(np.integer)
        participantMeta.set_index("club")

        if clubParticipants is None:
            clubParticipants = participantMeta
        else:
            clubParticipants = pd.concat([clubParticipants, participantMeta], axis=0)

        noParticipantsPenalty = raceMeta["penalty"] * raceMeta["counters"]
        results.iloc[:, race - 1] = (
            results.iloc[:, race - 1].replace(np.nan, noParticipantsPenalty).astype(int)
        )
        results["Total"] = results["Total"] + results.iloc[:, race - 1].astype(int)

    totalParticipants = clubParticipants.groupby(["club"], as_index=False).sum()
    totalParticipants["competition"], totalParticipants["gender"] = [
        competition,
        gender,
    ]
    return (results.sort_values(by=["Total"]), totalParticipants)
