import argparse
import sys

try:
    import curses
except ImportError:
    curses = None

from domains import StudentMarkManager
from persistence import DEFAULT_DIRECTORY, load_data, save_archive
from input import (
    input_course,
    input_course_curses,
    input_mark,
    input_mark_curses,
    input_student,
    input_student_curses,
    read_curses_text,
    read_non_empty,
)
from output import (
    safe_addstr,
    show_course_marks,
    show_course_marks_curses,
    show_courses,
    show_courses_curses,
    show_lines_curses,
    show_students,
    show_students_curses,
)


def run_action(action, manager):
    try:
        action(manager)
        if action in (input_student, input_course, input_mark):
            print("Saved successfully.")
    except (ValueError, OSError) as error:
        print(error)


def show_marks(manager):
    show_course_marks(manager, read_non_empty("Course ID: "))


def run_menu(manager):
    actions = {
        "1": input_student,
        "2": input_course,
        "3": input_mark,
        "4": show_students,
        "5": show_courses,
        "6": show_marks,
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
            try:
                save_archive(manager)
            except (ValueError, OSError) as error:
                print(f"Could not save students.dat: {error}. Please retry.")
                continue
            print("Saved students.dat (ZIP DEFLATE).")
            print("Goodbye.")
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid option.")
        else:
            run_action(action, manager)


def run_curses_action(action, screen, manager, success_message):
    try:
        action(screen, manager)
        show_lines_curses(screen, "Success", [success_message])
    except (ValueError, OSError) as error:
        show_lines_curses(screen, "Error", [str(error)])


def run_curses_menu(screen, manager):
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
            try:
                save_archive(manager)
            except (ValueError, OSError) as error:
                show_lines_curses(screen, "Save error", [str(error), "Data remains in memory. Retry exit to save."])
                continue
            return
        if choice == ord("1"):
            run_curses_action(input_student_curses, screen, manager, "Student added.")
        elif choice == ord("2"):
            run_curses_action(input_course_curses, screen, manager, "Course added.")
        elif choice == ord("3"):
            run_curses_action(input_mark_curses, screen, manager, "Mark saved.")
        elif choice == ord("4"):
            show_students_curses(screen, manager)
        elif choice == ord("5"):
            show_courses_curses(screen, manager)
        elif choice == ord("6"):
            course_id = read_curses_text(screen, "Course ID")
            try:
                show_course_marks_curses(screen, manager, course_id)
            except ValueError as error:
                show_lines_curses(screen, "Error", [str(error)])
        else:
            show_lines_curses(screen, "Input error", ["Invalid option."])


def main(data_directory=DEFAULT_DIRECTORY):
    try:
        manager = load_data(data_directory)
    except (ValueError, OSError, UnicodeError) as error:
        print(f"Cannot load saved data: {error}")
        print("Startup stopped. Repair or restore the saved data before continuing.")
        return 2
    if curses is not None and sys.stdin.isatty() and sys.stdout.isatty():
        curses.wrapper(run_curses_menu, manager)
    else:
        run_menu(manager)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Practical work 5: persistent student marks")
    parser.add_argument("--data-dir", default=DEFAULT_DIRECTORY, help="Directory for the three text files and students.dat")
    sys.exit(main(parser.parse_args().data_dir))
