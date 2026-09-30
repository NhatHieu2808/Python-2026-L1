"""Practical work 3: OOP student marks, maths, NumPy, and curses."""

import math

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
        if score < 0 or score > 10:
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
        if student_id in self.students:
            raise ValueError("Student ID already exists")
        self.students[student_id] = Student(student_id, name, date_of_birth)

    def add_course(self, course_id, name, credits):
        if course_id in self.courses:
            raise ValueError("Course ID already exists")
        if credits <= 0:
            raise ValueError("Credits must be positive")
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


def add_sample_data(manager):
    manager.add_course("PY101", "Python Programming", 3)
    manager.add_course("MA101", "Mathematics", 2)
    manager.add_student("S001", "Alice Nguyen", "2006-01-12")
    manager.add_student("S002", "Bob Tran", "2006-05-20")
    manager.set_mark("S001", "PY101", 8.76)
    manager.set_mark("S001", "MA101", 7.94)
    manager.set_mark("S002", "PY101", 9.28)
    manager.set_mark("S002", "MA101", 8.49)


def format_student_table(manager):
    lines = [f"{'ID':<10}{'Name':<25}{'DoB':<14}{'GPA':>5}"]
    for student in manager.students_by_gpa():
        gpa = student.calculate_gpa(manager.courses)
        lines.append(
            f"{student.student_id:<10}{student.name:<25}"
            f"{student.date_of_birth:<14}{gpa:>5.2f}"
        )
    return lines


def curses_interface(screen, manager):
    curses.curs_set(0)
    screen.clear()
    screen.addstr(1, 2, "STUDENT MARK MANAGEMENT", curses.A_BOLD)
    screen.addstr(3, 2, "Students sorted by GPA (descending)")
    for row, line in enumerate(format_student_table(manager), start=5):
        screen.addstr(row, 2, line)
    screen.addstr(5 + len(manager.students) + 2, 2, "Press any key to exit.")
    screen.refresh()
    screen.getch()


def plain_interface(manager):
    print("STUDENT MARK MANAGEMENT")
    print("Students sorted by GPA (descending)")
    for line in format_student_table(manager):
        print(line)


def main():
    manager = StudentMarkManager()
    add_sample_data(manager)
    if curses is None:
        plain_interface(manager)
    else:
        curses.wrapper(curses_interface, manager)


if __name__ == "__main__":
    main()

