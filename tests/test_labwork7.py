"""Focused checks for the OOP lab, including real console processes."""

from contextlib import redirect_stdout
import importlib.util
from io import StringIO
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "2.student.mark.oop.py"
SPEC = importlib.util.spec_from_file_location("labwork7", SCRIPT)
LAB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAB)


class Labwork7Tests(unittest.TestCase):
    def test_encapsulation_and_validated_updates(self):
        student = LAB.Student(" 001 ", "Nguyễn An", "01/01/2006")
        self.assertEqual(student.get_id(), "001")
        student.set_name("  Trương Quý Nhật Hiếu  ")
        student.set_date_of_birth(" 28/08/2006 ")
        self.assertEqual(student.get_name(), "Trương Quý Nhật Hiếu")
        self.assertEqual(student.get_date_of_birth(), "28/08/2006")
        for item_id in ("", "  ", None, 1):
            with self.subTest(item_id=item_id), self.assertRaises(ValueError):
                LAB.Student(item_id)
        with self.assertRaises(ValueError):
            student.set_name(None)
        with self.assertRaises(ValueError):
            student.set_date_of_birth(None)
        self.assertEqual(student.get_name(), "Trương Quý Nhật Hiếu")
        self.assertEqual(student.get_date_of_birth(), "28/08/2006")
        for attribute in ("__id", "__name", "__date_of_birth"):
            self.assertFalse(hasattr(student, attribute))
        manager = LAB.StudentMarkManager()
        manager.add_student(student)
        manager.add_course(LAB.Course("PY", "Python"))
        snapshot = manager.get_students()
        self.assertIsInstance(snapshot, tuple)
        snapshot += (LAB.Student("002"),)
        self.assertEqual(len(manager.get_students()), 1)
        for add, record in ((manager.add_student, LAB.Student("001")),
                            (manager.add_course, LAB.Course("PY")),
                            (manager.add_student, LAB.Course("DB")),
                            (manager.add_course, LAB.Student("002"))):
            with self.assertRaises(ValueError):
                add(record)
        self.assertEqual(manager.get_students(), (student,))
        self.assertEqual(len(manager.get_courses()), 1)

    def test_polymorphic_input_and_listing(self):
        records = [LAB.Student("001"), LAB.Course("PY")]
        output = StringIO()
        with patch("builtins.input", side_effect=["Nguyễn An", "01/01/2006", "Python"]), redirect_stdout(output):
            for record in records:
                record.input()
                record.list()
        self.assertIsInstance(records[0], LAB.NamedRecord)
        self.assertIsInstance(records[1], LAB.NamedRecord)
        self.assertIsNot(LAB.Student.input, LAB.Course.input)
        self.assertIsNot(LAB.Student.list, LAB.Course.list)
        self.assertEqual(output.getvalue().splitlines(), [
            f"{'001':<12}{'Nguyễn An':<30}01/01/2006",
            f"{'PY':<12}Python",
        ])

    def test_marks_are_validated_and_isolated_by_student_and_course(self):
        manager = LAB.StudentMarkManager()
        for student_id in ("001", "002"):
            manager.add_student(LAB.Student(student_id))
        for course_id in ("PY", "DB"):
            manager.add_course(LAB.Course(course_id))
        self.assertIsNone(manager.get_mark("002", "DB"))
        manager.set_mark("001", "PY", 0)
        manager.set_mark("002", "PY", 10)
        manager.set_mark("001", "DB", 8.75)
        manager.set_mark("002", "DB", 7.125)
        for score in (-1, 10.01, float("nan"), float("inf"), -float("inf"), "bad"):
            with self.subTest(score=score), self.assertRaises(ValueError):
                manager.set_mark("001", "DB", score)
        for student_id, course_id in (("unknown", "PY"), ("001", "unknown")):
            with self.assertRaises(ValueError):
                manager.set_mark(student_id, course_id, 5)
            with self.assertRaises(ValueError):
                manager.get_mark(student_id, course_id)
        self.assertEqual([manager.get_mark(s, c) for s, c in (
            ("001", "PY"), ("002", "PY"), ("001", "DB"), ("002", "DB"))],
            [0.0, 10.0, 8.75, 7.125])
        manager.set_mark("001", "DB", 9.375)
        self.assertEqual(manager.get_mark("001", "DB"), 9.375)
        self.assertEqual(manager.get_mark("002", "DB"), 7.125)

    def run_cli(self, answers):
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as working_directory:
            result = subprocess.run(
                [sys.executable, "-B", str(SCRIPT)],
                input="\n".join(answers) + "\n", cwd=working_directory,
                capture_output=True, text=True, encoding="utf-8",
                env=environment, timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual(list(Path(working_directory).iterdir()), [])
        return result.stdout

    def test_cli_two_students_two_courses_and_invalid_input(self):
        first, second = "Nguyễn Trương Thị Phương Thảo", "Trương Quý Nhật Hiếu"
        output = self.run_cli([
            "-1", "bad", "2", "", "001", first, "01/01/2006",
            "001", "002", second, "28/08/2006",
            "2", "", "PY", "Python", "PY", "DB", "Database",
            "1", "2", "4", "DB", "3", "unknown", "4", "unknown", "9",
            "3", "PY", "-1", "11", "nan", "inf", "-inf", "bad", "0", "10",
            "3", "DB", "8.75", "7.125", "4", "PY", "4", "DB", "0",
        ])
        for expected in ("STUDENTS", "COURSES", "MARKS FOR Python", "MARKS FOR Database",
                         "ID cannot be empty.", "ID already exists.", "Invalid option.",
                         "Please enter a non-negative integer."):
            self.assertIn(expected, output)
        self.assertEqual(output.count("Course not found."), 2)
        self.assertEqual(output.count("Not entered"), 2)
        self.assertEqual(output.count("Please enter a mark from 0 to 10."), 6)
        for student_id, name, value in (("001", first, "0.0"), ("002", second, "10.0"),
                                        ("001", first, "8.75"), ("002", second, "7.125")):
            self.assertIn(f"{student_id:<12}{name:<30}{value}", output)
        self.assertIn(f"{'001':<12}{first:<30}01/01/2006", output)
        self.assertIn(f"{'DB':<12}Database", output)

    def test_cli_empty_lists_and_unknown_course(self):
        output = self.run_cli(["0", "0", "1", "2", "3", "PY", "4", "PY", "0"])
        self.assertIn("STUDENTS", output)
        self.assertIn("COURSES", output)
        self.assertEqual(output.count("Course not found."), 2)


if __name__ == "__main__":
    unittest.main()
