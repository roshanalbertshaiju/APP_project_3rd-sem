"""
Subject Data Model
"""
from dataclasses import dataclass


@dataclass
class Subject:
    subject_id: str
    name: str
    department: str
    semester: int = 1
    duration_minutes: int = 180

    def to_dict(self):
        return {
            "subject_id": self.subject_id,
            "name": self.name,
            "department": self.department,
            "semester": self.semester,
            "duration_minutes": self.duration_minutes,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            subject_id=data["subject_id"],
            name=data["name"],
            department=data["department"],
            semester=int(data.get("semester", 1)),
            duration_minutes=int(data.get("duration_minutes", 180)),
        )
