"""Labwork 5a checks use synthetic data in temporary directories."""

import csv
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_labworks import PW5, ROOT


spec = importlib.util.spec_from_file_location("pw5_extras", ROOT / "pw5/extras.py")
EXTRAS = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"persistence": PW5.persistence}):
    spec.loader.exec_module(EXTRAS)


class ExtrasTests(unittest.TestCase):
    def make_manager(self):
        manager = PW5.manager()
        manager.add_student("001", 'Nguyễn, "An"', "2006-01-02")
        manager.add_student("002", "NA", "2006-03-04")
        manager.add_course("007", 'Python, "cơ bản"', 3)
        manager.set_mark("001", "007", 8.79)
        manager.set_mark("002", "007", 0)
        return manager

    def test_csv_round_trip_preserves_text_numbers_and_references(self):
        manager = self.make_manager()
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            exports = EXTRAS.export_csv(manager, directory)
            self.assertEqual(exports, Path(directory) / "exports")
            frames = EXTRAS.load_csv_frames(exports)
            self.assertEqual([len(frames[name]) for name in EXTRAS.CSV_COLUMNS], [2, 1, 2])
            students = frames["students"].to_dict(orient="records")
            self.assertEqual(students, [
                {"id": "001", "name": 'Nguyễn, "An"', "dob": "2006-01-02"},
                {"id": "002", "name": "NA", "dob": "2006-03-04"},
            ])
            self.assertEqual(frames["courses"].to_dict(orient="records"), [
                {"id": "007", "name": 'Python, "cơ bản"', "credits": 3},
            ])
            self.assertEqual(frames["marks"].to_dict(orient="records"), [
                {"student_id": "001", "course_id": "007", "score": 8.7},
                {"student_id": "002", "course_id": "007", "score": 0.0},
            ])
            with (exports / "students.csv").open(encoding="utf-8", newline="") as stream:
                self.assertEqual(list(csv.DictReader(stream)), students)
            self.assertFalse(any(frame.isna().any().any() for frame in frames.values()))

    def test_empty_exports_have_headers_and_pickle_round_trip(self):
        manager = PW5.manager()
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            exports = EXTRAS.export_csv(manager, directory)
            frames = EXTRAS.load_csv_frames(exports)
            for name, columns in EXTRAS.CSV_COLUMNS.items():
                self.assertEqual(list(frames[name].columns), list(columns))
                self.assertTrue(frames[name].empty)
            restored = EXTRAS.pickle_round_trip(manager, exports)
            self.assertEqual(PW5.persistence.records_from_manager(restored), {
                "students.txt": [], "courses.txt": [], "marks.txt": [],
            })
            self.assertTrue((exports / "snapshot.pkl").is_file())

    def test_pickle_ignores_existing_snapshot_and_preserves_files_on_failure(self):
        manager = self.make_manager()
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            PW5.persistence.save_archive(manager, directory)
            originals = {name: (Path(directory) / name).read_bytes()
                         for name in (*PW5.persistence.FILES, "students.dat")}
            exports = Path(directory) / "exports"
            exports.mkdir()
            snapshot = exports / "snapshot.pkl"
            snapshot.write_bytes(b"not a trusted pickle")
            with patch.object(EXTRAS.pickle, "dump", side_effect=OSError("write failed")):
                with self.assertRaises(OSError):
                    EXTRAS.pickle_round_trip(manager, exports)
            self.assertEqual(snapshot.read_bytes(), b"not a trusted pickle")
            self.assertFalse(list(exports.glob("*.tmp")))
            restored = EXTRAS.pickle_round_trip(manager, exports)
            self.assertEqual(PW5.persistence.records_from_manager(restored),
                             PW5.persistence.records_from_manager(manager))
            self.assertNotEqual(snapshot.read_bytes(), b"not a trusted pickle")
            self.assertEqual(originals, {name: (Path(directory) / name).read_bytes()
                                         for name in originals})

    def test_query_equality_duplicates_escapes_and_invalid_conditions(self):
        students = EXTRAS.pd.DataFrame([
            {"id": "001", "name": "Mr. Volunteers", "dob": "2006"},
            {"id": "002", "name": "Mr. Volunteers", "dob": "2007"},
            {"id": "003", "name": 'Nguyễn, "An"', "dob": "2006"},
            {"id": "004", "name": "NA", "dob": "2008"},
        ])
        before = students.copy(deep=True)
        self.assertEqual(EXTRAS.query_students(students, 'name = "Mr. Volunteers"')["id"].tolist(), ["001", "002"])
        self.assertEqual(EXTRAS.query_students(students, ' id == "003" ')["name"].tolist(), ['Nguyễn, "An"'])
        condition = "name = " + json.dumps('Nguyễn, "An"', ensure_ascii=False)
        self.assertEqual(EXTRAS.query_students(students, condition)["id"].tolist(), ["003"])
        self.assertTrue(EXTRAS.query_students(students, 'name = "missing"').empty)
        self.assertEqual(EXTRAS.query_students(students, 'name = "NA"')["id"].tolist(), ["004"])
        for condition in ("", "   ", 'age = "20"', 'name != "NA"',
                          'name = "NA" or id = "001"', "name = __import__('os')",
                          r'name = "bad\q"', 'name = "unclosed'):
            with self.subTest(condition=condition), self.assertRaises(ValueError):
                EXTRAS.query_students(students, condition)
        EXTRAS.pd.testing.assert_frame_equal(students, before)

    def test_csv_loader_rejects_wrong_columns_and_broken_references(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            exports = EXTRAS.export_csv(self.make_manager(), directory)
            (exports / "marks.csv").write_text("student_id,course_id,score\nmissing,007,8.7\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                EXTRAS.load_csv_frames(exports)
            (exports / "students.csv").write_text("id,name\n001,Alice\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                EXTRAS.load_csv_frames(exports)

    def test_real_cli_creates_archive_then_exports_and_queries(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            options = dict(text=True, encoding="utf-8", capture_output=True, timeout=20,
                           cwd=directory, env=os.environ | {"PYTHONIOENCODING": "utf-8"})
            data = "1\n001\nMr. Volunteers\n2006\n1\n002\nMr. Volunteers\n2007\n2\n007\nPython\n3\n3\n001\n007\n8.79\n0\n"
            first = subprocess.run([sys.executable, "-B", str(ROOT / "pw5/main.py"), "--data-dir", directory], input=data, **options)
            self.assertEqual(first.returncode, 0, first.stderr)
            archive = (Path(directory) / "students.dat").read_bytes()
            command = [sys.executable, "-B", str(ROOT / "pw5/extras.py"), "--data-dir", directory]
            result = subprocess.run(command, input='name = "Mr. Volunteers"\n', **options)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Pickle round-trip: PASS", result.stdout)
            self.assertIn("students=2; courses=1; marks=1", result.stdout)
            self.assertIn("001", result.stdout)
            self.assertIn("002", result.stdout)
            for condition, code, message in [
                ('name = "missing"\n', 0, "No students matched."),
                ("\n", 0, "Query skipped."),
                ('age = "20"\n', 2, "Student query columns"),
            ]:
                checked = subprocess.run(command, input=condition, **options)
                self.assertEqual(checked.returncode, code, checked.stderr)
                self.assertIn(message, checked.stdout)
            self.assertEqual((Path(directory) / "students.dat").read_bytes(), archive)


if __name__ == "__main__":
    unittest.main()
