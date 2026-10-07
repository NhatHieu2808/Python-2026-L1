"""Run with python -B -m unittest discover -s tests -v from the repository root."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_application(directory):
    names = ("domains", "input", "output", "persistence")
    saved = {name: module for name, module in sys.modules.items()
             if name in names or name.startswith("domains.")}
    for name in saved:
        del sys.modules[name]
    sys.path.insert(0, str(ROOT / directory))
    try:
        main = load_module(directory + "_main", ROOT / directory / "main.py")
        return SimpleNamespace(
            main=main, input=sys.modules["input"], output=sys.modules["output"],
            manager=sys.modules["domains"].StudentMarkManager,
            persistence=sys.modules.get("persistence"),
        )
    finally:
        sys.path.pop(0)
        for name in list(sys.modules):
            if name in names or name.startswith("domains."):
                del sys.modules[name]
        sys.modules.update(saved)


LAB1 = load_module("lab1", ROOT / "labwork1.py")
LAB1B = load_module("lab1b", ROOT / "labwork1b.py")
PW3 = load_module("pw3", ROOT / "3.student.mark.oop.math.py")
PW4 = load_application("pw4")
PW5 = load_application("pw5")


class FakeCurses:
    A_BOLD = 1
    KEY_DOWN = 258
    KEY_UP = 259
    KEY_LEFT = 260
    KEY_RIGHT = 261
    KEY_NPAGE = 338
    KEY_PPAGE = 339

    @staticmethod
    def curs_set(value):
        return None

    @staticmethod
    def echo():
        return None

    @staticmethod
    def noecho():
        return None


class FakeScreen:
    def __init__(self, keys, texts=(), height=24, width=80):
        self.keys = iter(keys)
        self.texts = iter(texts)
        self.height = height
        self.width = width
        self.writes = []

    def getmaxyx(self):
        return self.height, self.width

    def clear(self):
        return None

    def refresh(self):
        return None

    def addnstr(self, row, column, text, length, *attributes):
        if not (0 <= row < self.height and 0 <= column < self.width):
            raise AssertionError("Write outside the screen")
        self.writes.append(str(text)[:length])

    def getch(self):
        return next(self.keys)

    def getstr(self, row, column, length):
        if not (0 <= row < self.height and 0 <= column < self.width):
            raise AssertionError("Input outside the screen")
        return next(self.texts).encode("utf-8")[:length]


class LabworkTests(unittest.TestCase):
    def test_lab1_all_exercises_and_boundaries(self):
        self.assertEqual(LAB1.calculate_circle_area(10), 314.0)
        self.assertEqual(LAB1.celsius_to_fahrenheit(10), 50.0)
        for value in (-3, 0, 1, 6):
            self.assertFalse(LAB1.is_prime(value))
        for value in (2, 3, 13):
            self.assertTrue(LAB1.is_prime(value))
        for value in (6, 28):
            self.assertTrue(LAB1.is_perfect(value))
        self.assertFalse(LAB1.is_perfect(30))
        self.assertEqual(LAB1.find_color(["Blue", "Yellow", "White", "Red"], "Red"), 3)
        self.assertEqual(LAB1.find_color([], "Red"), -1)
        self.assertEqual(LAB1.create_ranges(), ([0, 1, 2, 3, 4, 5, 6], [1, 4, 7, 10], [5, 4, 3, 2, 1], [6, 4, 2, 0, -2]))
        self.assertEqual(LAB1.remove_dollar_sign("$$a$"), "a")
        self.assertEqual(LAB1.remove_dollar_sign(""), "")
        self.assertEqual(LAB1.extract_even([1, 4, 5, -1, 10, 0, -2]), [4, 10, 0, -2])
        self.assertEqual(LAB1.factorial(0), 1)
        self.assertEqual(LAB1.factorial(5), 120)
        with self.assertRaises(ValueError):
            LAB1.factorial(-1)
        self.assertEqual(LAB1.get_divisors(-12), [1, 2, 3, 4, 6, 12])
        with self.assertRaises(ValueError):
            LAB1.get_divisors(0)
        self.assertEqual(LAB1.distance_between_points(0, 0, 3, 4), 5.0)
        self.assertEqual(LAB1.create_pattern(4, 5), "* * * * *\n*       *\n*       *\n* * * * *")
        self.assertEqual(LAB1.create_pattern(3, 1), "*\n*\n*")

    def test_lab1b_duplicate_and_empty_ids_retry(self):
        values = ["2", "", "S1", "Alice", "2006", "S1", "S2", "Bob", "2007"]
        with patch("builtins.input", side_effect=values), contextlib.redirect_stdout(io.StringIO()):
            students = LAB1B.input_students()
        with patch("builtins.input", side_effect=["C1", "nan", "-1", "8.5", "7"]), contextlib.redirect_stdout(io.StringIO()):
            marks = {}
            LAB1B.input_marks(students, [{"id": "C1", "name": "Python"}], marks)
        self.assertEqual(marks, {"C1": {"S1": 8.5, "S2": 7.0}})
        with self.assertRaises(ValueError):
            LAB1B.validate_unique_ids([{"id": "S1"}, {"id": "S1"}], "Student")

    def test_oop_validation_gpa_and_sorting(self):
        for factory in (PW3.StudentMarkManager, PW4.manager, PW5.manager):
            with self.subTest(manager=factory):
                manager = factory()
                manager.add_student("S1", "Alice", "2006")
                manager.add_student("S2", "Bob", "2007")
                manager.add_course("A", "Python", 3)
                manager.add_course("B", "Math", 1)
                for sid, a, b in (("S1", 8.79, 6.29), ("S2", 7.99, 7.99)):
                    manager.set_mark(sid, "A", a)
                    manager.set_mark(sid, "B", b)
                self.assertEqual(manager.students["S1"].marks["A"], 8.7)
                self.assertAlmostEqual(manager.students["S1"].calculate_gpa(manager.courses), 8.075)
                self.assertEqual([s.student_id for s in manager.students_by_gpa()], ["S1", "S2"])
                for score in (-1, 10.1, float("nan"), float("inf"), 10 ** 1000):
                    with self.assertRaises(ValueError):
                        manager.set_mark("S1", "A", score)
                for score in (0, 10):
                    manager.set_mark("S1", "A", score)
                    self.assertEqual(manager.students["S1"].marks["A"], score)
                for credits in (0, -1, 1.5, float("nan"), True):
                    with self.assertRaises(ValueError):
                        manager.add_course("invalid", "Invalid", credits)
                for sid in ("", "  ", " S1 "):
                    with self.assertRaises(ValueError):
                        manager.add_student(sid, "Other", "2008")

    def test_console_input_retries_duplicate_ids(self):
        for app in (PW4, PW5):
            with tempfile.TemporaryDirectory(dir=ROOT) as directory:
                manager = app.manager()
                manager.data_directory = Path(directory)
                manager.add_student("S1", "First", "2006")
                with patch("builtins.input", side_effect=["", "S1", "S2", "Second", "2007"]), contextlib.redirect_stdout(io.StringIO()):
                    app.input.input_student(manager)
                self.assertEqual(list(manager.students), ["S1", "S2"])
                self.assertEqual(manager.students["S1"].name, "First")

    def test_curses_pagination_and_horizontal_scroll(self):
        for module in (PW3, PW4.output, PW5.output):
            with patch.object(module, "curses", FakeCurses):
                lines = [f"S{i:<9}Student {i:<17}2006-01-01     8.70" for i in range(30)]
                screen = FakeScreen([FakeCurses.KEY_RIGHT, FakeCurses.KEY_DOWN, FakeCurses.KEY_NPAGE, FakeCurses.KEY_LEFT, ord("q")], height=10, width=40)
                module.show_lines_curses(screen, "Students", lines)
                self.assertTrue(any("8.70" in line for line in screen.writes))
                self.assertTrue(any("2/" in line for line in screen.writes))

    def test_curses_complete_menus(self):
        for app in (PW4, PW5):
            with tempfile.TemporaryDirectory(dir=ROOT) as directory:
                manager = app.manager()
                manager.data_directory = Path(directory)
                keys = [ord(k) for k in ["1", "q", "2", "q", "3", "q", "4", "q", "5", "q", "6", "q", "0"]]
                texts = ["S1", "Alice", "2006", "C1", "Python", "3", "S1", "C1", "8.79", "C1"]
                screen = FakeScreen(keys, texts)
                with patch.object(app.main, "curses", FakeCurses), patch.object(app.input, "curses", FakeCurses), patch.object(app.output, "curses", FakeCurses):
                    app.main.run_curses_menu(screen, manager)
                self.assertEqual(manager.students["S1"].marks["C1"], 8.7)
                self.assertTrue(any("8.70" in line for line in screen.writes))
                if app is PW5:
                    self.assertTrue((Path(directory) / "students.dat").exists())


class PersistenceTests(unittest.TestCase):
    def make_manager(self, directory):
        manager = PW5.manager()
        manager.data_directory = Path(directory)
        manager.add_student("S1", "Trương Quý Nhật Hiếu", "2006-08-28")
        manager.add_course("A", "Lập trình Python", 3)
        manager.add_course("B", "Toán", 1)
        manager.set_mark("S1", "A", 8.79)
        manager.set_mark("S1", "B", 6.29)
        return manager

    def test_first_run_and_empty_dataset(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            manager = PW5.persistence.load_data(directory)
            self.assertFalse(manager.students)
            PW5.persistence.save_archive(manager)
            self.assertFalse(PW5.persistence.load_data(directory).students)

    def test_utf8_compression_and_restore_without_text_files(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            manager = self.make_manager(directory)
            PW5.persistence.save_text_files(manager)
            self.assertIn("Trương", (Path(directory) / "students.txt").read_text(encoding="utf-8"))
            PW5.persistence.save_archive(manager)
            with zipfile.ZipFile(Path(directory) / "students.dat") as archive:
                self.assertEqual(set(archive.namelist()), set(PW5.persistence.FILES))
                self.assertTrue(all(entry.compress_type == zipfile.ZIP_DEFLATED for entry in archive.infolist()))
            for name in PW5.persistence.FILES:
                (Path(directory) / name).unlink()
            restored = PW5.persistence.load_data(directory)
            self.assertEqual(restored.students["S1"].name, "Trương Quý Nhật Hiếu")
            self.assertEqual(restored.students["S1"].marks, {"A": 8.7, "B": 6.2})
            self.assertAlmostEqual(restored.students["S1"].calculate_gpa(restored.courses), 8.075)
            self.assertTrue(all((Path(directory) / name).exists() for name in PW5.persistence.FILES))

    def test_corrupt_archives_preserve_existing_files(self):
        for content in (b"", b"not a zip file"):
            with tempfile.TemporaryDirectory(dir=ROOT) as directory:
                manager = self.make_manager(directory)
                PW5.persistence.save_text_files(manager)
                paths = [Path(directory) / name for name in PW5.persistence.FILES]
                before = [path.read_bytes() for path in paths]
                (Path(directory) / "students.dat").write_bytes(content)
                with self.assertRaises(ValueError):
                    PW5.persistence.load_data(directory)
                self.assertEqual([path.read_bytes() for path in paths], before)

    def test_invalid_json_and_duplicate_references_do_not_replace_files(self):
        cases = [
            {"students.txt": "", "courses.txt": "[]", "marks.txt": "[]"},
            {"students.txt": '[{"id":"S1","name":"A","dob":"2006"},{"id":"S1","name":"B","dob":"2007"}]', "courses.txt": "[]", "marks.txt": "[]"},
            {"students.txt": "[]", "courses.txt": "[]", "marks.txt": '[{"student_id":"missing","course_id":"missing","score":8}]'},
            {"students.txt": "[]", "courses.txt": "[]", "marks.txt": '[{"student_id":"S1","course_id":"C1","score":NaN}]'},
        ]
        for contents in cases:
            with tempfile.TemporaryDirectory(dir=ROOT) as directory:
                PW5.persistence.save_text_files(self.make_manager(directory))
                before = {name: (Path(directory) / name).read_bytes() for name in PW5.persistence.FILES}
                with zipfile.ZipFile(Path(directory) / "students.dat", "w") as archive:
                    for name, value in contents.items():
                        archive.writestr(name, value)
                with self.assertRaises(ValueError):
                    PW5.persistence.load_data(directory)
                self.assertEqual(before, {name: (Path(directory) / name).read_bytes() for name in PW5.persistence.FILES})

    def test_plain_files_load_and_incomplete_files_fail(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            PW5.persistence.save_text_files(self.make_manager(directory))
            self.assertIn("S1", PW5.persistence.load_data(directory).students)
            (Path(directory) / "marks.txt").unlink()
            with self.assertRaises(ValueError):
                PW5.persistence.load_data(directory)

    def test_archive_member_names_are_validated(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            with zipfile.ZipFile(Path(directory) / "students.dat", "w") as archive:
                archive.writestr("../outside.txt", "do not extract")
            with self.assertRaises(ValueError):
                PW5.persistence.load_data(directory)
            self.assertEqual([p.name for p in Path(directory).iterdir()], ["students.dat"])

    def test_failed_archive_replace_keeps_previous_archive(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            manager = self.make_manager(directory)
            PW5.persistence.save_archive(manager)
            path = Path(directory) / "students.dat"
            before = path.read_bytes()
            original_replace = PW5.persistence.os.replace
            def fail_archive(source, destination):
                if Path(destination).name == "students.dat":
                    raise OSError("simulated archive write failure")
                return original_replace(source, destination)
            manager.set_mark("S1", "A", 9.9)
            with patch.object(PW5.persistence.os, "replace", side_effect=fail_archive):
                with self.assertRaises(OSError):
                    PW5.persistence.save_archive(manager)
            self.assertEqual(path.read_bytes(), before)
            self.assertFalse(list(Path(directory).glob("*.tmp")))

    def test_two_process_save_restore_and_corruption_exit(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            command = [sys.executable, "-B", str(ROOT / "pw5/main.py"), "--data-dir", directory]
            data = "1\nS1\nTrương Quý Nhật Hiếu\n2006-08-28\n2\nC1\nPython\n3\n3\nS1\nC1\n8.79\n0\n"
            options = dict(text=True, encoding="utf-8", capture_output=True, timeout=20, env=__import__("os").environ | {"PYTHONIOENCODING": "utf-8"})
            first = subprocess.run(command, input=data, **options)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("Saved students.dat", first.stdout)
            second = subprocess.run(command, input="4\n6\nC1\n0\n", **options)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("Trương Quý Nhật Hiếu", second.stdout)
            self.assertIn("8.70", second.stdout)
            paths = [Path(directory) / name for name in PW5.persistence.FILES]
            before = [path.read_bytes() for path in paths]
            (Path(directory) / "students.dat").write_bytes(b"broken")
            failed = subprocess.run(command, input="0\n", **options)
            self.assertEqual(failed.returncode, 2)
            self.assertIn("Cannot load saved data", failed.stdout)
            self.assertEqual([path.read_bytes() for path in paths], before)


if __name__ == "__main__":
    unittest.main()
