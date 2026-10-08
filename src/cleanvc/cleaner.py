import csv
import re
from pathlib import Path
from typing import List, Dict, Optional

def slugify_header(name: str) -> str:
    """Normalize headers: 'First Name (%)' -> 'first_name_pct'."""
    name = name.strip().lower()
    name = re.sub(r"[%]", "_pct", name)
    name = re.sub(r"[\s\-]+", "_", name)
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

class CSVCleaner:
    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    def clean_rows(self, raw_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Clean keys, strip whitespace from values, and drop fully empty rows."""
        cleaned_records = []
        for row in raw_data:
            cleaned_row = {}
            has_value = False
            for key, val in row.items():
                clean_key = slugify_header(key)
                clean_val = val.strip() if val else ""
                if clean_val:
                    has_value = True
                cleaned_row[clean_key] = clean_val
            
            if has_value:
                cleaned_records.append(cleaned_row)
        return cleaned_records

    def process_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """Reads, cleans, and saves the cleaned CSV data."""
        in_file = Path(input_path)
        out_file = Path(output_path) if output_path else in_file.with_name(f"cleaned_{in_file.name}")

        with in_file.open(mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            records = [row for row in reader]

        cleaned = self.clean_rows(records)

        if cleaned:
            fieldnames = list(cleaned[0].keys())
            with out_file.open(mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=self.delimiter)
                writer.writeheader()
                writer.writerows(cleaned)

        return str(out_file)
