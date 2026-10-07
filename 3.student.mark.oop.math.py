"""Practical work 3: OOP student marks, maths, NumPy, and curses."""

import math
import sys

import numpy as np

try:
    import curses
except ImportError:
    curses = None


class Course:
    def __init__(self, course_id, name, credits):
        self.course_id = course_id
        self.name = name
        self.credits = credits


class Student:
    def __init__(self, student_id, name, date_of_birth):
        self.student_id = student_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.marks = {}

    def set_mark(self, course_id, score):
        if not 0 <= score <= 10 or not math.isfinite(score):
            raise ValueError("A score must be from 0 to 10")
        self.marks[course_id] = math.floor(score * 10) / 10

    def calculate_gpa(self, courses):
        scores = []
        credits = []
        for course_id, score in self.marks.items():
            if course_id in courses:
                scores.append(score)
                credits.append(courses[course_id].credits)

        if not credits:
            return 0.0

        score_array = np.array(scores, dtype=float)
        credit_array = np.array(credits, dtype=float)
        return float(np.sum(score_array * credit_array) / np.sum(credit_array))


class StudentMarkManager:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self, student_id, name, date_of_birth):
        student_id = student_id.strip()
        if not student_id:
            raise ValueError("Student ID cannot be empty")
        if student_id in self.students:
            raise ValueError("Student ID already exists")
        self.students[student_id] = Student(student_id, name, date_of_birth)

    def add_course(self, course_id, name, credits):
        course_id = course_id.strip()
        if not course_id:
            raise ValueError("Course ID cannot be empty")
        if course_id in self.courses:
            raise ValueError("Course ID already exists")
        if type(credits) is not int or credits <= 0:
            raise ValueError("Credits must be a positive integer")
        self.courses[course_id] = Course(course_id, name, credits)

    def set_mark(self, student_id, course_id, score):
        if student_id not in self.students:
            raise ValueError("Student not found")
        if course_id not in self.courses:
            raise ValueError("Course not found")
        self.students[student_id].set_mark(course_id, score)

    def students_by_gpa(self):
        return sorted(
            self.students.values(),
            key=lambda student: student.calculate_gpa(self.courses),
            reverse=True,
        )


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This value cannot be empty.")


def read_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a positive integer.")


def read_unique_id(prompt, existing):
    while True:
        value = read_non_empty(prompt)
        if value not in existing:
            return value
        print("ID already exists. Enter another ID.")


def read_score(prompt):
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 10:
                return score
        except ValueError:
            pass
        print("Please enter a score from 0 to 10.")


def format_student_table(manager):
    lines = [f"{'ID':<10}{'Name':<25}{'DoB':<14}{'GPA':>5}"]
    for student in manager.students_by_gpa():
        gpa = student.calculate_gpa(manager.courses)
        lines.append(
            f"{student.student_id:<10}{student.name:<25}"
            f"{student.date_of_birth:<14}{gpa:>5.2f}"
        )
    return lines


def safe_addstr(screen, row, column, text, attribute=0):
    height, width = screen.getmaxyx()
    if row < 0 or row >= height or column < 0 or column >= width:
        return
    maximum_length = max(0, width - column - 1)
    if maximum_length == 0:
        return
    if attribute:
        screen.addnstr(row, column, str(text), maximum_length, attribute)
    else:
        screen.addnstr(row, column, str(text), maximum_length)


def show_lines_curses(screen, title, lines):
    page = 0
    horizontal_offset = 0
    display_lines = list(lines) or ["No data available."]
    while True:
        height, width = screen.getmaxyx()
        page_size = max(1, height - 4)
        page_count = max(1, (len(display_lines) + page_size - 1) // page_size)
        page = min(page, page_count - 1)
        start = page * page_size
        visible_width = max(1, width - 1)
        maximum_offset = max(0, max(len(line) for line in display_lines) - visible_width)
        horizontal_offset = min(horizontal_offset, maximum_offset)

        screen.clear()
        safe_addstr(screen, 0, 0, title, curses.A_BOLD)
        for row, line in enumerate(display_lines[start : start + page_size], start=2):
            safe_addstr(screen, row, 0, line[horizontal_offset:])

        if page_count == 1:
            footer = "Left/Right: scroll; q/Enter: back"
        else:
            footer = f"{page + 1}/{page_count} Up/Down; Left/Right; q back"
        safe_addstr(screen, height - 1, 0, footer)
        screen.refresh()
        key = screen.getch()
        if key in (10, 13, 27, ord("q"), ord("Q")):
            return
        if key in (curses.KEY_DOWN, curses.KEY_NPAGE, ord("n")) and page < page_count - 1:
            page += 1
        elif key in (curses.KEY_UP, curses.KEY_PPAGE, ord("p")) and page > 0:
            page -= 1
        elif key in (curses.KEY_RIGHT, ord("l")):
            horizontal_offset = min(maximum_offset, horizontal_offset + max(1, visible_width // 2))
        elif key in (curses.KEY_LEFT, ord("h")):
            horizontal_offset = max(0, horizontal_offset - max(1, visible_width // 2))


def read_curses_text(screen, prompt):
    while True:
        height, width = screen.getmaxyx()
        screen.clear()
        if height < 4 or width < 12:
            safe_addstr(screen, 0, 0, "Resize terminal to at least 4x12")
            screen.refresh()
            screen.getch()
            continue
        safe_addstr(screen, 0, 0, prompt, curses.A_BOLD)
        safe_addstr(screen, 2, 0, "Input: ")
        screen.refresh()
        curses.echo()
        curses.curs_set(1)
        try:
            raw_value = screen.getstr(2, 7, width - 8)
        finally:
            curses.noecho()
            curses.curs_set(0)
        value = raw_value.decode("utf-8", errors="replace").strip()
        if value:
            return value
        show_lines_curses(screen, "Input error", ["This value cannot be empty."])


def read_curses_unique_id(screen, prompt, existing):
    while True:
        value = read_curses_text(screen, prompt)
        if value not in existing:
            return value
        show_lines_curses(screen, "Input error", ["ID already exists. Enter another ID."])


def read_curses_positive_integer(screen, prompt):
    while True:
        value = read_curses_text(screen, prompt)
        try:
            number = int(value)
            if number > 0:
                return number
        except ValueError:
            pass
        show_lines_curses(screen, "Input error", ["Please enter a positive integer."])


def read_curses_score(screen, prompt):
    while True:
        value = read_curses_text(screen, prompt)
        try:
            score = float(value)
            if 0 <= score <= 10:
                return score
        except ValueError:
            pass
        show_lines_curses(screen, "Input error", ["Please enter a score from 0 to 10."])


def format_course_table(manager):
    lines = [f"{'ID':<10}{'Course name':<30}{'Credits':>7}"]
    for course in manager.courses.values():
        lines.append(f"{course.course_id:<10}{course.name:<30}{course.credits:>7}")
    return lines


def format_course_marks(manager, course_id):
    course = manager.courses.get(course_id)
    if course is None:
        raise ValueError("Course not found")
    lines = [f"Marks for {course.name}"]
    for student in manager.students.values():
        score = student.marks.get(course_id)
        shown_score = "Not entered" if score is None else f"{score:.1f}"
        lines.append(f"{student.student_id:<10}{student.name:<25}{shown_score}")
    return lines


def add_student_curses(screen, manager):
    try:
        manager.add_student(
            read_curses_unique_id(screen, "Student ID", manager.students),
            read_curses_text(screen, "Student name"),
            read_curses_text(screen, "Date of birth"),
        )
        show_lines_curses(screen, "Success", ["Student added."])
    except ValueError as error:
        show_lines_curses(screen, "Error", [str(error)])


def add_course_curses(screen, manager):
    try:
        manager.add_course(
            read_curses_unique_id(screen, "Course ID", manager.courses),
            read_curses_text(screen, "Course name"),
            read_curses_positive_integer(screen, "Credits"),
        )
        show_lines_curses(screen, "Success", ["Course added."])
    except ValueError as error:
        show_lines_curses(screen, "Error", [str(error)])


def enter_mark_curses(screen, manager):
    try:
        manager.set_mark(
            read_curses_text(screen, "Student ID"),
            read_curses_text(screen, "Course ID"),
            read_curses_score(screen, "Score"),
        )
        show_lines_curses(
            screen, "Success", ["Mark saved and rounded down to one decimal place."]
        )
    except ValueError as error:
        show_lines_curses(screen, "Error", [str(error)])


def curses_interface(screen, manager):
    curses.curs_set(0)
    menu_lines = [
        "1. Add student",
        "2. Add course",
        "3. Enter mark",
        "4. List students by GPA",
        "5. List courses",
        "6. Show marks for a course",
        "0. Exit",
    ]
    while True:
        screen.clear()
        safe_addstr(screen, 0, 0, "STUDENT MARK MANAGEMENT", curses.A_BOLD)
        for row, line in enumerate(menu_lines, start=2):
            safe_addstr(screen, row, 0, line)
        safe_addstr(screen, min(len(menu_lines) + 3, screen.getmaxyx()[0] - 1), 0, "Choice: ")
        screen.refresh()
        choice = screen.getch()
        if choice == ord("0"):
            return
        if choice == ord("1"):
            add_student_curses(screen, manager)
        elif choice == ord("2"):
            add_course_curses(screen, manager)
        elif choice == ord("3"):
            enter_mark_curses(screen, manager)
        elif choice == ord("4"):
            show_lines_curses(screen, "Students by GPA", format_student_table(manager))
        elif choice == ord("5"):
            show_lines_curses(screen, "Courses", format_course_table(manager))
        elif choice == ord("6"):
            course_id = read_curses_text(screen, "Course ID")
            try:
                show_lines_curses(
                    screen, "Course marks", format_course_marks(manager, course_id)
                )
            except ValueError as error:
                show_lines_curses(screen, "Error", [str(error)])
        else:
            show_lines_curses(screen, "Input error", ["Invalid option."])


def plain_interface(manager):
    print("STUDENT MARK MANAGEMENT")
    print("Students sorted by GPA (descending)")
    for line in format_student_table(manager):
        print(line)


def list_courses(manager):
    if not manager.courses:
        print("No courses have been added.")
        return
    print(f"{'ID':<10}{'Course name':<30}{'Credits':>7}")
    for course in manager.courses.values():
        print(f"{course.course_id:<10}{course.name:<30}{course.credits:>7}")


def show_course_marks(manager):
    if not manager.courses or not manager.students:
        print("Add at least one course and one student first.")
        return
    course_id = read_non_empty("Course ID: ")
    course = manager.courses.get(course_id)
    if course is None:
        print("Course not found.")
        return
    print(f"Marks for {course.name}")
    for student in manager.students.values():
        score = student.marks.get(course_id)
        shown_score = "Not entered" if score is None else f"{score:.1f}"
        print(f"{student.student_id:<10}{student.name:<25}{shown_score}")


def add_student_from_input(manager):
    try:
        manager.add_student(
            read_unique_id("Student ID: ", manager.students),
            read_non_empty("Student name: "),
            read_non_empty("Date of birth: "),
        )
        print("Student added.")
    except ValueError as error:
        print(error)


def add_course_from_input(manager):
    try:
        manager.add_course(
            read_unique_id("Course ID: ", manager.courses),
            read_non_empty("Course name: "),
            read_positive_integer("Credits: "),
        )
        print("Course added.")
    except ValueError as error:
        print(error)


def enter_mark_from_input(manager):
    try:
        manager.set_mark(
            read_non_empty("Student ID: "),
            read_non_empty("Course ID: "),
            read_score("Score: "),
        )
        print("Mark saved and rounded down to one decimal place.")
    except ValueError as error:
        print(error)


def show_student_report(manager):
    if not manager.students:
        print("No students have been added.")
        return
    plain_interface(manager)


def run_menu(manager):
    actions = {
        "1": add_student_from_input,
        "2": add_course_from_input,
        "3": enter_mark_from_input,
        "4": show_student_report,
        "5": list_courses,
        "6": show_course_marks,
    }
    while True:
        print("\nSTUDENT MARK MANAGEMENT")
        print("1. Add student")
        print("2. Add course")
        print("3. Enter mark")
        print("4. List students by GPA")
        print("5. List courses")
        print("6. Show marks for a course")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid option.")
        else:
            action(manager)


def main():
    manager = StudentMarkManager()
    if curses is not None and sys.stdin.isatty() and sys.stdout.isatty():
        curses.wrapper(curses_interface, manager)
    else:
        run_menu(manager)


if __name__ == "__main__":
    main()
