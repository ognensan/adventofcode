# Agent Instructions

## Running Python with Pipenv

This project uses pipenv to manage Python dependencies and virtual environments.

### Prerequisites

- Python 3.13
- pipenv installed (`pip install pipenv`)

### Common Commands

#### Running Python Scripts

```bash
# Run a Python script using the pipenv environment
pipenv run python path/to/script.py

# Run with arguments
pipenv run python solution.py input.csv
```

#### Running Tests

```bash
# Run pytest
pipenv run pytest

# Run pytest with verbose output
pipenv run pytest -v

# Run tests for a specific file
pipenv run pytest test_solution.py -v
```

#### Linting

```bash
# Run flake8 linter
pipenv run flake8 file.py

# Run flake8 on multiple files
pipenv run flake8 file1.py file2.py
```

#### Installing Dependencies

```bash
# Install all dependencies from Pipfile
pipenv install

# Install dev dependencies
pipenv install --dev

# Add a new package
pipenv install package_name

# Add a new dev package
pipenv install --dev package_name
```

#### Shell Access

```bash
# Activate the virtual environment shell
pipenv shell

# Exit the shell
exit
```

### Available Packages

**Production packages:**
- pillow - Image processing
- matplotlib - Plotting and visualization
- numpy - Numerical computing
- pulp - Linear programming

**Development packages:**
- flake8 - Code linting
- pytest - Testing framework

### Project Structure

Each day's solution is in its own directory (day1/, day2/, etc.) with:
- `solution.py` - Main solution implementation
- `test_solution.py` - Test cases
- Input files (.csv, .txt, etc.)
