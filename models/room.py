"""
Room Data Model
"""
from dataclasses import dataclass


@dataclass
class Room:
    room_id: str
    name: str
    capacity: int
    is_available: bool = True

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
            "capacity": self.capacity,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            room_id=data["room_id"],
            name=data["name"],
            capacity=int(data["capacity"]),
            is_available=bool(data.get("is_available", True)),
        )
