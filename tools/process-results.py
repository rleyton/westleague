#!env python
import logging
import datetime
from src.adapter_sheets import load_volunteers, load_results
from src.utils_consts import (
    EXT_TIMES,
    EXT_PLACES,
    EXT_META,
    EXT_ADJUSTMENTS,
    EXT_CSV,
    GENDER_COMPETITION_MAP,
    HTML_DIR,
    MARKDOWN_DIR,
    PDF_DIR,
)
from src.adapter_pdf import generate_pdf, combined_pdf, generate_single_pdf
from src.utils_functions import fetch_events_from_dir, fetch_volunteers_from_dir
from src.adapter_gender import gender_process
from src.adapter_team import process_teams, load_team_submissions
from src.adapter_results import (
    results_merge,
    tidy_results,
    merge_runners,
    get_missing_teams,
)
from src.adapter_times import adjust_times
from src.adapter_places import adjust_places, process_final_results
from src.adapter_points import calculate_competition_points
from src.adapter_json import json_write
from src.adapter_format import export_results, get_html
from src.adapter_clubs import load_clubs
import pandas as pd
import pathlib
from src.utils_config import (
    DATA_DIR,
    ADJUSTMENTS_DIR,
    TEAMS,
    GENDERS,
    RESULTS_DIR,
    year as event_year,
    event as event_number,
)

logging.basicConfig(level=logging.DEBUG)

# hard-coded to same location for now
SOURCE_DATA = DATA_DIR

pathlib.Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(RESULTS_DIR + MARKDOWN_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(RESULTS_DIR + HTML_DIR).mkdir(parents=True, exist_ok=True)
pathlib.Path(RESULTS_DIR + PDF_DIR).mkdir(parents=True, exist_ok=True)


teams = load_clubs()
genders = pd.read_csv(GENDERS, index_col="shortcode")

results = {}
resultsHTML = {}
leagueResults = {}
teamResults = {}
ageCatResults = {}
missingTeams = set()
eventMeta = {}
index = []
eventTotalParticipants = 0
totalGenderParticipants = {}
pdfs = []

logging.info(f"Processing: {DATA_DIR}")

# for each event we have files for
for event in sorted(fetch_events_from_dir(DATA_DIR)):
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
                    results_merge(times=record["times"], places=record["places"]),
                    clubSubmissions=clubSubmissions,
                    event=event,
                )
            ),
            adjustments=record["adjustments"],
        )
    except Exception as e:
        raise Exception(f"Problem processing event {event}: {e}")

    eventMissingTeams = set(
        get_missing_teams(results=results[event], submissions=clubSubmissions)
    )
    if len(eventMissingTeams) > 0:
        logging.warning(f"Event submissions for {event}: {eventMissingTeams}")
        missingTeams = missingTeams.union(eventMissingTeams)

    # Now we have a results DataFrame, so process the competition results
    (racemeta, teamResults[event], ageCatResults[event]) = calculate_competition_points(
        results=results[event], teams=teams, event=event
    )

    # Produce the CSV outputs

    # core results
    if results[event] is not None:
        resultsPages = export_results(
            results=results[event], base_file_name=event, suffix=".event.results"
        )
        index.append(
            {
                "event": event,
                "competition": "n/a",
                "gender": "all",
                "results": get_html(resultsPages),
            }
        )
    else:
        raise Exception(f"Unexpectedly no merged results for event {event}")

    eventTotalParticipants += racemeta["totals"]["participants"]

    # ageCategory specific results
    if ageCatResults[event] is not None:
        for gender in ageCatResults[event]:
            resultsHTML[gender] = {}
            for competition in ageCatResults[event][gender]:
                # only write files if any data
                if len(ageCatResults[event][gender][competition]) > 0:
                    baseFileName = (
                        event + "." + competition + "." + GENDER_COMPETITION_MAP[gender]
                    )
                    ageCatResultsPage = export_results(
                        results=ageCatResults[event][gender][competition],
                        base_file_name=baseFileName,
                        suffix=".agecat.results",
                    )
                    resultsHTML[gender][competition] = (
                        RESULTS_DIR + "/html/" + get_html(ageCatResultsPage)
                    )

                    index.append(
                        {
                            "event": event,
                            "competition": competition,
                            "gender": gender,
                            "results": get_html(ageCatResultsPage),
                        }
                    )
                    logging.info("Wrote: " + get_html(ageCatResultsPage))

    # team results
    if teamResults[event] is not None:
        for gender in teamResults[event]:
            if gender not in totalGenderParticipants:
                totalGenderParticipants[gender] = 0

            for competition in teamResults[event][gender]:
                if competition not in eventMeta:
                    eventMeta[competition] = {}

                eventMeta[competition][gender] = racemeta[competition][gender]

                if competition != "OVERALL":
                    totalGenderParticipants[gender] += racemeta[competition][gender][
                        "participants"
                    ]

                baseFileName = (
                    event + "." + competition + "." + GENDER_COMPETITION_MAP[gender]
                )

                resultPages = export_results(
                    results=teamResults[event][gender][competition],
                    base_file_name=baseFileName,
                    suffix=".team.results",
                )

                pdfs.append(
                    generate_pdf(
                        competition=competition,
                        gender=gender,
                        resultshtml=resultsHTML[gender][competition],
                        teamhtml=RESULTS_DIR + "/html/" + get_html(resultPages),
                        prefix=f"{event_year}, Event #{event_number} ",
                    )
                )

                index.append(
                    {
                        "event": event,
                        "competition": competition,
                        "gender": gender,
                        "results": get_html(resultPages),
                    }
                )
                logging.info("Wrote: " + get_html(resultPages))
    else:
        raise Exception(
            f"Unexpectedly no merged results for team results in event {event}"
        )

logging.info(f"Finished processing: {DATA_DIR}")

# TODO: This all needs refactoring/tidying up
json_write(
    object={
        "races": eventMeta,
        "attendance": {
            "total": eventTotalParticipants,
            "gender": totalGenderParticipants,
        },
    },
    filename=RESULTS_DIR + "/" + "meta.json",
)

missing = pd.DataFrame({"team": list(missingTeams)})


theMissingTeams = missing.join(
    other=teams, on="team", lsuffix="missing", rsuffix="teamDetails"
)

missing_teams = export_results(
    results=theMissingTeams, base_file_name="", suffix="missingTeamSubmissions"
)

index.append(
    {
        "event": "n/a",
        "competition": "n/a",
        "gender": "n/a",
        "results": get_html(missing_teams),
    }
)

volunteersFile = fetch_volunteers_from_dir(dir=DATA_DIR)
if volunteersFile:
    volunteers = pd.read_csv(volunteersFile)

    volunteers.columns = ["Name", "Role"]

    vols = export_results(results=volunteers, base_file_name="", suffix="volunteers")

    index.append(
        {
            "event": "n/a",
            "competition": "n/a",
            "gender": "n/a",
            "results": get_html(vols),
        }
    )
    pdfs.append(
        generate_single_pdf(
            html=RESULTS_DIR + HTML_DIR + "/" + get_html(vols),
            filename="volunteers",
            summary="Volunteers",
        )
    )

pdfs.insert(
    0,
    generate_single_pdf(
        html=RESULTS_DIR + HTML_DIR + "/" + get_html(missing_teams),
        filename="missingTeams",
        summary="Team submissions still pending",
    ),
)

# Render a basic HTML index


def make_clickable(val):
    return f'<a target="_blank" href="{val}">{val}</a>'


indexDF = pd.DataFrame(index)
indexDF = indexDF.style.format({"results": make_clickable})

indexDF.hide(axis="index").to_html(
    RESULTS_DIR + HTML_DIR + "/" + "index.html",
    index=False,
    render_links=True,
    escape=False,
)

datestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


summary = f"""
<h1>Summary</h1>
<p>Combined results PDF. Please see <a href="https://westleague.org.uk">westleague.org.uk</a></p>
<p>Latest results/status at <a href="https://results.westleague.org.uk">results.westleague.org.uk</a></p>
<p>Note results are provisional until all team results received.</p>
<h1>Results</h1>
<p>Results for all races at Event #{event_number} for season {event_year}.</p>
<p>The are presented in the following order:<p>
<ul>
<li>Still pending team submissions</li>
<li>U11: Male, Male Teams, Female, Female Teams</li>
<li>U13: Male, Male Teams, Female, Female Teams</li>
<li>U15: Male, Male Teams, Female, Female Teams</li>
<li>U17: Male, Male Teams, Female, Female Teams</li>
<li>U20: Male, Male Teams, Female, Female Teams</li>
<li>Senior: Male, Male Teams, Female, Female Teams</li>
<li>Master: Male, Male Teams, Female, Female Teams</li>
<li>Overall: Male, Male Teams, Female, Female Teams</li>
<li>Volunteers
</ul>
<p>
<h1>Last updated</h1>
<p>This file was last updated at: {datestamp}</p>
"""
combined_pdf(
    pdf_list=pdfs, target=RESULTS_DIR + PDF_DIR + "/RESULTS.pdf", summary=summary
)


logging.info("Finished")
