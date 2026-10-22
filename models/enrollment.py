"""
Enrollment Data Model (Student-Subject mapping)
"""
from dataclasses import dataclass


@dataclass
class Enrollment:
    student_id: str
    subject_id: str

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "subject_id": self.subject_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_id=data["student_id"],
            subject_id=data["subject_id"],
        )
