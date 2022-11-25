import pandas as pd
import numpy as np
import logging
from .utils_consts import (
    SeniorAgeCats,
    PENALTY_POINTS,
    AgeCatCounterOverrides,
    DEFAULT_COUNTERS,
    CompetitionsBreakouts,
    GENDER_COMPETITIONS,
    NONBINARY,
)


def get_team_counters(ageCat):
    if ageCat in AgeCatCounterOverrides:
        return AgeCatCounterOverrides[ageCat]
    else:
        return DEFAULT_COUNTERS


def get_competition_breakout(event):
    if event in CompetitionsBreakouts:
        return CompetitionsBreakouts[event]
    else:
        return CompetitionsBreakouts["default"]


def get_competition_agecats(event):
    # from eg. U20-Senior-Masters_Combined
    # return a list of agecats in upper case
    if event is not None:
        agepart = event.upper().split("_")[0]
        if "-" in agepart:
            agecats = agepart.split("-")
        else:
            agecats = [agepart]

        # normalise filename MASTERS to MASTER to match the agecat
        if "MASTERS" in agecats:
            agecats.remove("MASTERS")
            agecats.append("MASTER")

        return agecats
    else:
        raise Exception("get_competition_agecats: event is None")


def extract_team_results(results, team):
    # we want a DataFrame back
    return results[results["clubnumber"] == team]


def extract_age_category_results(results, ageCat, gender):
    # get Age Category results
    ageCatResults = results[results["AgeCat"] == ageCat]

    # extract the matching gender records
    genderResults = ageCatResults[ageCatResults["gender"] == gender].reset_index()

    # preserve the finish position column
    genderResults["finishPosition"] = genderResults["position"]

    #
    genderResults["position"] = genderResults.index + 1
    return genderResults


def calculate_team_points(team, teamResults, maxCounters, penaltyPoints):
    # sum up the points for first N counters
    countingResults = teamResults.head(maxCounters)

    # how many results?
    teamCounters = len(countingResults)

    # what were the finisher positions
    teamFinishers = ",".join(
        teamResults.head(maxCounters)["position"].astype("string").values.tolist()
    )
    totalFinishers = len(teamResults)
    # base team points
    teamPoints = countingResults["position"].sum()

    teamPenalty = 0
    if teamCounters < maxCounters:
        # fewer than the maxCounters, so calculate penalty
        teamPenalty = (maxCounters - teamCounters) * penaltyPoints

    teamResult = {
        "team": team,
        "finisherPositions": teamFinishers,
        "teamPoints": teamPoints,
        "penaltyPoints": teamPenalty,
        "totalPoints": teamPoints + teamPenalty,
        "totalFinishers": totalFinishers,
    }
    # return a tuple of total points, counters used, and penalty part
    # return (countingResults.sum()+teamPenalty, teamCounters, teamPenalty)
    df = pd.DataFrame(teamResult, index=[team])
    return df


def calculate_competition_points(results, teams, event):
    totalRunners = len(event)

    # What competitions are in these results
    competitionBreakout = get_competition_breakout(event)

    competitionAgeCats = get_competition_agecats(event)

    competitionPoints = {}

    # for each age category in each set of results
    for ageCat in competitionAgeCats:
        competitionPoints[ageCat] = {}
        for gender in GENDER_COMPETITIONS:
            maxCounters = get_team_counters(ageCat=ageCat)

            competitionPoints[ageCat][gender] = None

            # get the results for that age category
            ageCatResults = extract_age_category_results(
                results=results, ageCat=ageCat, gender=gender
            )

            # how many took part
            totalParticipants = len(ageCatResults)

            # what the penalty points are
            penaltyPoints = totalParticipants + PENALTY_POINTS

            # Work through all the teams we know about
            for team in teams.index:
                # get their results
                teamResults = extract_team_results(ageCatResults, team)

                # work out their points, and how many constituted
                teamResult = calculate_team_points(
                    team=team,
                    teamResults=teamResults,
                    maxCounters=maxCounters,
                    penaltyPoints=penaltyPoints,
                )

                # note the gender of the final results so it appears in final
                teamResult["gender"] = gender

                if competitionPoints[ageCat][gender] is None:
                    competitionPoints[ageCat][gender] = teamResult
                else:
                    competitionPoints[ageCat][gender] = pd.concat(
                        [competitionPoints[ageCat][gender], teamResult], ignore_index=0
                    )
            #            results = times.join(other=places, lsuffix="times", rsuffix="places")

            points = tidy_points(
                competitionPoints[ageCat][gender]
                .sort_values(by="totalPoints")
                .join(other=teams, on="team")
            )

            # is there a points table
            if points is not None:
                competitionPoints[ageCat][gender] = points
            else:
                # remove the working data
                del competitionPoints[ageCat][gender]

    return competitionPoints


def get_all_possible_columns(results):
    idealCols = [
        "Club name",
        "team",
        "gender",
        "finisherPositions",
        "teamPoints",
        "penaltyPoints",
        "totalPoints",
        "totalFinishers",
        "Website",
    ]
    columns = []
    for col in idealCols:
        if col in results:
            columns.append(col)
    return columns


def tidy_points(results=None):
    if results is not None:
        # check if there are no results in the data set
        if results["totalFinishers"].sum() == 0:
            return None
        availCols = get_all_possible_columns(results)
        provisionalResults = results[availCols]
        provisionalResults.insert(
            loc=0, column="position", value=np.arange(len(results)) + 1
        )
        returnResults = provisionalResults[provisionalResults["totalFinishers"] > 0]
        return returnResults
    else:
        return None
