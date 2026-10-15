"""Labwork 7: the functions of labwork1b.py implemented with OOP."""

import math


def read_count(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Please enter a non-negative integer.")


def read_unique_id(prompt, existing):
    while True:
        item_id = input(prompt).strip()
        if not item_id:
            print("ID cannot be empty.")
        elif item_id in existing:
            print("ID already exists.")
        else:
            return item_id


class NamedRecord:
    """Common identity and name; IDs stay fixed after registration."""

    def __init__(self, item_id, name=""):
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError("ID must be a non-empty string")
        self.__id = item_id.strip()
        self.set_name(name)

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        self.__name = name.strip()

    def input(self):
        self.set_name(input("Name: "))

    def list(self):
        print(f"{self.get_id():<12}{self.get_name()}")


class Course(NamedRecord):
    """A course uses the common input and listing methods."""


class Student(NamedRecord):
    def __init__(self, student_id, name="", date_of_birth=""):
        super().__init__(student_id, name)
        self.set_date_of_birth(date_of_birth)

    def get_date_of_birth(self):
        return self.__date_of_birth

    def set_date_of_birth(self, date_of_birth):
        if not isinstance(date_of_birth, str):
            raise ValueError("Date of birth must be a string")
        self.__date_of_birth = date_of_birth.strip()

    def input(self):
        super().input()
        self.set_date_of_birth(input("Date of birth: "))

    def list(self):
        print(f"{self.get_id():<12}{self.get_name():<30}{self.get_date_of_birth()}")


class StudentMarkManager:
    def __init__(self):
        self.__students = {}
        self.__courses = {}
        self.__marks = {}

    def add_student(self, student):
        if not isinstance(student, Student):
            raise ValueError("Expected a Student")
        if student.get_id() in self.__students:
            raise ValueError("Student ID already exists")
        self.__students[student.get_id()] = student

    def add_course(self, course):
        if not isinstance(course, Course):
            raise ValueError("Expected a Course")
        if course.get_id() in self.__courses:
            raise ValueError("Course ID already exists")
        self.__courses[course.get_id()] = course

    def get_students(self):
        return tuple(self.__students.values())

    def get_courses(self):
        return tuple(self.__courses.values())

    def get_course(self, course_id):
        return self.__courses.get(course_id)

    def _check_references(self, student_id, course_id):
        if student_id not in self.__students:
            raise ValueError("Student not found")
        if course_id not in self.__courses:
            raise ValueError("Course not found")

    def set_mark(self, student_id, course_id, score):
        self._check_references(student_id, course_id)
        score = float(score)
        if not math.isfinite(score) or not 0 <= score <= 10:
            raise ValueError("A mark must be finite and from 0 to 10")
        self.__marks[(student_id, course_id)] = score

    def get_mark(self, student_id, course_id):
        self._check_references(student_id, course_id)
        return self.__marks.get((student_id, course_id))

    def input(self):
        for record_type, existing, add_record, label in (
            (Student, self.__students, self.add_student, "students"),
            (Course, self.__courses, self.add_course, "courses"),
        ):
            count = read_count(f"Number of {label}: ")
            for index in range(count):
                print(f"{record_type.__name__} {index + 1}")
                record = record_type(read_unique_id("ID: ", existing))
                record.input()  # Dispatch to Student's override or Course's inherited method.
                add_record(record)

    def _list_records(self, records, title, header):
        print(f"\n{title}")
        print(header)
        for record in records:
            record.list()  # The same call produces the row for the actual record type.

    def list_students(self):
        self._list_records(
            self.get_students(), "STUDENTS",
            f"{'ID':<12}{'Name':<30}{'Date of birth'}",
        )

    def list_courses(self):
        self._list_records(self.get_courses(), "COURSES", f"{'ID':<12}{'Name'}")

    def input_marks(self):
        course_id = input("Course ID: ").strip()
        if self.get_course(course_id) is None:
            print("Course not found.")
            return
        for student in self.get_students():
            while True:
                try:
                    score = float(input(f"Mark for {student.get_name()}: "))
                    self.set_mark(student.get_id(), course_id, score)
                    break
                except ValueError:
                    print("Please enter a mark from 0 to 10.")

    def show_marks(self):
        course_id = input("Course ID: ").strip()
        course = self.get_course(course_id)
        if course is None:
            print("Course not found.")
            return
        print(f"\nMARKS FOR {course.get_name()}")
        print(f"{'Student ID':<12}{'Student name':<30}{'Mark'}")
        for student in self.get_students():
            score = self.get_mark(student.get_id(), course_id)
            displayed_score = "Not entered" if score is None else score
            print(f"{student.get_id():<12}{student.get_name():<30}{displayed_score}")

    def run(self):
        while True:
            print("\n1. List students")
            print("2. List courses")
            print("3. Input marks for a course")
            print("4. Show marks for a course")
            print("0. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.list_students()
            elif choice == "2":
                self.list_courses()
            elif choice == "3":
                self.input_marks()
            elif choice == "4":
                self.show_marks()
            elif choice == "0":
                return
            else:
                print("Invalid option.")


def main():
    manager = StudentMarkManager()
    manager.input()
    manager.run()


if __name__ == "__main__":
    main()
