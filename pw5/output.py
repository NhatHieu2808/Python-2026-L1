try:
    import curses
except ImportError:
    curses = None


def format_student_table(manager):
    lines = [f"{'ID':<10}{'Name':<25}{'DoB':<14}{'GPA':>5}"]
    for student in manager.students_by_gpa():
        gpa = student.calculate_gpa(manager.courses)
        lines.append(
            f"{student.student_id:<10}{student.name:<25}"
            f"{student.date_of_birth:<14}{gpa:>5.2f}"
        )
    return lines


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


def show_students(manager):
    if not manager.students:
        print("No students have been added.")
        return
    for line in format_student_table(manager):
        print(line)


def show_courses(manager):
    if not manager.courses:
        print("No courses have been added.")
        return
    for line in format_course_table(manager):
        print(line)


def show_course_marks(manager, course_id):
    for line in format_course_marks(manager, course_id):
        print(line)


def show_students_curses(screen, manager):
    show_lines_curses(screen, "Students by GPA", format_student_table(manager))


def show_courses_curses(screen, manager):
    show_lines_curses(screen, "Courses", format_course_table(manager))


def show_course_marks_curses(screen, manager, course_id):
    show_lines_curses(screen, "Course marks", format_course_marks(manager, course_id))
