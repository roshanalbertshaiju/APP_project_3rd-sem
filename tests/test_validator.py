"""
Unit Tests for Constraint Validator (Milestone 3)
"""
import unittest
from config import ValidationCode
from models.room import Room
from models.faculty import Faculty
from models.timeslot import TimeSlot
from models.exam import Exam
from validation.validator import Validator


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.rooms = {
            "R1": Room("R1", "Room 101", 50, is_available=True),
            "R2": Room("R2", "Room 102", 30, is_available=True),
            "R_UNAVAIL": Room("R_UNAVAIL", "Repair Room", 40, is_available=False),
        }
        self.faculty = {
            "F1": Faculty("F1", "Dr. Raman", "CSE", is_available=True),
            "F2": Faculty("F2", "Dr. Priya", "CSE", is_available=True),
            "F_UNAVAIL": Faculty("F_UNAVAIL", "Prof. Leave", "CSE", is_available=False),
        }
        self.timeslots = {
            "TS1": TimeSlot("TS1", "2026-10-10", "09:00", "12:00", is_available=True),
            "TS2": TimeSlot("TS2", "2026-10-10", "13:00", "16:00", is_available=True),
            "TS_UNAVAIL": TimeSlot("TS_UNAVAIL", "2026-10-11", "09:00", "12:00", is_available=False),
        }
        self.students_by_subject = {
            "SUB1": [f"S{i}" for i in range(1, 26)],  # 25 students
            "SUB2": [f"S{i}" for i in range(20, 41)], # 22 students (overlaps with SUB1 on S20..S25)
            "SUB3": [f"S{i}" for i in range(50, 95)], # 45 students (no overlap)
        }

    def test_valid_assignment(self):
        exam = Exam("EX1", "SUB1", "TS1", "R1", "F1", student_count=25)
        res = Validator.validate_assignment(
            exam, [], self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertTrue(res.is_valid)
        self.assertEqual(res.status, ValidationCode.VALID)

    def test_timeslot_unavailable(self):
        exam = Exam("EX1", "SUB1", "TS_UNAVAIL", "R1", "F1")
        res = Validator.validate_assignment(
            exam, [], self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertFalse(res.is_valid)
        self.assertEqual(res.status, ValidationCode.TIMESLOT_UNAVAILABLE)

    def test_room_unavailable(self):
        exam = Exam("EX1", "SUB1", "TS1", "R_UNAVAIL", "F1")
        res = Validator.validate_assignment(
            exam, [], self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertFalse(res.is_valid)
        self.assertEqual(res.status, ValidationCode.ROOM_UNAVAILABLE)

    def test_faculty_unavailable(self):
        exam = Exam("EX1", "SUB1", "TS1", "R1", "F_UNAVAIL")
        res = Validator.validate_assignment(
            exam, [], self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertFalse(res.is_valid)
        self.assertEqual(res.status, ValidationCode.FACULTY_UNAVAILABLE)

    def test_capacity_exceeded(self):
        # SUB3 has 45 students, R2 capacity is 30
        exam = Exam("EX3", "SUB3", "TS1", "R2", "F1", student_count=45)
        res = Validator.validate_assignment(
            exam, [], self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertFalse(res.is_valid)
        self.assertEqual(res.status, ValidationCode.CAPACITY_EXCEEDED)

    def test_duplicate_room_booking(self):
        existing = [Exam("EX1", "SUB1", "TS1", "R1", "F1")]
        # Same room R1 and same slot TS1
        exam = Exam("EX2", "SUB3", "TS1", "R1", "F2")
        res = Validator.validate_assignment(
            exam, existing, self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertFalse(res.is_valid)
        self.assertEqual(res.status, ValidationCode.DUPLICATE_BOOKING)

    def test_faculty_conflict(self):
        existing = [Exam("EX1", "SUB1", "TS1", "R1", "F1")]
        # Different room R2 (capacity 30), student_count=20, but same faculty F1 in same slot TS1
        exam = Exam("EX2", "SUB3", "TS1", "R2", "F1", student_count=20)
        res = Validator.validate_assignment(
            exam, existing, self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertFalse(res.is_valid)
        self.assertEqual(res.status, ValidationCode.FACULTY_UNAVAILABLE)

    def test_student_conflict(self):
        existing = [Exam("EX1", "SUB1", "TS1", "R1", "F1")]
        # SUB2 has overlapping students (S20..S25) with SUB1
        # Assigned to same slot TS1, different room R2 and faculty F2
        exam = Exam("EX2", "SUB2", "TS1", "R2", "F2")
        res = Validator.validate_assignment(
            exam, existing, self.students_by_subject, self.rooms, self.faculty, self.timeslots
        )
        self.assertFalse(res.is_valid)
        self.assertEqual(res.status, ValidationCode.CONFLICT)


if __name__ == "__main__":
    unittest.main()
