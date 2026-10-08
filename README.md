# cleanvc

[![PyPI](https://img.shields.io/pypi/v/cleanvc.svg)](https://pypi.org/project/cleanvc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A lightweight, zero-dependency Python tool and CLI to clean up messy CSV files.

## Features

- **Header Normalization**: Automatically converts column headers into clean snake_case identifiers (e.g., `First Name (%)` -> `first_name_pct`).
- **Whitespace Stripping**: Strips extraneous leading and trailing spaces from values and headers.
- **Empty Row Removal**: Automatically discards completely blank rows.
- **UTF-8 with BOM Support**: Safely reads CSV files exported from Excel and other spreadsheet software (`utf-8-sig`).
- **CLI & Python API**: Use as a command-line utility or import in your Python scripts.
- **Zero Dependencies**: Powered exclusively by the Python standard library.

## Installation

```bash
pip install cleanvc
```

---

## Command-Line Usage (CLI)

Once installed, use `cleanvc` directly from your terminal:

```bash
# Clean a messy CSV (creates cleaned_messy.csv automatically)
cleanvc messy.csv

# Specify custom output destination
cleanvc messy.csv -o clean_data.csv

# Custom delimiter (e.g., semicolon)
cleanvc messy.csv -d ";" -o clean_data.csv

# Check version
cleanvc --version
```

You can also run it via Python module invocation:
```bash
python -m cleanvc messy.csv -o clean_data.csv
```

---

## Python API Usage

### Process a CSV File

```python
from cleanvc import CSVCleaner

cleaner = CSVCleaner()

# Automatically saves as cleaned_messy_sales.csv
cleaner.process_file("messy_sales.csv")

# Or specify your own output path
cleaner.process_file("messy_sales.csv", "cleaned_sales.csv")
```

### In-Memory Row Cleaning

```python
from cleanvc import CSVCleaner

cleaner = CSVCleaner()
raw_data = [
    {" First Name (%) ": "  Alice  ", " Score ": " 95 "},
    {" First Name (%) ": "   ", " Score ": ""},  # Automatically dropped
    {" First Name (%) ": "  Bob  ", " Score ": " 80 "},
]

cleaned = cleaner.clean_rows(raw_data)
# [
#   {"first_name_pct": "Alice", "score": "95"},
#   {"first_name_pct": "Bob", "score": "80"}
# ]
```

---

## Running Tests

Run the unit tests with Python's standard `unittest` runner:

```bash
python -m unittest discover -v tests
```

---

## Publishing to PyPI

1. **Install build and upload tools**:
   ```bash
   pip install --upgrade build twine
   ```

2. **Build distribution artifacts**:
   ```bash
   python -m build
   ```
   This generates the wheel (`.whl`) and source distribution (`.tar.gz`) in `dist/`.

3. **Verify the build**:
   ```bash
   twine check dist/*
   ```

4. **Upload to TestPyPI (Recommended first)**:
   ```bash
   twine upload --repository testpypi dist/*
   ```

5. **Publish to PyPI**:
   ```bash
   twine upload dist/*
   ```

## License

MIT License. See [LICENSE](LICENSE) for details.
