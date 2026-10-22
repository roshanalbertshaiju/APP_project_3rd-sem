"""
SQLite Database Connection and CRUD Operations
"""
import sqlite3
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from config import DATABASE_PATH
from models.student import Student
from models.subject import Subject
from models.faculty import Faculty
from models.room import Room
from models.timeslot import TimeSlot
from models.enrollment import Enrollment
from models.exam import Exam
from .schema import CREATE_TABLES_SQL

logger = logging.getLogger(__name__)


class Database:
    """Manages SQLite connection and provides CRUD operations for ExamOpt."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path if db_path is not None else DATABASE_PATH
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON;")
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()

    def _init_db(self):
        """Creates tables if they do not exist."""
        with self.get_connection() as conn:
            conn.executescript(CREATE_TABLES_SQL)

    def reset_database(self):
        """Clears all data from all tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exams;")
            cursor.execute("DELETE FROM enrollments;")
            cursor.execute("DELETE FROM timeslots;")
            cursor.execute("DELETE FROM rooms;")
            cursor.execute("DELETE FROM faculty;")
            cursor.execute("DELETE FROM subjects;")
            cursor.execute("DELETE FROM students;")
            conn.commit()

    # ==========================================
    # STUDENT CRUD
    # ==========================================

    def create_student(self, student: Student) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO students (student_id, name, department, semester)
                VALUES (?, ?, ?, ?)
                """,
                (student.student_id, student.name, student.department, student.semester)
            )
            for sub_id in student.enrolled_subject_ids:
                cursor.execute(
                    "INSERT OR IGNORE INTO enrollments (student_id, subject_id) VALUES (?, ?)",
                    (student.student_id, sub_id)
                )
            conn.commit()
            return True

    def get_student(self, student_id: str) -> Optional[Student]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            row = cursor.fetchone()
            if not row:
                return None
            cursor.execute("SELECT subject_id FROM enrollments WHERE student_id = ?", (student_id,))
            subs = [r["subject_id"] for r in cursor.fetchall()]
            return Student(
                student_id=row["student_id"],
                name=row["name"],
                department=row["department"],
                semester=row["semester"],
                enrolled_subject_ids=subs
            )

    def get_all_students(self) -> List[Student]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY student_id")
            rows = cursor.fetchall()
            students = []
            for row in rows:
                cursor.execute("SELECT subject_id FROM enrollments WHERE student_id = ?", (row["student_id"],))
                subs = [r["subject_id"] for r in cursor.fetchall()]
                students.append(
                    Student(
                        student_id=row["student_id"],
                        name=row["name"],
                        department=row["department"],
                        semester=row["semester"],
                        enrolled_subject_ids=subs
                    )
                )
            return students

    def update_student(self, student: Student) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE students SET name = ?, department = ?, semester = ?
                WHERE student_id = ?
                """,
                (student.name, student.department, student.semester, student.student_id)
            )
            # Update enrollments if provided
            cursor.execute("DELETE FROM enrollments WHERE student_id = ?", (student.student_id,))
            for sub_id in student.enrolled_subject_ids:
                cursor.execute(
                    "INSERT OR IGNORE INTO enrollments (student_id, subject_id) VALUES (?, ?)",
                    (student.student_id, sub_id)
                )
            conn.commit()
            return cursor.rowcount > 0

    def delete_student(self, student_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            conn.commit()
            return cursor.rowcount > 0

    # ==========================================
    # SUBJECT CRUD
    # ==========================================

    def create_subject(self, subject: Subject) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO subjects (subject_id, name, department, semester, duration_minutes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (subject.subject_id, subject.name, subject.department, subject.semester, subject.duration_minutes)
            )
            conn.commit()
            return True

    def get_subject(self, subject_id: str) -> Optional[Subject]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Subject.from_dict(dict(row))

    def get_all_subjects(self) -> List[Subject]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subjects ORDER BY subject_id")
            return [Subject.from_dict(dict(row)) for row in cursor.fetchall()]

    def update_subject(self, subject: Subject) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE subjects SET name = ?, department = ?, semester = ?, duration_minutes = ?
                WHERE subject_id = ?
                """,
                (subject.name, subject.department, subject.semester, subject.duration_minutes, subject.subject_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_subject(self, subject_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))
            conn.commit()
            return cursor.rowcount > 0

    # ==========================================
    # ENROLLMENT OPERATIONS
    # ==========================================

    def enroll_student(self, student_id: str, subject_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO enrollments (student_id, subject_id) VALUES (?, ?)",
                (student_id, subject_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def unenroll_student(self, student_id: str, subject_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM enrollments WHERE student_id = ? AND subject_id = ?",
                (student_id, subject_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_students_for_subject(self, subject_id: str) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT student_id FROM enrollments WHERE subject_id = ?", (subject_id,))
            return [r["student_id"] for r in cursor.fetchall()]

    def get_subjects_for_student(self, student_id: str) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT subject_id FROM enrollments WHERE student_id = ?", (student_id,))
            return [r["subject_id"] for r in cursor.fetchall()]

    def get_all_enrollments(self) -> List[Enrollment]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT student_id, subject_id FROM enrollments")
            return [Enrollment(r["student_id"], r["subject_id"]) for r in cursor.fetchall()]

    # ==========================================
    # FACULTY CRUD
    # ==========================================

    def create_faculty(self, faculty: Faculty) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO faculty (faculty_id, name, department, is_available)
                VALUES (?, ?, ?, ?)
                """,
                (faculty.faculty_id, faculty.name, faculty.department, 1 if faculty.is_available else 0)
            )
            conn.commit()
            return True

    def get_faculty(self, faculty_id: str) -> Optional[Faculty]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM faculty WHERE faculty_id = ?", (faculty_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Faculty(
                faculty_id=row["faculty_id"],
                name=row["name"],
                department=row["department"],
                is_available=bool(row["is_available"])
            )

    def get_all_faculty(self) -> List[Faculty]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM faculty ORDER BY faculty_id")
            return [
                Faculty(
                    faculty_id=row["faculty_id"],
                    name=row["name"],
                    department=row["department"],
                    is_available=bool(row["is_available"])
                )
                for row in cursor.fetchall()
            ]

    def update_faculty(self, faculty: Faculty) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE faculty SET name = ?, department = ?, is_available = ?
                WHERE faculty_id = ?
                """,
                (faculty.name, faculty.department, 1 if faculty.is_available else 0, faculty.faculty_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_faculty(self, faculty_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM faculty WHERE faculty_id = ?", (faculty_id,))
            conn.commit()
            return cursor.rowcount > 0

    # ==========================================
    # ROOM CRUD
    # ==========================================

    def create_room(self, room: Room) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO rooms (room_id, name, capacity, is_available)
                VALUES (?, ?, ?, ?)
                """,
                (room.room_id, room.name, room.capacity, 1 if room.is_available else 0)
            )
            conn.commit()
            return True

    def get_room(self, room_id: str) -> Optional[Room]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms WHERE room_id = ?", (room_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Room(
                room_id=row["room_id"],
                name=row["name"],
                capacity=row["capacity"],
                is_available=bool(row["is_available"])
            )

    def get_all_rooms(self) -> List[Room]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms ORDER BY capacity, room_id")
            return [
                Room(
                    room_id=row["room_id"],
                    name=row["name"],
                    capacity=row["capacity"],
                    is_available=bool(row["is_available"])
                )
                for row in cursor.fetchall()
            ]

    def update_room(self, room: Room) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE rooms SET name = ?, capacity = ?, is_available = ?
                WHERE room_id = ?
                """,
                (room.name, room.capacity, 1 if room.is_available else 0, room.room_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_room(self, room_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM rooms WHERE room_id = ?", (room_id,))
            conn.commit()
            return cursor.rowcount > 0

    # ==========================================
    # TIMESLOT CRUD
    # ==========================================

    def create_timeslot(self, slot: TimeSlot) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO timeslots (slot_id, date, start_time, end_time, is_available)
                VALUES (?, ?, ?, ?, ?)
                """,
                (slot.slot_id, slot.date, slot.start_time, slot.end_time, 1 if slot.is_available else 0)
            )
            conn.commit()
            return True

    def get_timeslot(self, slot_id: str) -> Optional[TimeSlot]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM timeslots WHERE slot_id = ?", (slot_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return TimeSlot(
                slot_id=row["slot_id"],
                date=row["date"],
                start_time=row["start_time"],
                end_time=row["end_time"],
                is_available=bool(row["is_available"])
            )

    def get_all_timeslots(self) -> List[TimeSlot]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM timeslots ORDER BY date, start_time, slot_id")
            return [
                TimeSlot(
                    slot_id=row["slot_id"],
                    date=row["date"],
                    start_time=row["start_time"],
                    end_time=row["end_time"],
                    is_available=bool(row["is_available"])
                )
                for row in cursor.fetchall()
            ]

    def update_timeslot(self, slot: TimeSlot) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE timeslots SET date = ?, start_time = ?, end_time = ?, is_available = ?
                WHERE slot_id = ?
                """,
                (slot.date, slot.start_time, slot.end_time, 1 if slot.is_available else 0, slot.slot_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_timeslot(self, slot_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM timeslots WHERE slot_id = ?", (slot_id,))
            conn.commit()
            return cursor.rowcount > 0

    # ==========================================
    # EXAMS CRUD
    # ==========================================

    def create_exam(self, exam: Exam) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO exams (exam_id, subject_id, slot_id, room_id, faculty_id, student_count, status, status_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    exam.exam_id,
                    exam.subject_id,
                    exam.slot_id,
                    exam.room_id,
                    exam.faculty_id,
                    exam.student_count,
                    exam.status,
                    exam.status_reason
                )
            )
            conn.commit()
            return True

    def get_exam(self, exam_id: str) -> Optional[Exam]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exams WHERE exam_id = ?", (exam_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Exam.from_dict(dict(row))

    def get_all_exams(self) -> List[Exam]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exams ORDER BY exam_id")
            return [Exam.from_dict(dict(row)) for row in cursor.fetchall()]

    def delete_exam(self, exam_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exams WHERE exam_id = ?", (exam_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all_exams(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exams")
            conn.commit()
