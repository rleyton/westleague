# Results 

## Submission of results

* Team managers/club captains, please see the [league website for details on submitting results](https://westleague.org.uk/results/submission/)

## Provisional results

_Provisional results reflect team submissions received by **19th November, 3:15pm**_ - Please direct queries/issues to contact@westleague.org.uk

* [Event #1, Kilmarnock (18th November, 2023)](https://results.westleague.org.uk/results/provisional/2023-24/1/html/)
  * [Provisional Race results](https://results.westleague.org.uk/results/provisional/2023-24/1/html/) - See below for known issues
  * **9 Teams still need to submit results** - [List of teams here](https://github.com/rleyton/westleague/blob/main/results/provisional/2023-24/1/markdown/missingTeamSubmissions.md), [please submit via website here](https://westleague.org.uk/results/submission/)
  * Hosted by [Kilmarnock H&AC](http://www.kilmarnockharriers.com/)
  * [Attendance: 441](./results/provisional/2023-24/1/meta.json)
  * [Thanks to the 20 volunteers](./results/provisional/2023-24/1/html/volunteers.html)
  * Data variations: [CSV](https://github.com/rleyton/westleague/tree/main/results/provisional/2023-24/1), [markdown](https://github.com/rleyton/westleague/tree/main/results/provisional/2023-24/1/markdown/)


### Known results issues

* [9 teams still to submit results, list here](https://github.com/rleyton/westleague/blob/main/results/provisional/2023-24/1/markdown/missingTeamSubmissions.md)
* Known time/results mismatch in the following events:
  * U11 Boys 
  * U15 Combined
* Please direct queries/issues to contact@westleague.org.uk


## Future events

* Event #2, Bellahouston (20th January, 2024)
  * Please check back after the event
* Event #3, Erskine (10th February, 2024)
  * Please check back after the eventp


## 2022-23

* [Results summary/links for the 2022-23 season can be found here](./README.2022-23.md)

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


## Results processing, technical notes 

### Introduction

This is a repository for tooling, and public data, for the [West District XC League](https://westleague.org.uk/).

### Running the results process

See [tools/README.md](./tools/README.md) for the steps to process results.

## Reference data

* [West District clubs (CSV)](./data/reference/clubs.csv)

## See also

* [West District League website](https://westleague.org.uk/)

