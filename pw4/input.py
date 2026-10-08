import unicodedata

try:
    import curses
except ImportError:
    curses = None

from output import show_lines_curses


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


def input_student(manager):
    manager.add_student(
        read_unique_id("Student ID: ", manager.students),
        read_non_empty("Student name: "),
        read_non_empty("Date of birth: "),
    )


def input_course(manager):
    manager.add_course(
        read_unique_id("Course ID: ", manager.courses),
        read_non_empty("Course name: "),
        read_positive_integer("Credits: "),
    )


def input_mark(manager):
    manager.set_mark(
        read_non_empty("Student ID: "),
        read_non_empty("Course ID: "),
        read_score("Score: "),
    )


def read_curses_text(screen, prompt):
    characters = []
    input_error = False
    screen.keypad(True)
    curses.noecho()
    try:
        while True:
            height, width = screen.getmaxyx()
            screen.clear()
            if height < 4 or width < 12:
                curses.curs_set(0)
                if height > 0 and width > 1:
                    screen.addnstr(0, 0, "Resize terminal to at least 4x12", width - 1)
                screen.refresh()
                screen.get_wch()
                continue

            curses.curs_set(1)
            screen.addnstr(0, 0, prompt, width - 1, curses.A_BOLD)
            screen.addnstr(2, 0, "Input: ", width - 1)
            # Scroll the visible suffix by terminal columns, not UTF-8 bytes.
            visible_text = ""
            visible_columns = 0
            for character in reversed(characters):
                size = 0 if unicodedata.combining(character) else (
                    2 if unicodedata.east_asian_width(character) in ("W", "F") else 1
                )
                if visible_columns + size > width - 8:
                    break
                visible_text = character + visible_text
                visible_columns += size
            while visible_text and unicodedata.combining(visible_text[0]):
                visible_text = visible_text[1:]
            if visible_text:
                screen.addnstr(2, 7, visible_text, len(visible_text))
            if input_error:
                screen.addnstr(3, 0, "This value cannot be empty.", width - 1)
            screen.move(2, 7 + visible_columns)
            screen.refresh()

            key = screen.get_wch()
            if key in ("\n", "\r", 10, 13, curses.KEY_ENTER):
                value = "".join(characters).strip()
                if value:
                    return value
                characters.clear()
                input_error = True
            elif key in ("\b", "\x7f", 8, 127, curses.KEY_BACKSPACE):
                if characters:
                    characters.pop()
                input_error = False
            elif isinstance(key, str) and key.isprintable():
                characters.append(key)
                input_error = False
            # Resize and other special keys redraw without changing the buffer.
    finally:
        curses.noecho()
        curses.curs_set(0)


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


def read_curses_score(screen, prompt):
    while True:
        value = read_curses_text(screen, prompt)
        try:
            score = float(value)
            if 0 <= score <= 10:
                return score
        except ValueError:
            pass


def input_student_curses(screen, manager):
    manager.add_student(
        read_curses_unique_id(screen, "Student ID", manager.students),
        read_curses_text(screen, "Student name"),
        read_curses_text(screen, "Date of birth"),
    )


def input_course_curses(screen, manager):
    manager.add_course(
        read_curses_unique_id(screen, "Course ID", manager.courses),
        read_curses_text(screen, "Course name"),
        read_curses_positive_integer(screen, "Credits"),
    )


def input_mark_curses(screen, manager):
    manager.set_mark(
        read_curses_text(screen, "Student ID"),
        read_curses_text(screen, "Course ID"),
        read_curses_score(screen, "Score"),
    )


def input_students(manager):
    number_of_students = read_positive_integer("Number of students: ")
    for index in range(number_of_students):
        print(f"Student {index + 1}")
        student_id = read_unique_id("ID: ", manager.students)
        name = read_non_empty("Name: ")
        date_of_birth = read_non_empty("Date of birth: ")
        manager.add_student(student_id, name, date_of_birth)


def input_courses(manager):
    number_of_courses = read_positive_integer("Number of courses: ")
    for index in range(number_of_courses):
        print(f"Course {index + 1}")
        course_id = read_unique_id("ID: ", manager.courses)
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
