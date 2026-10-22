"""
Unit Tests for RoomAllocator and Scheduler (Milestones 4 & 5)
"""
import unittest
from config import ScheduleCode
from models.subject import Subject
from models.room import Room
from models.faculty import Faculty
from models.timeslot import TimeSlot
from models.exam import Exam
from scheduling.room_allocator import RoomAllocator
from scheduling.scheduler import Scheduler
from validation.validator import Validator


class TestRoomAllocator(unittest.TestCase):
    def setUp(self):
        self.rooms = [
            Room("R_SMALL", "Room A", 30, is_available=True),
            Room("R_MED", "Room B", 50, is_available=True),
            Room("R_LARGE", "Room C", 100, is_available=True),
            Room("R_UNAVAIL", "Room D", 60, is_available=False),
        ]

    def test_best_fit_selection(self):
        # 45 students should pick Room B (50), not Room C (100) or Room A (30)
        alloc, status = RoomAllocator.allocate_best_fit_room(
            student_count=45, slot_id="TS1", rooms=self.rooms, current_schedule=[]
        )
        self.assertIsNotNone(alloc)
        self.assertEqual(alloc.room_id, "R_MED")
        self.assertEqual(status, "OK")

    def test_prevents_double_booking(self):
        # Room B is already booked in TS1
        existing = [Exam("EX1", "CS101", "TS1", "R_MED", "F1")]
        # Next 45 students in TS1 cannot use Room B, must pick Room C
        alloc, status = RoomAllocator.allocate_best_fit_room(
            student_count=45, slot_id="TS1", rooms=self.rooms, current_schedule=existing
        )
        self.assertIsNotNone(alloc)
        self.assertEqual(alloc.room_id, "R_LARGE")

    def test_capacity_exceeded(self):
        # 120 students cannot fit in any room
        alloc, status = RoomAllocator.allocate_best_fit_room(
            student_count=120, slot_id="TS1", rooms=self.rooms, current_schedule=[]
        )
        self.assertIsNone(alloc)
        self.assertEqual(status, "CAPACITY_EXCEEDED")


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()
        self.subjects = [
            Subject("CS101", "Programming", "CSE", 1),
            Subject("CS102", "Data Structures", "CSE", 1),
            Subject("EC101", "Circuits", "ECE", 1),
        ]
        self.students_by_subject = {
            "CS101": [f"S{i}" for i in range(1, 31)],  # 30 students
            "CS102": [f"S{i}" for i in range(1, 31)],  # Same 30 students (must NOT be in same slot)
            "EC101": [f"E{i}" for i in range(1, 26)],  # 25 different students
        }
        self.faculty = [
            Faculty("F1", "Dr. A", "CSE", is_available=True),
            Faculty("F2", "Dr. B", "ECE", is_available=True),
        ]
        self.rooms = [
            Room("R1", "Hall 1", 40, is_available=True),
            Room("R2", "Hall 2", 40, is_available=True),
        ]
        self.timeslots = [
            TimeSlot("TS1", "2026-10-10", "09:00", "12:00", is_available=True),
            TimeSlot("TS2", "2026-10-10", "13:00", "16:00", is_available=True),
        ]

    def test_successful_schedule_generation(self):
        report = self.scheduler.generate_schedule(
            self.subjects, self.students_by_subject, self.faculty, self.rooms, self.timeslots
        )
        self.assertTrue(report.is_complete)
        self.assertEqual(report.scheduled_count, 3)
        self.assertEqual(report.unscheduled_count, 0)

        # Ensure CS101 and CS102 are not in the same slot
        cs101 = next(e for e in report.scheduled_exams if e.subject_id == "CS101")
        cs102 = next(e for e in report.scheduled_exams if e.subject_id == "CS102")
        self.assertNotEqual(cs101.slot_id, cs102.slot_id)

        # Full validation check
        rooms_by_id = {r.room_id: r for r in self.rooms}
        faculty_by_id = {f.faculty_id: f for f in self.faculty}
        slots_by_id = {t.slot_id: t for t in self.timeslots}
        valid, results = Validator.validate_full_timetable(
            report.scheduled_exams, self.students_by_subject, rooms_by_id, faculty_by_id, slots_by_id
        )
        self.assertTrue(valid)

    def test_no_available_timeslots(self):
        # Mark all slots unavailable
        for ts in self.timeslots:
            ts.is_available = False
        report = self.scheduler.generate_schedule(
            self.subjects, self.students_by_subject, self.faculty, self.rooms, self.timeslots
        )
        self.assertFalse(report.is_complete)
        self.assertEqual(report.scheduled_count, 0)
        self.assertEqual(report.unscheduled_count, 3)
        self.assertEqual(report.unscheduled_exams[0].status, ScheduleCode.NO_AVAILABLE_TIME_SLOT)


if __name__ == "__main__":
    unittest.main()
