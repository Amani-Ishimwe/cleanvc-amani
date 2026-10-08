import csv
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure src is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cleanvc import CSVCleaner, slugify_header, main


class TestSlugifyHeader(unittest.TestCase):
    def test_basic_slugify(self):
        self.assertEqual(slugify_header("First Name"), "first_name")
        self.assertEqual(slugify_header("Email Address"), "email_address")

    def test_percent_replacement(self):
        self.assertEqual(slugify_header("First Name (%)"), "first_name_pct")
        self.assertEqual(slugify_header("Discount%"), "discount_pct")

    def test_special_characters_and_spaces(self):
        self.assertEqual(slugify_header("  User #ID / Number  "), "user_id_number")
        self.assertEqual(slugify_header("Order-Total ($)"), "order_total")
        self.assertEqual(slugify_header("___leading_and_trailing___"), "leading_and_trailing")


class TestCSVCleaner(unittest.TestCase):
    def setUp(self):
        self.cleaner = CSVCleaner()

    def test_clean_rows_whitespace_and_empty(self):
        raw_data = [
            {" First Name ": "  Alice  ", " Age ": " 30 "},
            {" First Name ": "   ", " Age ": ""},  # completely empty row
            {" First Name ": "Bob", " Age ": "  25  "},
        ]
        cleaned = self.cleaner.clean_rows(raw_data)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(cleaned[0], {"first_name": "Alice", "age": "30"})
        self.assertEqual(cleaned[1], {"first_name": "Bob", "age": "25"})

    def test_clean_rows_partial_values_kept(self):
        raw_data = [
            {" First Name ": "Charlie", " Age ": ""},
        ]
        cleaned = self.cleaner.clean_rows(raw_data)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0], {"first_name": "Charlie", "age": ""})

    def test_process_file_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_csv = tmp_path / "raw.csv"
            output_csv = tmp_path / "cleaned.csv"

            # Write messy CSV with BOM
            with input_csv.open("w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([" First Name (%) ", " Total Spend ($) "])
                writer.writerow(["  John Doe  ", " 100.50 "])
                writer.writerow(["   ", "   "])  # empty row
                writer.writerow(["Jane Smith", " 250.00 "])

            result_path = self.cleaner.process_file(str(input_csv), str(output_csv))
            self.assertEqual(result_path, str(output_csv))
            self.assertTrue(output_csv.exists())

            # Read back cleaned file
            with output_csv.open("r", encoding="utf-8") as f:
                reader = list(csv.DictReader(f))

            self.assertEqual(len(reader), 2)
            self.assertEqual(reader[0]["first_name_pct"], "John Doe")
            self.assertEqual(reader[0]["total_spend"], "100.50")
            self.assertEqual(reader[1]["first_name_pct"], "Jane Smith")
            self.assertEqual(reader[1]["total_spend"], "250.00")

    def test_process_file_default_output_name(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_csv = tmp_path / "data.csv"
            expected_output = tmp_path / "cleaned_data.csv"

            with input_csv.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Header A", "Header B"])
                writer.writerow(["Val 1", "Val 2"])

            result_path = self.cleaner.process_file(str(input_csv))
            self.assertEqual(result_path, str(expected_output))
            self.assertTrue(expected_output.exists())


class TestCLI(unittest.TestCase):
    def test_cli_execution(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_csv = tmp_path / "messy.csv"
            output_csv = tmp_path / "output.csv"

            with input_csv.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([" First (%) ", " Age "])
                writer.writerow(["  Sam  ", " 22 "])

            exit_code = main([str(input_csv), "-o", str(output_csv)])
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_csv.exists())

            with output_csv.open("r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["first_pct"], "Sam")


if __name__ == "__main__":
    unittest.main()
