"""Check the assigned curve, original score plots, and both standalone CLIs."""

import csv
import hashlib
import importlib.util
import math
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import unittest

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def load_script(name, directory):
    spec = importlib.util.spec_from_file_location(name, ROOT / directory / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LAB6A = load_script("lab6a", "labwork6_matplotlib")
LAB6B = load_script("lab6b", "labwork6_pandas_plot")


class Labwork6Tests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_assigned_curve_and_labels(self):
        figure = LAB6A.create_plot()
        self.assertEqual(len(figure.axes), 1)
        axis = figure.axes[0]
        x, y = axis.lines[0].get_data()
        self.assertEqual((x[0], x[-1]), (-5, 5))
        self.assertTrue(np.all(np.diff(x) > 0))
        self.assertGreaterEqual(len(x), 500)
        expected = [2 * value + math.sin(value) ** 2 + 3 for value in x]
        np.testing.assert_allclose(y, expected)
        self.assertEqual(y[np.where(x == 0)[0][0]], 3)
        self.assertEqual(axis.get_title(), "hello, po!")
        self.assertEqual((axis.get_xlabel(), axis.get_ylabel()), ("x", "y"))
        self.assertEqual(axis.get_xlim(), (-5, 5))
        self.assertTrue(all(line.get_visible() for line in axis.get_xgridlines()))
        self.assertTrue(all(line.get_visible() for line in axis.get_ygridlines()))

    def test_original_scores_and_plot_contents(self):
        scores = pd.read_csv(LAB6B.SCORE_FILE)
        original = scores.copy(deep=True)
        with LAB6B.SCORE_FILE.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        expected = {
            course: [(number, float(row[course]))
                     for number, row in enumerate(rows, 1) if row[course] != ""]
            for course in LAB6B.COURSES
        }
        self.assertEqual(len(rows), 30)
        self.assertEqual({course: len(values) for course, values in expected.items()},
                         {"math": 28, "python": 30, "database": 29})
        self.assertEqual(scores[LAB6B.COURSES].isna().sum().to_dict(),
                         {"math": 2, "python": 0, "database": 1})
        plots = LAB6B.create_plots(scores)
        pd.testing.assert_frame_equal(scores, original)

        scatter = plots["scattered.png"].axes[0]
        self.assertEqual(len(scatter.collections), 3)
        self.assertEqual([text.get_text() for text in scatter.get_legend().texts],
                         LAB6B.COURSES)
        for course, collection in zip(LAB6B.COURSES, scatter.collections):
            np.testing.assert_allclose(collection.get_offsets(), expected[course])

        histogram_axes = plots["histo.png"].axes
        self.assertEqual(len(histogram_axes), 3)
        for course, axis in zip(LAB6B.COURSES, histogram_axes):
            values = [value for _, value in expected[course]]
            counts, _ = np.histogram(values, bins=10)
            np.testing.assert_array_equal([bar.get_height() for bar in axis.patches], counts)
            self.assertEqual(sum(bar.get_height() for bar in axis.patches), len(values))
            self.assertEqual(axis.get_title(), course)

        self.assertEqual(len(plots["box.png"].axes), 1)
        box = plots["box.png"].axes[0]
        self.assertEqual([label.get_text() for label in box.get_xticklabels()],
                         LAB6B.COURSES)
        self.assertEqual(len(box.lines), 21)  # Box, whiskers, caps, median, and fliers.
        for index, course in enumerate(LAB6B.COURSES):
            values = [value for _, value in expected[course]]
            q1, q3 = np.percentile(values, [25, 75])
            np.testing.assert_allclose(box.lines[index * 7 + 1].get_ydata()[0], q1)
            np.testing.assert_allclose(box.lines[index * 7 + 2].get_ydata()[0], q3)
            np.testing.assert_allclose(box.lines[index * 7 + 5].get_ydata(),
                                       statistics.median(values))

    def test_standalone_scripts_from_another_directory(self):
        before = hashlib.sha256(LAB6B.SCORE_FILE.read_bytes()).hexdigest()
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        environment["MPLBACKEND"] = "Agg"
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as working_directory:
            for directory in ("labwork6_matplotlib", "labwork6_pandas_plot"):
                result = subprocess.run(
                    [sys.executable, "-B", str(ROOT / directory / "main.py")],
                    cwd=working_directory, env=environment,
                    capture_output=True, text=True, encoding="utf-8", timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                print(result.stdout.strip())
            self.assertEqual(list(Path(working_directory).iterdir()), [])
        self.assertTrue((LAB6A.OUTPUT_DIRECTORY / "po.pdf").read_bytes().startswith(b"%PDF-"))
        for filename in ("scattered.png", "histo.png", "box.png"):
            with Image.open(LAB6B.OUTPUT_DIRECTORY / filename) as picture:
                self.assertEqual(picture.format, "PNG")
                self.assertGreaterEqual(picture.width, 1000)
                picture.verify()
        self.assertEqual(hashlib.sha256(LAB6B.SCORE_FILE.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
