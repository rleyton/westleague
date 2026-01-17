# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains tooling for processing results for the [West District XC League](https://westleague.org.uk/). The system processes cross-country race results from multiple events per season, handling timing data, finish positions, team submissions, and generating league standings across different age categories and genders.

## Essential Commands

### Setup
```bash
# Install dependencies (Python 3.9 required)
pipenv install --dev
pipenv shell
```

### Testing
```bash
# Run all tests with coverage
pipenv run pytest

# Run specific test markers
pipenv run pytest -m unit
pipenv run pytest -m integration

# Run tests for a specific file
pipenv run pytest tests/unit/test_adapter_clubs.py

# Run a single test
pipenv run pytest tests/unit/test_adapter_clubs.py::test_function_name

# Coverage requirement: 62% minimum (configured in pytest.ini)
```

### Results Processing
```bash
# Process all events for a season
make results

# Process a single event manually
export PROCESS_EVENT=1
pipenv run python ./tools/sheets-to-csv.py
pipenv run python ./tools/club-submissions-to-csv.py
pipenv run python ./tools/process-results.py

# Generate league tables after processing events
pipenv run python ./tools/team-results.py
```

## Architecture

### Data Flow Pipeline

The results processing follows a sequential pipeline:

1. **Data Ingestion**: `sheets-to-csv.py` pulls timing and finish position data from Google Sheets into CSV files
2. **Club Submissions**: `club-submissions-to-csv.py` converts Excel spreadsheets submitted by clubs into normalized CSV format
3. **Results Processing**: `process-results.py` merges timing data with finish positions, applies adjustments, and calculates competition points
4. **League Aggregation**: `team-results.py` aggregates event results across the season to produce league standings

### Adapter Pattern

The codebase uses an adapter-based architecture where each `adapter_*.py` module handles a specific concern:

- **adapter_sheets.py**: Google Sheets API integration
- **adapter_excel.py**: Excel file parsing for club submissions
- **adapter_gender.py**: Gender classification and competition assignment
- **adapter_team.py**: Team/club data management
- **adapter_times.py**: Time adjustment and validation
- **adapter_places.py**: Finish position adjustment and processing
- **adapter_results.py**: Core results merging and runner data management
- **adapter_points.py**: Competition points calculation
- **adapter_format.py**: Multi-format output generation (CSV, Markdown, HTML)
- **adapter_pdf.py**: PDF generation and combination
- **adapter_team_results.py**: League table generation
- **adapter_json.py**: JSON output for metadata

### Configuration System

Configuration is managed through:
- `.env` file: Defines `PROCESS_YEAR`, `PROCESS_EVENT`, and Google Sheets URL
- `utils_config.py`: Reads `.env` and constructs data directory paths
- `utils_consts.py`: Constants for competition structure, scoring rules, file naming conventions

### Data Structure

```
data/
  {YEAR}/
    {EVENT}/
      {RACE}.times.csv        # Timing data
      {RACE}.places.csv       # Finish positions
      {RACE}.meta.csv         # Event metadata
      club-parsed/            # Parsed club submissions
        {CLUB_ID}.{RACE}.csv
  adjustments/
    {YEAR}/{EVENT}/
      {RACE}.adjustments.csv  # Manual corrections
  reference/
    clubs.csv                 # Club registry
    genders.csv               # Gender mapping

results/
  provisional/{YEAR}/{EVENT}/
    html/                     # HTML results
    markdown/                 # Markdown results
    pdf/                      # PDF results
    meta.json                 # Event statistics
  provisional/{YEAR}/teamStandings/
                              # Season league tables
```

### Race Types and Competition Structure

- **Age-specific races**: U11, U13 (separate by gender)
- **Combined races**: U15, U17, U20-Senior-Masters (mixed gender, separated in results)
- **Gender competitions**: Male (M) and Female (F) - non-binary participants compete in male category
- **Age categories**: U11, U13, U15, U17, U20, SENIOR, MASTER, OVERALL

Scoring uses top N counters per team (typically 3, but 4 for SENIOR/OVERALL) with lowest total winning. Missing runners incur 10-point penalty per missing counter.

### Key Processing Concepts

**Adjustments**: Manual corrections stored in `data/adjustments/{year}/{event}/` to fix timing errors, gender misclassifications, or position corrections. Applied via `adjust_times()` and `adjust_places()`.

**Club Submissions**: Clubs submit Excel spreadsheets with their runners in finish order. These are parsed to match timing data with runner identities.

**Results Merging**: The core process joins timing data (times.csv) with finish positions (places.csv) and club submissions to produce complete results with runner names, clubs, times, and positions.

**Points Calculation**: Team points are calculated by summing positions of top N counters. Lower total wins. Managed in `adapter_points.py`.

## Important Notes

- Python 3.9 is required
- Google Sheets API credentials needed for `sheets-to-csv.py`
- The `.env` file must be configured with `PROCESS_YEAR` and `PROCESS_EVENT` before running processing scripts
- Results are provisional until all club submissions are received
- Test coverage must maintain 62% minimum threshold
- The codebase acknowledges it started with hexagonal architecture intent but evolved pragmatically for delivery speed
