import math
import numpy as np


class Student:
    def __init__(self, student_id, name, date_of_birth):
        self.student_id = student_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.marks = {}

    def set_mark(self, course_id, score):
        if score < 0 or score > 10:
            raise ValueError("A score must be from 0 to 10")
        self.marks[course_id] = math.floor(score * 10) / 10

    def calculate_gpa(self, courses):
        scores = []
        credits = []
        for course_id, score in self.marks.items():
            if course_id in courses:
                scores.append(score)
                credits.append(courses[course_id].credits)
        if not credits:
            return 0.0
        score_array = np.array(scores, dtype=float)
        credit_array = np.array(credits, dtype=float)
        return float(np.sum(score_array * credit_array) / np.sum(credit_array))
