"""
Room Allocation Component for ExamOpt (Milestone 5)
SRM Institute of Science and Technology, Tiruchirappalli
"""
from typing import List, Optional, Tuple, Set
from models.room import Room
from models.exam import Exam


class RoomAllocator:
    """Dedicated Room Allocator implementing Best-Fit capacity matching and conflict prevention."""

    @staticmethod
    def get_booked_room_ids(slot_id: str, current_schedule: List[Exam]) -> Set[str]:
        """Returns set of room IDs already booked in the given slot."""
        return {
            exam.room_id
            for exam in current_schedule
            if exam.slot_id == slot_id and exam.room_id is not None
        }

    @staticmethod
    def get_available_rooms_for_slot(
        slot_id: str,
        rooms: List[Room],
        current_schedule: List[Exam],
    ) -> List[Room]:
        """Returns all physically available and unbooked rooms for the time slot."""
        booked = RoomAllocator.get_booked_room_ids(slot_id, current_schedule)
        return [
            r for r in rooms
            if r.is_available and r.room_id not in booked
        ]

    @staticmethod
    def allocate_best_fit_room(
        student_count: int,
        slot_id: str,
        rooms: List[Room],
        current_schedule: List[Exam],
    ) -> Tuple[Optional[Room], str]:
        """
        Selects the best-fit room for an exam in a given time slot.
        Matches room capacity >= student_count and picks the smallest suitable room to minimize waste.
        Prevents double-booking and checks room availability.

        Returns:
            (Room, "OK") if allocated.
            (None, "CAPACITY_EXCEEDED") if unbooked rooms exist but none have sufficient capacity.
            (None, "NO_ROOM_AVAILABLE") if all rooms are booked or unavailable.
        """
        available_rooms = RoomAllocator.get_available_rooms_for_slot(slot_id, rooms, current_schedule)

        if not available_rooms:
            return None, "NO_ROOM_AVAILABLE"

        # Filter rooms having sufficient capacity
        suitable_rooms = [r for r in available_rooms if r.capacity >= student_count]

        if not suitable_rooms:
            return None, "CAPACITY_EXCEEDED"

        # Best-Fit: Sort ascending by capacity to minimize leftover seats
        suitable_rooms.sort(key=lambda r: (r.capacity, r.name))
        return suitable_rooms[0], "OK"
