# Testing Guide

This document describes how to run and write tests for the West District XC League results processing project.

## Quick Start

### Install Test Dependencies

```bash
pipenv install --dev
```

### Run All Tests

```bash
pipenv run pytest
```

### Run Tests with Coverage

```bash
pipenv run pytest --cov=tools/src --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures and test configuration
├── unit/                    # Unit tests for individual modules
│   ├── test_utils_functions.py
│   ├── test_adapter_clubs.py
│   └── test_adapter_gender.py
├── integration/             # Integration tests (future)
└── fixtures/                # Test data files
```

## Running Tests

### Command Line

```bash
# Run all tests
pipenv run pytest

# Run with verbose output
pipenv run pytest -v

# Run specific test file
pipenv run pytest tests/unit/test_utils_functions.py

# Run specific test class
pipenv run pytest tests/unit/test_utils_functions.py::TestFetchEventsFromDir

# Run specific test function
pipenv run pytest tests/unit/test_utils_functions.py::TestFetchEventsFromDir::test_returns_none_when_dir_is_none

# Run tests matching a pattern
pipenv run pytest -k "gender"

# Run with coverage report
pipenv run pytest --cov=tools/src --cov-report=term-missing
```

### VS Code Debugging

The project includes several VS Code debug configurations for running tests:

1. **pytest: Run All Tests** - Run the entire test suite
2. **pytest: Run All Tests with Coverage** - Run tests and generate coverage report
3. **pytest: Run Current Test File** - Debug the currently open test file
4. **pytest: Debug Current Test** - Debug a specific test (select test name first)
5. **pytest: Run Unit Tests Only** - Run only unit tests

To use:
1. Open the Run and Debug panel (Cmd+Shift+D / Ctrl+Shift+D)
2. Select the desired configuration from the dropdown
3. Press F5 or click the green play button

## Writing Tests

### Test Structure

Tests are organized using pytest classes and follow this pattern:

```python
import pytest
from tools.src.module_name import function_to_test

class TestFunctionName:
    """Tests for function_to_test"""

    def test_basic_functionality(self):
        """Should do something when given valid input"""
        result = function_to_test(valid_input)
        assert result == expected_output

    def test_edge_case(self):
        """Should handle edge case correctly"""
        result = function_to_test(edge_case_input)
        assert result is not None
```

### Using Fixtures

Common test fixtures are defined in `tests/conftest.py`:

```python
def test_with_sample_data(sample_clubs_df):
    """Test using predefined sample clubs dataframe"""
    assert len(sample_clubs_df) == 3
    # Your test code here

def test_with_temp_directory(tmp_path):
    """Test using temporary directory (pytest built-in fixture)"""
    test_file = tmp_path / "test.csv"
    test_file.write_text("data")
    # Your test code here
```

Available fixtures:
- `sample_clubs_csv` - Temporary CSV file with sample clubs data
- `sample_clubs_df` - Pandas DataFrame with sample clubs
- `sample_results_df` - Sample results DataFrame
- `temp_data_dir` - Temporary data directory structure
- `temp_results_dir` - Temporary results directory
- `sample_meta_csv` - Sample event meta files
- `tmp_path` - Pytest built-in temporary directory

### Mocking

Use `pytest-mock` or `unittest.mock` for mocking:

```python
from unittest.mock import patch

def test_with_mock():
    with patch('tools.src.adapter_clubs.pd.read_csv') as mock_read:
        mock_read.return_value = sample_dataframe
        result = load_clubs()
        mock_read.assert_called_once()
```

## Coverage

### Current Coverage

The project currently has:
- **86.13% overall coverage** (565 of 656 statements)
- **231 passing tests** across 13 test modules
- 100% coverage on 12 core modules
- 90%+ coverage on 5 additional modules

### Coverage Breakdown by Module

**Perfect Coverage (100%):**
- adapter_clubs.py
- adapter_format.py
- adapter_gender.py
- adapter_json.py
- adapter_pretty_html.py
- adapter_team.py
- utils_config.py
- utils_consts.py
- utils_functions.py

**Excellent Coverage (90-99%):**
- adapter_points.py - 99.15%
- adapter_excel.py - 96.55%
- adapter_places.py - 96.00%
- adapter_sheets.py - 95.89%
- adapter_times.py - 95.00%

**Good Coverage (70-89%):**
- adapter_results.py - 77.06%
- adapter_team_results.py - 70.00%

### Viewing Coverage Reports

After running tests with coverage:

```bash
# Terminal report (shows missing lines)
pipenv run pytest --cov=tools/src --cov-report=term-missing

# HTML report (interactive)
pipenv run pytest --cov=tools/src --cov-report=html
open htmlcov/index.html

# XML report (for CI systems)
pipenv run pytest --cov=tools/src --cov-report=xml
```

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Every push to `main` branch
- Every pull request to `main` branch

The CI pipeline:
1. Runs tests on Python 3.9, 3.10, and 3.11
2. Generates coverage reports
3. Uploads coverage to Codecov
4. Fails if tests fail or coverage drops below threshold (9%)

View test results in the "Actions" tab on GitHub.

## Test Markers

Tests can be marked with custom markers:

```python
@pytest.mark.unit
def test_something():
    pass

@pytest.mark.slow
def test_long_running():
    pass

@pytest.mark.requires_api
def test_with_external_api():
    pass
```

Run specific markers:
```bash
pipenv run pytest -m unit
pipenv run pytest -m "not slow"
```

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. You're running tests via `pipenv run pytest` (not just `pytest`)
2. All dependencies are installed: `pipenv install --dev`
3. You're in the project root directory

### Pandas/NumPy Version Conflicts

If you see numpy dtype size errors:
```bash
pipenv run pip install --force-reinstall --no-cache-dir pandas
```

## Best Practices

1. **Write tests first** - Consider TDD for new features
2. **Test behavior, not implementation** - Focus on what the function does, not how
3. **Use descriptive test names** - `test_returns_none_when_dir_is_none` not `test_1`
4. **One assertion per test** - Makes failures easier to debug
5. **Use fixtures** - Share common setup code
6. **Mock external dependencies** - Don't make real API calls or read real files (except in integration tests)
7. **Keep tests fast** - Unit tests should run in milliseconds

## Next Steps

To expand test coverage, consider adding tests for:

1. **Phase 1 - High Priority**
   - `adapter_times.py` - Time parsing and formatting
   - `adapter_places.py` - Place calculations
   - `adapter_points.py` - Points calculation

2. **Phase 2 - Medium Priority**
   - `adapter_results.py` - Results processing
   - `adapter_team_results.py` - Team results aggregation
   - `adapter_format.py` - Output formatting

3. **Phase 3 - Integration Tests**
   - End-to-end result processing workflows
   - Multi-event team standings calculation
   - PDF/HTML generation

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [pytest-mock documentation](https://pytest-mock.readthedocs.io/)
