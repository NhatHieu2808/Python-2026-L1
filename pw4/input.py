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


def read_score(prompt):
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 10:
                return score
        except ValueError:
            pass
        print("Please enter a score from 0 to 10.")


def input_student(manager):
    manager.add_student(
        read_non_empty("Student ID: "),
        read_non_empty("Student name: "),
        read_non_empty("Date of birth: "),
    )


def input_course(manager):
    manager.add_course(
        read_non_empty("Course ID: "),
        read_non_empty("Course name: "),
        read_positive_integer("Credits: "),
    )


def input_mark(manager):
    manager.set_mark(
        read_non_empty("Student ID: "),
        read_non_empty("Course ID: "),
        read_score("Score: "),
    )


def input_students(manager):
    number_of_students = read_positive_integer("Number of students: ")
    for index in range(number_of_students):
        print(f"Student {index + 1}")
        student_id = read_non_empty("ID: ")
        name = read_non_empty("Name: ")
        date_of_birth = read_non_empty("Date of birth: ")
        manager.add_student(student_id, name, date_of_birth)


def input_courses(manager):
    number_of_courses = read_positive_integer("Number of courses: ")
    for index in range(number_of_courses):
        print(f"Course {index + 1}")
        course_id = read_non_empty("ID: ")
        name = read_non_empty("Name: ")
        credits = read_positive_integer("Credits: ")
        manager.add_course(course_id, name, credits)


def input_marks(manager):
    for course in manager.courses.values():
        print(f"Marks for {course.name}")
        for student in manager.students.values():
            while True:
                try:
                    score = read_score(f"{student.name}: ")
                    manager.set_mark(student.student_id, course.course_id, score)
                    break
                except ValueError as error:
                    print(error)
