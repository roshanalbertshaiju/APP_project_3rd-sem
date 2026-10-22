"""
Domain models for ExamOpt
"""
from .student import Student
from .subject import Subject
from .faculty import Faculty
from .room import Room
from .timeslot import TimeSlot
from .enrollment import Enrollment
from .exam import Exam

__all__ = [
    "Student",
    "Subject",
    "Faculty",
    "Room",
    "TimeSlot",
    "Enrollment",
    "Exam",
]
