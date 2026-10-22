"""
Constraint Validation Engine for ExamOpt (Milestone 3)
SRM Institute of Science and Technology, Tiruchirappalli
"""
from dataclasses import dataclass, field
from typing import List, Dict, Set, Any, Tuple, Optional

from config import ValidationCode
from models.exam import Exam
from models.room import Room
from models.faculty import Faculty
from models.timeslot import TimeSlot


@dataclass
class ValidationResult:
    status: str
    is_valid: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "is_valid": self.is_valid,
            "message": self.message,
            "details": self.details,
        }


class Validator:
    """Validates examination assignments against academic constraints."""

    @staticmethod
    def validate_assignment(
        exam: Exam,
        existing_exams: List[Exam],
        students_by_subject: Dict[str, List[str]],
        rooms_by_id: Dict[str, Room],
        faculty_by_id: Dict[str, Faculty],
        timeslots_by_id: Dict[str, TimeSlot],
    ) -> ValidationResult:
        """
        Validates an individual exam assignment against existing schedule.
        Checks:
          - Input validity
          - Slot, Room, Faculty availability
          - Room capacity
          - Duplicate room booking (room conflict)
          - Faculty conflict
          - Student conflict
        """
        # 1. Input Integrity Checks
        if not exam.subject_id or not exam.slot_id or not exam.room_id or not exam.faculty_id:
            return ValidationResult(
                status=ValidationCode.INVALID,
                is_valid=False,
                message="Missing required examination fields (subject, slot, room, or faculty).",
                details={"exam_id": exam.exam_id}
            )

        if exam.slot_id not in timeslots_by_id:
            return ValidationResult(
                status=ValidationCode.INVALID,
                is_valid=False,
                message=f"Time slot '{exam.slot_id}' does not exist.",
                details={"slot_id": exam.slot_id}
            )

        if exam.room_id not in rooms_by_id:
            return ValidationResult(
                status=ValidationCode.INVALID,
                is_valid=False,
                message=f"Room '{exam.room_id}' does not exist.",
                details={"room_id": exam.room_id}
            )

        if exam.faculty_id not in faculty_by_id:
            return ValidationResult(
                status=ValidationCode.INVALID,
                is_valid=False,
                message=f"Faculty '{exam.faculty_id}' does not exist.",
                details={"faculty_id": exam.faculty_id}
            )

        slot = timeslots_by_id[exam.slot_id]
        room = rooms_by_id[exam.room_id]
        faculty = faculty_by_id[exam.faculty_id]

        # 2. Availability Checks
        if not slot.is_available:
            return ValidationResult(
                status=ValidationCode.TIMESLOT_UNAVAILABLE,
                is_valid=False,
                message=f"Time slot '{slot.label}' ({slot.slot_id}) is marked as unavailable.",
                details={"slot_id": slot.slot_id}
            )

        if not room.is_available:
            return ValidationResult(
                status=ValidationCode.ROOM_UNAVAILABLE,
                is_valid=False,
                message=f"Room '{room.name}' ({room.room_id}) is marked as unavailable.",
                details={"room_id": room.room_id, "room_name": room.name}
            )

        if not faculty.is_available:
            return ValidationResult(
                status=ValidationCode.FACULTY_UNAVAILABLE,
                is_valid=False,
                message=f"Faculty '{faculty.name}' ({faculty.faculty_id}) is marked as unavailable.",
                details={"faculty_id": faculty.faculty_id, "faculty_name": faculty.name}
            )

        # 3. Room Capacity Check
        enrolled_students = students_by_subject.get(exam.subject_id, [])
        student_count = exam.student_count if exam.student_count > 0 else len(enrolled_students)

        if student_count > room.capacity:
            return ValidationResult(
                status=ValidationCode.CAPACITY_EXCEEDED,
                is_valid=False,
                message=f"Room '{room.name}' capacity ({room.capacity}) is insufficient for {student_count} students.",
                details={
                    "room_id": room.room_id,
                    "room_name": room.name,
                    "room_capacity": room.capacity,
                    "required_capacity": student_count,
                    "deficit": student_count - room.capacity
                }
            )

        # 4. Duplicate Room Booking (Room Conflict in same time slot)
        for other in existing_exams:
            if other.exam_id == exam.exam_id:
                continue
            if other.slot_id == exam.slot_id and other.room_id == exam.room_id:
                return ValidationResult(
                    status=ValidationCode.DUPLICATE_BOOKING,
                    is_valid=False,
                    message=f"Room '{room.name}' ({room.room_id}) is already booked for exam '{other.exam_id}' in time slot '{slot.label}'.",
                    details={
                        "conflicting_exam_id": other.exam_id,
                        "room_id": room.room_id,
                        "slot_id": slot.slot_id
                    }
                )

        # 5. Faculty Conflict (Same faculty assigned to multiple exams in same time slot)
        for other in existing_exams:
            if other.exam_id == exam.exam_id:
                continue
            if other.slot_id == exam.slot_id and other.faculty_id == exam.faculty_id:
                return ValidationResult(
                    status=ValidationCode.FACULTY_UNAVAILABLE,
                    is_valid=False,
                    message=f"Faculty '{faculty.name}' is already assigned to exam '{other.exam_id}' in time slot '{slot.label}'.",
                    details={
                        "conflicting_exam_id": other.exam_id,
                        "faculty_id": faculty.faculty_id,
                        "slot_id": slot.slot_id
                    }
                )

        # 6. Student Conflict (A student has 2 exams in the same time slot)
        current_students_set = set(enrolled_students)
        for other in existing_exams:
            if other.exam_id == exam.exam_id:
                continue
            if other.slot_id == exam.slot_id:
                other_students = set(students_by_subject.get(other.subject_id, []))
                common = current_students_set.intersection(other_students)
                if common:
                    return ValidationResult(
                        status=ValidationCode.CONFLICT,
                        is_valid=False,
                        message=f"Student conflict: {len(common)} student(s) enrolled in both '{exam.subject_id}' and '{other.subject_id}' in slot '{slot.label}'.",
                        details={
                            "conflicting_exam_id": other.exam_id,
                            "subject_1": exam.subject_id,
                            "subject_2": other.subject_id,
                            "conflicting_students": list(common),
                            "conflict_count": len(common)
                        }
                    )

        return ValidationResult(
            status=ValidationCode.VALID,
            is_valid=True,
            message=f"Assignment for exam '{exam.exam_id}' ({exam.subject_id}) is valid.",
            details={"exam_id": exam.exam_id}
        )

    @staticmethod
    def validate_full_timetable(
        exams: List[Exam],
        students_by_subject: Dict[str, List[str]],
        rooms_by_id: Dict[str, Room],
        faculty_by_id: Dict[str, Faculty],
        timeslots_by_id: Dict[str, TimeSlot],
    ) -> Tuple[bool, List[ValidationResult]]:
        """
        Validates all scheduled exams in a timetable.
        Returns (is_all_valid, list_of_validation_results).
        """
        results: List[ValidationResult] = []
        is_all_valid = True

        scheduled = [e for e in exams if e.slot_id and e.room_id and e.faculty_id]
        
        for i, exam in enumerate(scheduled):
            # Check against exams scheduled before this one
            prior_exams = scheduled[:i]
            res = Validator.validate_assignment(
                exam,
                prior_exams,
                students_by_subject,
                rooms_by_id,
                faculty_by_id,
                timeslots_by_id,
            )
            results.append(res)
            if not res.is_valid:
                is_all_valid = False

        return is_all_valid, results
