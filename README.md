# Results 


# 2022-23

* [Event #1, Strathaven](https://results.westleague.org.uk/results/provisional/2022-23/1/html/)
  * Variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/1), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/1/markdown/)
* [Event #2, Kilmarnock](https://results.westleague.org.uk/results/provisional/2022-23/2/html/)
  * Variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/2), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/2)
* Event #3, Bellahouston park (not yet available)
  * Not yet available
* [Team standings, by competition](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html)
  * Variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/teamStandings/), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2022-23/teamStandings/markdown/)
  * U11
    * [Male](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U11_M.team.standings.html)
    * [Female](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U11_F.team.standings.html)
  * U13
    * [Male](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U13_M.team.standings.html)
    * [Female](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U13_F.team.standings.html)
  * U15
    * [Male](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U15_M.team.standings.html)
    * [Female](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U15_F.team.standings.html)
  * U17
    * [Male](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U17_M.team.standings.html)
    * [Female](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U17_F.team.standings.html)
  * U20
    * [Male](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U20_M.team.standings.html)
    * [Female](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/U20_F.team.standings.html)
  * Senior
    * [Male](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/SENIOR_M.team.standings.html)
    * [Female](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/SENIOR_F.team.standings.html)
  * Master
    * [Male](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/MASTER_M.team.standings.html)
    * [Female](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/MASTER_F.team.standings.html)
* [Team position summary](https://results.westleague.org.uk/results/provisional/2022-23/teamStandings/html/club_position_summary.html)
  * What position a club holds in each of the various competitions
* Website coverage
  * [5th February, after two events](https://westleague.org.uk/2023/02/05/results-standings-with-one-week-to-go-to-bellahouston/)

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

