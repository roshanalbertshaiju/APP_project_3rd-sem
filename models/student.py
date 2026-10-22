"""
Student Data Model
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Student:
    student_id: str
    name: str
    department: str
    semester: int = 1
    enrolled_subject_ids: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "semester": self.semester,
            "enrolled_subject_ids": self.enrolled_subject_ids,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            department=data["department"],
            semester=int(data.get("semester", 1)),
            enrolled_subject_ids=data.get("enrolled_subject_ids", []),
        )
