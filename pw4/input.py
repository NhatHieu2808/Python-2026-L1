def read_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a positive integer.")


def input_students(manager):
    number_of_students = read_positive_integer("Number of students: ")
    for index in range(number_of_students):
        print(f"Student {index + 1}")
        student_id = input("ID: ").strip()
        name = input("Name: ").strip()
        date_of_birth = input("Date of birth: ").strip()
        manager.add_student(student_id, name, date_of_birth)


def input_courses(manager):
    number_of_courses = read_positive_integer("Number of courses: ")
    for index in range(number_of_courses):
        print(f"Course {index + 1}")
        course_id = input("ID: ").strip()
        name = input("Name: ").strip()
        credits = read_positive_integer("Credits: ")
        manager.add_course(course_id, name, credits)


def input_marks(manager):
    for course in manager.courses.values():
        print(f"Marks for {course.name}")
        for student in manager.students.values():
            while True:
                try:
                    score = float(input(f"{student.name}: "))
                    manager.set_mark(student.student_id, course.course_id, score)
                    break
                except ValueError as error:
                    print(error)

