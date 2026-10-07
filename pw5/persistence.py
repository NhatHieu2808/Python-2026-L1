"""UTF-8 JSON text files and a DEFLATE ZIP archive for Practical work 5."""

import json
import math
import os
from pathlib import Path
import tempfile
import zipfile
import zlib

from domains import StudentMarkManager


FILES = ("students.txt", "courses.txt", "marks.txt")
DEFAULT_DIRECTORY = Path(__file__).resolve().parent


def records_from_manager(manager):
    students = [
        {"id": student.student_id, "name": student.name, "dob": student.date_of_birth}
        for student in manager.students.values()
    ]
    courses = [
        {"id": course.course_id, "name": course.name, "credits": course.credits}
        for course in manager.courses.values()
    ]
    marks = [
        {"student_id": student.student_id, "course_id": course_id, "score": score}
        for student in manager.students.values()
        for course_id, score in student.marks.items()
    ]
    return dict(zip(FILES, (students, courses, marks)))


def require_text(record, key):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or invalid text field: {key}")
    return value.strip()


def manager_from_records(records):
    manager = StudentMarkManager()
    for filename in FILES:
        if not isinstance(records[filename], list):
            raise ValueError(f"{filename} must contain a JSON list")
        if any(not isinstance(row, dict) for row in records[filename]):
            raise ValueError(f"{filename} contains an invalid record")
    for row in records["students.txt"]:
        manager.add_student(
            require_text(row, "id"), require_text(row, "name"), require_text(row, "dob")
        )
    for row in records["courses.txt"]:
        manager.add_course(require_text(row, "id"), require_text(row, "name"), row.get("credits"))
    seen_marks = set()
    for row in records["marks.txt"]:
        student_id = require_text(row, "student_id")
        course_id = require_text(row, "course_id")
        score = row.get("score")
        if type(score) not in (int, float) or not 0 <= score <= 10 or not math.isfinite(score):
            raise ValueError("A stored score must be a finite number from 0 to 10")
        pair = (student_id, course_id)
        if pair in seen_marks:
            raise ValueError("Duplicate student/course mark")
        seen_marks.add(pair)
        manager.set_mark(student_id, course_id, score)
    return manager


def encode_records(manager):
    records = records_from_manager(manager)
    manager_from_records(records)
    return {
        name: json.dumps(rows, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
        for name, rows in records.items()
    }


def write_text_files(contents, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    temporary_paths = []
    try:
        # Finish writing every temporary file before replacing an existing file.
        for name in FILES:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="\n", dir=directory,
                prefix=name + ".", suffix=".tmp", delete=False,
            ) as stream:
                temporary_paths.append((Path(stream.name), directory / name))
                stream.write(contents[name])
        for temporary_path, destination in temporary_paths:
            os.replace(temporary_path, destination)
    finally:
        for temporary_path, _ in temporary_paths:
            if temporary_path.exists():
                temporary_path.unlink()


def save_text_files(manager, directory=None):
    if directory is None:
        directory = getattr(manager, "data_directory", DEFAULT_DIRECTORY)
    write_text_files(encode_records(manager), directory)


def save_archive(manager, directory=None):
    if directory is None:
        directory = getattr(manager, "data_directory", DEFAULT_DIRECTORY)
    directory = Path(directory)
    contents = encode_records(manager)
    write_text_files(contents, directory)
    with tempfile.NamedTemporaryFile(dir=directory, suffix=".tmp", delete=False) as stream:
        temporary_path = Path(stream.name)
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in FILES:
                archive.writestr(name, contents[name].encode("utf-8"))
        os.replace(temporary_path, directory / "students.dat")
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def load_data(directory=DEFAULT_DIRECTORY):
    directory = Path(directory)
    archive_path = directory / "students.dat"
    if archive_path.exists():
        try:
            with zipfile.ZipFile(archive_path, "r") as archive:
                names = archive.namelist()
                if len(names) != len(FILES) or set(names) != set(FILES):
                    raise ValueError("students.dat must contain exactly the three required text files")
                contents = {name: archive.read(name).decode("utf-8") for name in FILES}
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, zlib.error) as error:
            raise ValueError(f"Cannot decompress students.dat: {error}") from error
    else:
        present = [(directory / name).exists() for name in FILES]
        if not any(present):
            manager = StudentMarkManager()
            manager.data_directory = directory
            return manager
        if not all(present):
            raise ValueError("Incomplete text files. Restore all three files before continuing.")
        contents = {}
        for name in FILES:
            with open(directory / name, "r", encoding="utf-8") as stream:
                contents[name] = stream.read()

    # Validate all files and references before changing any local data file.
    records = {name: json.loads(contents[name]) for name in FILES}
    manager = manager_from_records(records)
    manager.data_directory = directory
    if archive_path.exists():
        write_text_files(contents, directory)
    return manager
