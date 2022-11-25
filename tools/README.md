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

# Coding apologies/TODO

* This is an early first draft; it needs some reflection and tidying. 
* Currently hard-coded to event 2022-23/1
* Started with a loose hexagonal architecture intent, but it fell apart in order to get things turned around. 
* There's a few overlapping constants and variables
* The pandas logic is generally creating copies of Dataframes for clarity. This could be improved.


# Still to do

* Proper counter rule (ie. first N finishers in senior/masters, rather than exclusive-to-specific-age-group)
* Handle multiple-events, ie. the league itself
  * ie. pull in previous event results, build the running tally
  * multi-year?
* Support time manipulation etc.
* Graphs! Statistic! Prettyness
 * [@bazzargh](https://github.com/bazzargh/) suggested looking at [https://datasette.io/](Datasette), which does seem quite tasty

# Example run

```
(westleague) ➜  westleague git:(main) tools/process-results.py 
DEBUG:root:Processing: U13_Boys
DEBUG:root:No adjustments for U13_Boys
DEBUG:root:Processing: U11_Boys
INFO:root:Added new time record at 7
DEBUG:root:Processing: U15_Combined
DEBUG:root:No adjustments for U15_Combined
DEBUG:root:Processing: U13_Girls
DEBUG:root:Adjustment of remove ignored
DEBUG:root:Processing: U11_Girls
INFO:root:Added new time record at 20
INFO:root:Added new time record at 20
INFO:root:Added new time record at 32
INFO:root:Added new time record at 38
DEBUG:root:Processing: U17_Combined
INFO:root:Changing recorded club for place 12 from 47M to 57M
DEBUG:root:Adjustment of 57 ignored
ERROR:root:Insufficient names for club 36 in event U17_Combined
DEBUG:root:Processing: U20-Senior-Masters_Combined
INFO:root:Changing recorded club for place 101 from 22M to 2M
DEBUG:root:Adjustment of 2 ignored
INFO:root:Remove finishing position 120
INFO:root:Finished
```