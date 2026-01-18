# Results

## Submission of results

- Team managers/club captains, please see the [league website for details on submitting results](https://westleague.org.uk/results/submission/)
  - Note that this is event/weather/volunteer dependent. Please follow social media/news for cancellation notes.

## Provisional results

### 2025-26


* [Event #1, Strathaven](https://results.westleague.org.uk/results/provisional/2025-26/1/html/)
  * [PROVISIONAL Race results](https://results.westleague.org.uk/results/provisional/2025-26/1/html/)
  * Still [awaiting 15 team results](./results/provisional/2025-26/1/missingTeamSubmissions.csv)
  * Hosted by [East Kilbride AC](http://www.ekac.org.uk/)
  * [Attendance: 409](./results/provisional/2025-26/1/meta.json)
  * [Thanks to the volunteers](./results/provisional/2025-26/1/html/volunteers.html)
    * [Attendance](./results/provisional/2025-26/1/meta.json)
  * Data variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2025-26/1), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2025-26/1/markdown/)


### Processing notes

- Results typically processed on the **SUNDAY** following the event
- Until all team submissions received, **team positions/points will change**
- Please direct queries/issues to contact@westleague.org.uk

## Previous seasons

- [See previous seasons results here](./PREVIOUS_SEASONS.md)

# Results explainer

- Filenames are of the form `RACE`.`AGECAT`.`GENDER`.`TYPE`.results.`FILETYPE`
- Where:
  - `RACE` is the race name 'on the day', eg. `U11_Boys`, `U11_Girls`, ..., `U17_Combined`, `U20-Senior-Masters_Combined`
  - `AGECAT` is the age category taking part in a race, eg. `U11`, ... `U20`, `SENIOR`, `MASTER`
    - Note that `OVERALL` is a combined for all participants in the Senior race
  - `GENDER` is the gender competition the league currently runs: `male` and `female`
    - Non-binary participants are _currently_ included in the `male` competition results
    - Participants gender is displayed on an individual race result (`M`, `F`, `A`)
  - `TYPE` is the type of results
    - One of `agecat`, `team`, `event` (see below)
  - `FILETYPE` is the file type, eg. `md`, `csv`,`pdf`, `html`
- Result files:
  - `missingTeamSubmissions`: are a report of any clubs missing any names for a race they took part in.
  - `volunteers`: lists the volunteers who made the event happen on the day
  - `agecat.results`: the results for the participants in that age category (mostly relevant for Seniors combined event)
  - `team.results`: the team results and points calculation for that race. See [the league website](https://westleague.org.uk/what-do-i-need-to-know/results-and-points-system/) for more detail.
- Team standings:
  - For each age category + gender, across all events in the League, show the relative placing of each team.
  - This determines the eventual winners of the league.
  - See [the league website](https://westleague.org.uk/what-do-i-need-to-know/results-and-points-system/) for more detail.

## Results processing, technical notes

### Introduction

This is a repository for tooling, and public data, for the [West District XC League](https://westleague.org.uk/).

### Running the results process

See [tools/README.md](./tools/README.md) for the steps to process results.

## Reference data

- [West District clubs (CSV)](./data/reference/clubs.csv)

## See also

- [West District League website](https://westleague.org.uk/)
