# Tools

* [club-submissions-to-csv.py](club-submissions-to-csv.py) - Converts submitted spreadsheets (Excel) into CSV, which are written to [../data/2022-23/1/club-parsed](../data/.../club-parsed). 
* [sheets-to-csv.py](sheets-to-csv.py) - Pulls tabulated timer and finish position data into a CSV. Requires Google API credentials. Writes out to [../data/2022-23/1/](../data/.../event)
* [process-results.py](process-results.py) - Uses CSVs produced by previous steps to calculate results, with reference to adjustments stored in [../data/adjustments/2022-23/1](../data/adjustments/...)

# Notes 

* Requires python3.9
* Run: `pipenv shell`
* Run: `tools/process-results.py`

# Outline intent

* See [top-level README](../README.md) for overall approach
* U

# Coding apologies/TODO

* Currently hard-coded to event 2022-23/1
* Started with a loose hexagonal architecture intent, but it fell apart in order to get things turned around. 
* There's a few overlapping constants and variables
* The pandas logic is generally creating copies of Dataframes for clarity. This could be improved


# Still to do

* Proper counter rule (ie. first N finishers in senior/masters, rather than exclusive-to-specific-age-group)
* Handle multiple-events, ie. the league itself
  * ie. pull in previous event results, build the running tally
  * multi-year?
* Support time manipulation etc.
* Graphs! Statistic! Prettyness
 * @bazzargh suggested looking at [https://datasette.io/](Datasette), which does seem quite tasty

