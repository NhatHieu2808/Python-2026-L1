"""Check Labwork 5 against an independent CSV and statistics calculation."""

import csv
import hashlib
from pathlib import Path
from statistics import mean
import subprocess
import sys
import unittest

import pandas as pd

from labwork5_pandas.main import analyze_scores, analyze_students


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labwork5_pandas"


class PandasLabTests(unittest.TestCase):
    def setUp(self):
        self.students = pd.read_csv(LAB / "students.csv")
        self.scores = pd.read_csv(LAB / "scores.csv")
        with (LAB / "students.csv").open(encoding="utf-8", newline="") as file:
            self.student_rows = list(csv.DictReader(file))
        with (LAB / "scores.csv").open(encoding="utf-8", newline="") as file:
            self.score_rows = list(csv.DictReader(file))

    def test_original_student_analysis(self):
        original = self.students.copy(deep=True)
        result = analyze_students(self.students)
        self.assertEqual(result["shape"], (30, 5))
        self.assertEqual(
            result["first_five"]["student_id"].tolist(),
            [row["student_id"] for row in self.student_rows[:5]],
        )
        self.assertEqual(result["name_gpa"].columns.tolist(), ["name", "GPA"])
        self.assertEqual(result["name_gpa"]["name"].tolist(), self.students["name"].tolist())
        self.assertEqual(result["name_gpa"]["GPA"].isna().sum(), 2)
        expected_filtered = [
            row["student_id"] for row in self.student_rows
            if row["GPA"] and float(row["GPA"]) >= 3.5
        ]
        self.assertEqual(result["gpa_at_least_3_5"]["student_id"].tolist(), expected_filtered)
        expected_order = sorted(
            self.student_rows,
            key=lambda row: float(row["GPA"]) if row["GPA"] else -float("inf"),
            reverse=True,
        )
        self.assertEqual(
            result["sorted_by_gpa"]["student_id"].tolist(),
            [row["student_id"] for row in expected_order],
        )
        for major, actual in result["average_gpa_by_major"].items():
            expected = mean(
                float(row["GPA"]) for row in self.student_rows
                if row["major"] == major and row["GPA"]
            )
            self.assertAlmostEqual(actual, expected)
        pd.testing.assert_frame_equal(self.students, original)

    def test_clean_merge_and_score_summaries(self):
        original_students = self.students.copy(deep=True)
        original_scores = self.scores.copy(deep=True)
        result = analyze_scores(self.students, self.scores)
        self.assertEqual(
            result["student_missing"].to_dict(),
            {"student_id": 0, "name": 0, "age": 1, "major": 0, "GPA": 2},
        )
        self.assertEqual(
            result["score_missing"].to_dict(),
            {"student_id": 0, "python": 0, "math": 2, "database": 1},
        )
        self.assertFalse(result["clean_students"].isna().any().any())
        self.assertFalse(result["clean_scores"].isna().any().any())
        merged = result["merged"].set_index("student_id")
        self.assertEqual(result["merged"].shape, (30, 9))
        self.assertEqual(set(merged.index), {row["student_id"] for row in self.student_rows})
        for column in ["age", "GPA"]:
            observed_mean = mean(float(row[column]) for row in self.student_rows if row[column])
            for row in self.student_rows:
                expected = float(row[column]) if row[column] else observed_mean
                self.assertAlmostEqual(merged.loc[row["student_id"], column], expected)
        expected_averages = {}
        score_means = {
            column: mean(float(row[column]) for row in self.score_rows if row[column])
            for column in ["python", "math", "database"]
        }
        for row in self.score_rows:
            values = []
            for column in ["python", "math", "database"]:
                expected = float(row[column]) if row[column] else score_means[column]
                self.assertAlmostEqual(merged.loc[row["student_id"], column], expected)
                values.append(expected)
            expected_averages[row["student_id"]] = mean(values)
            self.assertAlmostEqual(merged.loc[row["student_id"], "average_score"], mean(values))
        expected_top = sorted(expected_averages, key=expected_averages.get, reverse=True)[:5]
        self.assertEqual(result["top_five"]["student_id"].tolist(), expected_top)
        for major, actual in result["average_score_by_major"].items():
            expected = mean(
                expected_averages[row["student_id"]] for row in self.student_rows
                if row["major"] == major
            )
            self.assertAlmostEqual(actual, expected)
        pd.testing.assert_frame_equal(self.students, original_students)
        pd.testing.assert_frame_equal(self.scores, original_scores)

    def test_cli_covers_14_requirements_and_preserves_csv_files(self):
        files = [LAB / "students.csv", LAB / "scores.csv"]
        hashes = [hashlib.sha256(file.read_bytes()).hexdigest() for file in files]
        completed = subprocess.run(
            [sys.executable, "-B", str(LAB / "main.py")],
            cwd=ROOT.parent, capture_output=True, text=True, encoding="utf-8",
            check=True, timeout=20,
        )
        for part in [1, 2]:
            for exercise in range(1, 8):
                self.assertEqual(completed.stdout.count(f"[{part}.{exercise}]"), 1)
        self.assertIn("Rows: 30; columns: 5", completed.stdout)
        self.assertIn("Filled values are estimates", completed.stdout)
        self.assertEqual(hashes, [hashlib.sha256(file.read_bytes()).hexdigest() for file in files])


if __name__ == "__main__":
    unittest.main()
