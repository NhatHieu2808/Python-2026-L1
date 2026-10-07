"""Practical work 1: student mark management using functions."""


def input_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Please enter a non-negative integer.")


def input_unique_id(prompt, used_ids):
    while True:
        item_id = input(prompt).strip()
        if not item_id:
            print("ID cannot be empty.")
        elif item_id in used_ids:
            print("ID already exists.")
        else:
            used_ids.add(item_id)
            return item_id


def validate_unique_ids(items, item_name):
    used_ids = set()
    for item in items:
        item_id = item.get("id", "")
        if not item_id:
            raise ValueError(f"{item_name} ID cannot be empty")
        if item_id in used_ids:
            raise ValueError(f"Duplicate {item_name.lower()} ID: {item_id}")
        used_ids.add(item_id)


def input_students():
    students = []
    used_ids = set()
    number_of_students = input_positive_integer("Number of students: ")
    for index in range(number_of_students):
        print(f"Student {index + 1}")
        student = {
            "id": input_unique_id("ID: ", used_ids),
            "name": input("Name: ").strip(),
            "dob": input("Date of birth: ").strip(),
        }
        students.append(student)
    return students


def input_courses():
    courses = []
    used_ids = set()
    number_of_courses = input_positive_integer("Number of courses: ")
    for index in range(number_of_courses):
        print(f"Course {index + 1}")
        course = {
            "id": input_unique_id("ID: ", used_ids),
            "name": input("Name: ").strip(),
        }
        courses.append(course)
    return courses


def find_course(courses, course_id):
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


def input_marks(students, courses, marks):
    validate_unique_ids(students, "Student")
    validate_unique_ids(courses, "Course")
    course_id = input("Course ID: ").strip()
    course = find_course(courses, course_id)
    if course is None:
        print("Course not found.")
        return

    course_marks = {}
    for student in students:
        while True:
            try:
                score = float(input(f"Mark for {student['name']}: "))
                if 0 <= score <= 10:
                    course_marks[student["id"]] = score
                    break
            except ValueError:
                pass
            print("Please enter a mark from 0 to 10.")
    marks[course_id] = course_marks


def list_courses(courses):
    print("\nCOURSES")
    print(f"{'ID':<12}{'Name'}")
    for course in courses:
        print(f"{course['id']:<12}{course['name']}")


def list_students(students):
    print("\nSTUDENTS")
    print(f"{'ID':<12}{'Name':<30}{'Date of birth'}")
    for student in students:
        print(f"{student['id']:<12}{student['name']:<30}{student['dob']}")


def show_student_marks(students, courses, marks):
    course_id = input("Course ID: ").strip()
    course = find_course(courses, course_id)
    if course is None:
        print("Course not found.")
        return

    print(f"\nMARKS FOR {course['name']}")
    print(f"{'Student ID':<12}{'Student name':<30}{'Mark'}")
    course_marks = marks.get(course_id, {})
    for student in students:
        score = course_marks.get(student["id"], "Not entered")
        print(f"{student['id']:<12}{student['name']:<30}{score}")


def main():
    students = input_students()
    courses = input_courses()
    marks = {}

    while True:
        print("\n1. List students")
        print("2. List courses")
        print("3. Input marks for a course")
        print("4. Show marks for a course")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_students(students)
        elif choice == "2":
            list_courses(courses)
        elif choice == "3":
            input_marks(students, courses, marks)
        elif choice == "4":
            show_student_marks(students, courses, marks)
        elif choice == "0":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

