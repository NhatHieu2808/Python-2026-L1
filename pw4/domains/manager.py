from .course import Course
from .student import Student


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

