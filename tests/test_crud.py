"""
Unit Tests for SQLite CRUD Operations (Milestone 2)
"""
import unittest
from database.database import Database
from models.student import Student
from models.subject import Subject
from models.faculty import Faculty
from models.room import Room
from models.timeslot import TimeSlot
from models.exam import Exam


class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")

    def test_student_crud(self):
        # Create
        sub = Subject("CS101", "Programming", "CSE", 1)
        self.db.create_subject(sub)
        stu = Student("STU01", "Alice", "CSE", 1, ["CS101"])
        self.assertTrue(self.db.create_student(stu))

        # Read
        fetched = self.db.get_student("STU01")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Alice")
        self.assertIn("CS101", fetched.enrolled_subject_ids)

        # Update
        stu.name = "Alice Smith"
        self.assertTrue(self.db.update_student(stu))
        updated = self.db.get_student("STU01")
        self.assertEqual(updated.name, "Alice Smith")

        # Delete
        self.assertTrue(self.db.delete_student("STU01"))
        self.assertIsNone(self.db.get_student("STU01"))

    def test_subject_crud(self):
        sub = Subject("MA101", "Calculus", "Math", 1, 180)
        self.assertTrue(self.db.create_subject(sub))

        fetched = self.db.get_subject("MA101")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Calculus")

        sub.name = "Advanced Calculus"
        self.assertTrue(self.db.update_subject(sub))
        self.assertEqual(self.db.get_subject("MA101").name, "Advanced Calculus")

        self.assertTrue(self.db.delete_subject("MA101"))
        self.assertIsNone(self.db.get_subject("MA101"))

    def test_faculty_crud(self):
        fac = Faculty("FAC10", "Dr. Rao", "ECE", is_available=True)
        self.assertTrue(self.db.create_faculty(fac))

        fetched = self.db.get_faculty("FAC10")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Dr. Rao")

        fac.is_available = False
        self.assertTrue(self.db.update_faculty(fac))
        self.assertFalse(self.db.get_faculty("FAC10").is_available)

        self.assertTrue(self.db.delete_faculty("FAC10"))
        self.assertIsNone(self.db.get_faculty("FAC10"))

    def test_room_crud(self):
        rm = Room("RM101", "Lecture Hall 1", 50, is_available=True)
        self.assertTrue(self.db.create_room(rm))

        fetched = self.db.get_room("RM101")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.capacity, 50)

        rm.capacity = 60
        self.assertTrue(self.db.update_room(rm))
        self.assertEqual(self.db.get_room("RM101").capacity, 60)

        self.assertTrue(self.db.delete_room("RM101"))
        self.assertIsNone(self.db.get_room("RM101"))

    def test_timeslot_crud(self):
        ts = TimeSlot("TS1", "2026-10-15", "09:00", "12:00", is_available=True)
        self.assertTrue(self.db.create_timeslot(ts))

        fetched = self.db.get_timeslot("TS1")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.start_time, "09:00")

        ts.end_time = "12:30"
        self.assertTrue(self.db.update_timeslot(ts))
        self.assertEqual(self.db.get_timeslot("TS1").end_time, "12:30")

        self.assertTrue(self.db.delete_timeslot("TS1"))
        self.assertIsNone(self.db.get_timeslot("TS1"))

    def test_exam_crud(self):
        sub = Subject("CS201", "OS", "CSE", 2)
        ts = TimeSlot("TS2", "2026-10-16", "09:00", "12:00")
        rm = Room("R2", "Lab 2", 40)
        fac = Faculty("F2", "Dr. John", "CSE")
        self.db.create_subject(sub)
        self.db.create_timeslot(ts)
        self.db.create_room(rm)
        self.db.create_faculty(fac)

        exam = Exam("EX01", "CS201", "TS2", "R2", "F2", student_count=35, status="Successfully Scheduled")
        self.assertTrue(self.db.create_exam(exam))

        fetched = self.db.get_exam("EX01")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.student_count, 35)
        self.assertEqual(fetched.status, "Successfully Scheduled")

        self.assertEqual(len(self.db.get_all_exams()), 1)
        self.db.clear_all_exams()
        self.assertEqual(len(self.db.get_all_exams()), 0)


if __name__ == "__main__":
    unittest.main()
