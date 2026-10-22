"""
Exam Data Model
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Exam:
    exam_id: str
    subject_id: str
    slot_id: Optional[str] = None
    room_id: Optional[str] = None
    faculty_id: Optional[str] = None
    student_count: int = 0
    status: str = "Unscheduled"
    status_reason: str = ""

    def to_dict(self):
        return {
            "exam_id": self.exam_id,
            "subject_id": self.subject_id,
            "slot_id": self.slot_id,
            "room_id": self.room_id,
            "faculty_id": self.faculty_id,
            "student_count": self.student_count,
            "status": self.status,
            "status_reason": self.status_reason,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            exam_id=data["exam_id"],
            subject_id=data["subject_id"],
            slot_id=data.get("slot_id"),
            room_id=data.get("room_id"),
            faculty_id=data.get("faculty_id"),
            student_count=int(data.get("student_count", 0)),
            status=data.get("status", "Unscheduled"),
            status_reason=data.get("status_reason", ""),
        )
