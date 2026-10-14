"""Labwork 6b: visualize original course scores with Pandas."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIRECTORY = Path(__file__).resolve().parent
SCORE_FILE = OUTPUT_DIRECTORY.parent / "labwork5_pandas" / "scores.csv"
COURSES = ["math", "python", "database"]
COLORS = ["tab:blue", "tab:orange", "tab:green"]


def create_plots(scores):
    # Student order is an implementation choice, not an extra CSV field.
    plot_data = scores.copy()
    plot_data["student_number"] = range(1, len(scores) + 1)
    scatter_figure, scatter_axis = plt.subplots(figsize=(10, 5))
    for course, color in zip(COURSES, COLORS):
        # Drop only this course's missing values; preserve other observations.
        plot_data.dropna(subset=[course]).plot.scatter(
            x="student_number", y=course, ax=scatter_axis,
            color=color, label=course, alpha=0.75,
        )
    scatter_axis.set(
        title="Student scores by course", xlabel="Student order in CSV",
        ylabel="Score", xlim=(0.5, len(scores) + 0.5),
    )
    scatter_figure.tight_layout()

    histogram_figure, histogram_axes = plt.subplots(1, 3, figsize=(12, 4))
    for course, color, axis in zip(COURSES, COLORS, histogram_axes):
        scores[course].dropna().plot.hist(ax=axis, bins=10, color=color)
        axis.set(title=course, xlabel="Score", ylabel="Number of students")
    histogram_figure.suptitle("Course score distributions")
    histogram_figure.tight_layout()

    box_figure, box_axis = plt.subplots(figsize=(8, 5))
    # Pandas ignores NaN separately for each selected numeric column.
    scores[COURSES].plot.box(ax=box_axis)
    box_axis.set(title="Course score comparison", xlabel="Course", ylabel="Score")
    box_figure.tight_layout()
    return {
        "scattered.png": scatter_figure,
        "histo.png": histogram_figure,
        "box.png": box_figure,
    }


def main():
    scores = pd.read_csv(SCORE_FILE)
    print(f"Students: {len(scores)}")
    print("Missing scores (omitted separately for each course):")
    print(scores[COURSES].isna().sum().to_string())
    print("Valid scores:")
    print(scores[COURSES].count().to_string())
    for filename, figure in create_plots(scores).items():
        output = OUTPUT_DIRECTORY / filename
        figure.savefig(output, dpi=150)
        plt.close(figure)
        print(f"Saved: {output}")


if __name__ == "__main__":
    main()
