"""
Unit Tests for Milestone 8: Functional Programming Pipelines
SRM Institute of Science and Technology, Tiruchirappalli
"""
import unittest

from models.exam import Exam
from models.room import Room
from models.faculty import Faculty
from models.timeslot import TimeSlot
from scheduling.functional_evaluator import (
    reduce_sum,
    map_seat_wastage,
    map_room_utilization_percentages,
    filter_consecutive_student_instances,
    filter_overloaded_faculty_duties,
    evaluate_schedule_functional,
)


class TestFunctionalEvaluator(unittest.TestCase):
    def setUp(self):
        self.rooms = {
            "R1": Room("R1", "LH 101", 60),
            "R2": Room("R2", "LH 102", 40),
        }
        self.faculty = {
            "F1": Faculty("F1", "Dr. Raman", "CSE"),
            "F2": Faculty("F2", "Dr. Priya", "CSE"),
        }
        self.slots = {
            "TS1": TimeSlot("TS1", "2026-10-10", "09:30", "12:30"),
            "TS2": TimeSlot("TS2", "2026-10-10", "13:30", "16:30"),
            "TS3": TimeSlot("TS3", "2026-10-11", "09:30", "12:30"),
        }
        self.students = {
            "CS1": ["S1", "S2", "S3", "S4"],
            "CS2": ["S3", "S4", "S5", "S6"],  # Overlap with CS1 on S3, S4
            "CS3": ["S7", "S8"],
        }

    def test_reduce_sum(self):
        nums = [10.5, 20.5, 30.0]
        self.assertEqual(reduce_sum(nums), 61.0)
        self.assertEqual(reduce_sum([]), 0.0)

    def test_map_seat_wastage(self):
        exams = [
            Exam("E1", "CS1", "TS1", "R1", "F1", student_count=50),  # Room R1 cap 60 -> waste 10
            Exam("E2", "CS2", "TS2", "R2", "F2", student_count=40),  # Room R2 cap 40 -> waste 0
        ]
        wastages = map_seat_wastage(exams, self.rooms)
        self.assertEqual(wastages, [10, 0])

    def test_map_room_utilization_percentages(self):
        exams = [
            Exam("E1", "CS1", "TS1", "R1", "F1", student_count=30),  # 30/60 = 50%
            Exam("E2", "CS2", "TS2", "R2", "F2", student_count=40),  # 40/40 = 100%
        ]
        utils = map_room_utilization_percentages(exams, self.rooms)
        self.assertEqual(utils, [50.0, 100.0])

    def test_filter_consecutive_student_instances(self):
        # E1 in morning, E2 in afternoon of same day -> S3, S4 have consecutive exams
        exams = [
            Exam("E1", "CS1", "TS1", "R1", "F1", student_count=4),
            Exam("E2", "CS2", "TS2", "R2", "F2", student_count=4),
        ]
        consec = filter_consecutive_student_instances(exams, self.students, self.slots)
        self.assertEqual(len(consec), 1)
        pair, students = consec[0]
        self.assertEqual(set(pair), {"CS1", "CS2"})
        self.assertEqual(students, {"S3", "S4"})

    def test_filter_overloaded_faculty(self):
        # F1 assigned to both TS1 and TS2 on same day (2026-10-10)
        exams = [
            Exam("E1", "CS1", "TS1", "R1", "F1", student_count=4),
            Exam("E2", "CS2", "TS2", "R2", "F1", student_count=4),
        ]
        overloaded = filter_overloaded_faculty_duties(exams, self.slots, max_duties_per_day=1)
        self.assertEqual(len(overloaded), 1)
        fac_id, date, count = overloaded[0]
        self.assertEqual(fac_id, "F1")
        self.assertEqual(count, 2)

    def test_evaluate_schedule_functional(self):
        exams = [
            Exam("E1", "CS1", "TS1", "R1", "F1", student_count=50),
            Exam("E2", "CS2", "TS2", "R2", "F2", student_count=35),
        ]
        report = evaluate_schedule_functional(exams, self.students, self.rooms, self.faculty, self.slots)
        self.assertGreater(report.fitness_score, 0.0)
        self.assertGreaterEqual(report.total_penalty, 0.0)
        self.assertIn("consecutive_penalty", report.breakdown)


if __name__ == "__main__":
    unittest.main()
