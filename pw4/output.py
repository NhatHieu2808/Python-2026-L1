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


def curses_output(screen, manager):
    curses.curs_set(0)
    screen.clear()
    screen.addstr(1, 2, "STUDENT MARK MANAGEMENT", curses.A_BOLD)
    screen.addstr(3, 2, "Students sorted by GPA (descending)")
    for row, line in enumerate(format_student_table(manager), start=5):
        screen.addstr(row, 2, line)
    screen.addstr(5 + len(manager.students) + 2, 2, "Press any key to exit.")
    screen.refresh()
    screen.getch()


def show_students(manager):
    if not manager.students:
        print("No students have been added.")
        return
    if curses is None:
        for line in format_student_table(manager):
            print(line)
    else:
        curses.wrapper(curses_output, manager)


def show_courses(manager):
    if not manager.courses:
        print("No courses have been added.")
        return
    print(f"{'ID':<10}{'Course name':<30}{'Credits':>7}")
    for course in manager.courses.values():
        print(f"{course.course_id:<10}{course.name:<30}{course.credits:>7}")


def show_course_marks(manager, course_id):
    course = manager.courses.get(course_id)
    if course is None:
        raise ValueError("Course not found")
    print(f"Marks for {course.name}")
    for student in manager.students.values():
        score = student.marks.get(course_id)
        shown_score = "Not entered" if score is None else f"{score:.1f}"
        print(f"{student.student_id:<10}{student.name:<25}{shown_score}")
