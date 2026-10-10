"""Labwork 5a: a pickle round-trip, CSV exports, and a student query."""

import argparse
import json
import os
from pathlib import Path
import pickle
import re
import tempfile

import pandas as pd

from persistence import (
    DEFAULT_DIRECTORY,
    load_data,
    manager_from_records,
    records_from_manager,
)


CSV_COLUMNS = {
    "students": ("id", "name", "dob"),
    "courses": ("id", "name", "credits"),
    "marks": ("student_id", "course_id", "score"),
}
CSV_DTYPES = {
    "students": {"id": str, "name": str, "dob": str},
    "courses": {"id": str, "name": str, "credits": int},
    "marks": {"student_id": str, "course_id": str, "score": float},
}
CONDITION_PATTERN = re.compile(
    r'\s*(?P<column>[A-Za-z_]\w*)\s*(?:==|=)\s*'
    r'(?P<value>"(?:\\.|[^"\\])*")\s*'
)


def export_csv(manager, data_directory):
    """Export PW5 records separately from the teacher's analysis datasets."""
    records = records_from_manager(manager)
    manager_from_records(records)
    directory = Path(data_directory) / "exports"
    directory.mkdir(parents=True, exist_ok=True)
    for name, columns in CSV_COLUMNS.items():
        frame = pd.DataFrame(records[name + ".txt"], columns=columns)
        frame.to_csv(directory / (name + ".csv"), index=False, encoding="utf-8")
    return directory


def load_csv_frames(directory):
    """Read all three exports and validate their records and references."""
    directory = Path(directory)
    frames = {}
    for name, columns in CSV_COLUMNS.items():
        frame = pd.read_csv(
            directory / (name + ".csv"),
            dtype=CSV_DTYPES[name],
            keep_default_na=False,
        )
        if list(frame.columns) != list(columns):
            raise ValueError(f"{name}.csv must have columns: {', '.join(columns)}")
        frames[name] = frame
    manager_from_records({
        name + ".txt": frame.to_dict(orient="records")
        for name, frame in frames.items()
    })
    return frames


def pickle_round_trip(manager, directory):
    """Load only the bytes just dumped to our own open temporary file."""
    records = records_from_manager(manager)
    manager_from_records(records)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w+b", dir=directory, prefix="snapshot.", suffix=".tmp", delete=False,
    ) as stream:
        temporary_path = Path(stream.name)
        try:
            pickle.dump(records, stream)
            stream.flush()
            stream.seek(0)
            restored_records = pickle.load(stream)
            restored = manager_from_records(restored_records)
            if records_from_manager(restored) != records:
                raise ValueError("Pickle round-trip changed the PW5 records")
        except BaseException:
            stream.close()
            temporary_path.unlink()
            raise
    try:
        os.replace(temporary_path, directory / "snapshot.pkl")
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    return restored


def query_students(students, condition):
    """Filter one string column by equality without evaluating user code."""
    match = CONDITION_PATTERN.fullmatch(condition)
    if match is None:
        raise ValueError('Use one condition such as name = "Mr. Volunteers"')
    column = match.group("column")
    if column not in CSV_COLUMNS["students"] or column not in students.columns:
        raise ValueError("Student query columns are: id, name, dob")
    try:
        value = json.loads(match.group("value"))
    except json.JSONDecodeError as error:
        raise ValueError("Use a double-quoted value with valid JSON escapes") from error
    return students[students[column] == value].copy()


def main(data_directory=DEFAULT_DIRECTORY):
    try:
        manager = load_data(data_directory)
        directory = export_csv(manager, data_directory)
        pickle_round_trip(manager, directory)
        frames = load_csv_frames(directory)
        print(f"CSV exports: {directory}")
        print(f"Pickle round-trip: PASS; snapshot: {directory / 'snapshot.pkl'}")
        print("DataFrame rows: " + "; ".join(
            f"{name}={len(frame)}" for name, frame in frames.items()
        ))
        try:
            condition = input('Student condition, e.g. name = "Mr. Volunteers": ')
        except EOFError:
            condition = ""
        if not condition.strip():
            print("No condition entered. Query skipped.")
            return 0
        result = query_students(frames["students"], condition)
        if result.empty:
            print("No students matched.")
        else:
            print(result.to_string(index=False))
        return 0
    except (OSError, ValueError) as error:
        print(f"Cannot run Labwork 5a: {error}")
        return 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", default=DEFAULT_DIRECTORY,
        help="PW5 data directory containing students.dat or the three text files",
    )
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.data_dir))
