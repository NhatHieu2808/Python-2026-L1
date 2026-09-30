from domains import StudentMarkManager
from input import input_courses, input_marks, input_students
from output import show_students


def main():
    manager = StudentMarkManager()
    input_students(manager)
    input_courses(manager)
    input_marks(manager)
    show_students(manager)


if __name__ == "__main__":
    main()

