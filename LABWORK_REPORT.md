# Python 2026-2027 - Labwork completion report

## Relevant Drive structure

```text
Python 2026-2027/
|-- Slides/
|   |-- 1. Python Introduction.pdf
|   |-- 2. Python Language.pdf
|   `-- 3. Modules and Packages.pdf
`-- Labworks/
    |-- labwork1.pdf
    |-- labwork1b-student-management.pdf
    |-- labwork2.pdf
    `-- labwork3-modules-package.pdf
```

## Lecture/lab mapping

- `labwork1.pdf` and `labwork1b-student-management.pdf` use `2. Python Language.pdf`: expressions, data types, conditions, functions, collections, and loops.
- `labwork2.pdf` is the Git/GitHub submission workflow for Labwork 1 and 1b.
- `labwork3-modules-package.pdf` uses `3. Modules and Packages.pdf` and contains Practical work 3 and Practical work 4.

## Labwork 1 - completed

- Original: `labwork1.pdf`
- Completed file: `labwork1_completed.py`
- Exercises: 12/12 completed
- Coverage: circle area, temperature conversion, prime/perfect numbers, color lookup, ranges, string/list functions, factorial, divisors, distance, and rectangle pattern.
- Note: the PDF refers to a "given list" of colors but does not include the list itself. The interactive example uses a four-item list with `Red` at index 3, matching the expected output; `find_color` accepts any supplied list.

## Practical work 1 - completed

- Original: `labwork1b-student-management.pdf`
- Completed file: `labwork1b_student_management_completed.py`
- Functions: student/course input, mark entry, course/student listing, and per-course mark listing.

## Labwork 2 - completed

- Original: `labwork2.pdf`
- This lab requires editing the repository README with the student's name and ID, committing, and pushing to the student's GitHub fork.
- The public fork is available at `https://github.com/NhatHieu2808/Python-2026-L1`.
- The required code files and Labwork 3-4 project are present in the fork.
- The README contains the confirmed student name `Trương Quý Nhật Hiếu` and student ID `2410287`.

## Practical work 3 - completed

- Original: pages 17-18 of `labwork3-modules-package.pdf`
- Completed file: `3.student.mark.oop.math_completed.py`
- Implements a complete menu-based OOP student/course manager, one-decimal round-down with `math.floor`, NumPy credit-weighted GPA, descending GPA sorting, per-course mark display, and a curses interface.
- Windows does not include `_curses` by default, so a plain-console fallback is included. The curses branch remains available on supported systems.

## Practical work 4 - completed

- Original: page 19 of `labwork3-modules-package.pdf`
- Completed project: `pw4_completed/`
- Structure: `input.py`, `output.py`, `domains/`, and `main.py`.
- The modular menu supports student/course creation, mark entry, course listing, per-course mark display, and GPA-ranked student output.
- A ZIP archive is also supplied for Drive and GitHub transfer.

## Source limitation

The Labwork 3 PDF says to copy "Practical work 2" into `3.student.mark.oop.math.py`, but no Practical work 2 source file or starter code exists in the supplied Drive folder and no matching file was found elsewhere in the connected Drive. The completed OOP implementation therefore preserves the requirements visible in Labwork 1b and Labwork 3 without claiming to reproduce unavailable starter code.
