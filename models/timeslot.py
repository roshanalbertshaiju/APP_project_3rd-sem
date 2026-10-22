"""
TimeSlot Data Model
"""
from dataclasses import dataclass


@dataclass
class TimeSlot:
    slot_id: str
    date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    is_available: bool = True

    @property
    def label(self) -> str:
        return f"{self.date} {self.start_time}-{self.end_time}"

    def to_dict(self):
        return {
            "slot_id": self.slot_id,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            slot_id=data["slot_id"],
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            is_available=bool(data.get("is_available", True)),
        )
