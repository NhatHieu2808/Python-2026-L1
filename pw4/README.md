# Practical work 4 - modularization

This project splits the Practical work 3 student mark application into:

- `input.py`: console input functions.
- `output.py`: curses output, with a plain-console fallback on Windows.
- `domains/`: student, course, and manager classes.
- `main.py`: application coordination and menu.

The menu supports adding students and courses, entering marks, listing courses,
showing marks for a selected course, and listing students in descending GPA
order. Marks are rounded down to one decimal place and GPA is weighted by the
course credits with NumPy.

Install the dependency from the repository root:

```text
python -m pip install -r requirements.txt
```

Run the application from the repository root:

```text
python pw4/main.py
```
