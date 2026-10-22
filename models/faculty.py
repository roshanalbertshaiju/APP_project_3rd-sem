"""
Faculty Data Model
"""
from dataclasses import dataclass


@dataclass
class Faculty:
    faculty_id: str
    name: str
    department: str
    is_available: bool = True

    def to_dict(self):
        return {
            "faculty_id": self.faculty_id,
            "name": self.name,
            "department": self.department,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            faculty_id=data["faculty_id"],
            name=data["name"],
            department=data["department"],
            is_available=bool(data.get("is_available", True)),
        )
