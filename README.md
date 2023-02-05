# Results 


# 2022-23

* [Event #1, Strathaven](https://results.westleague.org.uk/results/provisional/2022-23/1/html/)
  * Variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/1), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/1/markdown/)
* [Event #2, Kilmarnock](https://results.westleague.org.uk/results/provisional/2022-23/2/html/)
  * Variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/2), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/2)
* Event #3, Bellahouston park (not yet available)
  * Not yet available
* [Overall team standings](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html)
  * Variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/teamStandings/), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/teamStandings/markdown/)
* [Team position summary](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/club_position_summary.html)
  * What position a club holds in each of the various competitions

# Results explainer
  * Results are still a bit 'raw', but filenames should hopefully make sense. 
    * We hope to have a 'nice' summary generated soon
  * Filenames generally consist of RACE.AGECAT
    * Note that RACE is the race itself
      * eg. `U11_Boys`, `U11_Girls`, ..., `U17_Combined`, `U20-Senior-Masters_Combined`
    * Age categories taking part in a race are broken out separately, eg. `U20`, `SENIOR`, `MASTER`
      * `OVERALL` is all participants in the Senior race
  * Result files:
    * `missingTeamSubmissions`: are a report of any clubs missing any names for a race they took part in.
    * `volunteers`: lists the volunteers who made the event happen on the day
    * `agecat.results`: the results for the participants in that age category (mostly relevant for Seniors combined event)
    * `team.results`: the team results and points calculation for that race. See [the league website](https://westleague.org.uk/what-do-i-need-to-know/results-and-points-system/) for more detail.
  * Team standings:
    * For each age category + gender, across all events in the League, show the relative placing of each team.
    * This determines the eventual winners of the league.
    * See [the league website](https://westleague.org.uk/what-do-i-need-to-know/results-and-points-system/) for more detail.


# Results processing, technical notes 

## Introduction

This is a repository for tooling, and public data, for the [West District XC League](https://westleague.org.uk/).

## Running the results process

See [tools/README.md](./tools/README.md) for the steps to process results.

# Reference data

* [West District clubs (CSV)](./data/reference/clubs.csv)

# See also

* [West District League website](https://westleague.org.uk/)

