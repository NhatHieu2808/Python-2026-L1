"""Labwork 5: inspect, clean, merge, and summarize the supplied CSV files."""

from pathlib import Path

import pandas as pd


DATA_DIRECTORY = Path(__file__).resolve().parent
SCORE_COLUMNS = ["python", "math", "database"]


def analyze_students(students):
    """Analyze the original data without filling its missing values."""
    return {
        "first_five": students.head(),
        "shape": students.shape,
        "name_gpa": students[["name", "GPA"]],
        "gpa_at_least_3_5": students[students["GPA"] >= 3.5],
        "sorted_by_gpa": students.sort_values(
            "GPA", ascending=False, kind="stable"
        ),
        "average_gpa_by_major": students.groupby("major")["GPA"].mean(),
    }


def analyze_scores(students, scores):
    """Fill numeric gaps on copies, then analyze the three subject scores."""
    student_columns = ["age", "GPA"]
    student_means = students[student_columns].mean()
    score_means = scores[SCORE_COLUMNS].mean()

    clean_students = students.copy()
    clean_scores = scores.copy()
    clean_students[student_columns] = clean_students[student_columns].fillna(
        student_means
    )
    clean_scores[SCORE_COLUMNS] = clean_scores[SCORE_COLUMNS].fillna(score_means)

    merged = pd.merge(
        clean_students, clean_scores, on="student_id", validate="one_to_one"
    )
    merged["average_score"] = merged[SCORE_COLUMNS].mean(axis=1)

    return {
        "student_missing": students.isna().sum(),
        "score_missing": scores.isna().sum(),
        "student_means": student_means,
        "score_means": score_means,
        "clean_students": clean_students,
        "clean_scores": clean_scores,
        "merged": merged,
        "top_five": merged.sort_values(
            "average_score", ascending=False, kind="stable"
        ).head(5),
        "average_score_by_major": merged.groupby("major")["average_score"].mean(),
    }


def display(title, value):
    print(f"\n{title}")
    if isinstance(value, pd.DataFrame):
        print(value.to_string(index=False))
    elif isinstance(value, pd.Series):
        print(value.to_string())
    else:
        print(value)


def main():
    students = pd.read_csv(DATA_DIRECTORY / "students.csv")
    part_one = analyze_students(students)

    display("[1.1] Load students.csv", DATA_DIRECTORY / "students.csv")
    display("[1.2] First five rows", part_one["first_five"])
    rows, columns = part_one["shape"]
    display("[1.3] Dataset shape", f"Rows: {rows}; columns: {columns}")
    display("[1.4] Name and GPA", part_one["name_gpa"])
    display("[1.5] GPA >= 3.5", part_one["gpa_at_least_3_5"])
    display("[1.6] GPA in descending order", part_one["sorted_by_gpa"])
    display("[1.7] Average GPA by major", part_one["average_gpa_by_major"])
    print("Part 1 uses original data. Group means exclude missing GPA values.")

    scores = pd.read_csv(DATA_DIRECTORY / "scores.csv")
    part_two = analyze_scores(students, scores)

    display(
        "[2.1] Load students.csv and scores.csv",
        f"students.csv: {students.shape}; scores.csv: {scores.shape}",
    )
    display("[2.2] Missing values in students.csv", part_two["student_missing"])
    display("Missing values in scores.csv", part_two["score_missing"])
    display(
        "[2.3] Fill missing numeric values on copies",
        "Use each column's mean of observed values. Filled values are estimates, "
        "not original observations. Keep full precision for calculations.",
    )
    display("Student column means", part_two["student_means"])
    display("Score column means", part_two["score_means"])
    display("Missing values after cleaning students", part_two["clean_students"].isna().sum())
    display("Missing values after cleaning scores", part_two["clean_scores"].isna().sum())
    display("[2.4] Merge on student_id", part_two["merged"].drop(columns="average_score"))
    display(
        "[2.5] Average of python, math, database for each student",
        part_two["merged"][["student_id", "name", *SCORE_COLUMNS, "average_score"]],
    )
    display("[2.6] Top five students by average score", part_two["top_five"])
    display("[2.7] Average score by major", part_two["average_score_by_major"])


if __name__ == "__main__":
    main()
