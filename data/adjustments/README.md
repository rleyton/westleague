# Overview

These files are the overrides/adjustments that are used by `tools/process-results.csv`

Core idea in the tooling is to try and make results processing repeatable and predictable, given a defined set of inputs. 

For results processing then they are:
* A list of clubs/teams
* A set of times, for each races. These are generally transcribed from written times, but a electronic timer could also be used.
* A set of club submissions, for each race. These are transcribed from written team+gender.
* Corrections that have been identified

And as new info comes to light, we can add corrections, and re-run to produce correct results.

# Types of adjustments

Just now these include:

## Adding times

This can happen if the timer/time recorder misses a item. During intense finish periods this does happen, and sometimes a ntoe is marked on the recording sheet to indicate this to results processor.

## Removing times

A time may be inadvertently recorded on the sheet that needs to be removed. We're trying to ensure the results as entered match the sheet preserved as the record.

## Removing finishers entirely

A DNF or disqualification can be applied retrospectively to a finisher if officals, team or individual advises of their having run a a short course, or some other issue.

## Changing recorded position

The runner's team number may be incorrectly recorded. During busy times, or just simply an accident, can come to light subsequently when looking at results.