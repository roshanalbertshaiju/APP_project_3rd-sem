"""
Examination Scheduling Engine for ExamOpt (Milestone 4)
SRM Institute of Science and Technology, Tiruchirappalli
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

from config import ScheduleCode, ValidationCode
from models.subject import Subject
from models.faculty import Faculty
from models.room import Room
from models.timeslot import TimeSlot
from models.exam import Exam
from validation.validator import Validator
from .room_allocator import RoomAllocator


@dataclass
class ScheduleReport:
    scheduled_exams: List[Exam] = field(default_factory=list)
    unscheduled_exams: List[Exam] = field(default_factory=list)
    is_complete: bool = False
    total_subjects: int = 0
    scheduled_count: int = 0
    unscheduled_count: int = 0
    summary_message: str = ""

    def to_dict(self):
        return {
            "scheduled_count": self.scheduled_count,
            "unscheduled_count": self.unscheduled_count,
            "total_subjects": self.total_subjects,
            "is_complete": self.is_complete,
            "summary_message": self.summary_message,
            "scheduled_exams": [e.to_dict() for e in self.scheduled_exams],
            "unscheduled_exams": [e.to_dict() for e in self.unscheduled_exams],
        }


class Scheduler:
    """Intelligent Examination Scheduler (Heuristic-based conflict-free timetable generator)."""

    def __init__(self, room_allocator: Optional[RoomAllocator] = None):
        self.room_allocator = room_allocator or RoomAllocator()

    def generate_schedule(
        self,
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        faculty_list: List[Faculty],
        rooms: List[Room],
        timeslots: List[TimeSlot],
    ) -> ScheduleReport:
        """
        Generates a feasible, conflict-free examination timetable.
        Returns ScheduleReport with scheduled and unscheduled exams.
        """
        scheduled_exams: List[Exam] = []
        unscheduled_exams: List[Exam] = []

        # Maps for quick lookups
        rooms_by_id = {r.room_id: r for r in rooms}
        faculty_by_id = {f.faculty_id: f for f in faculty_list}
        timeslots_by_id = {t.slot_id: t for t in timeslots}

        # Filter available slots and faculty
        available_slots = [ts for ts in timeslots if ts.is_available]
        available_faculty = [f for f in faculty_list if f.is_available]

        if not available_slots:
            for sub in subjects:
                cnt = len(students_by_subject.get(sub.subject_id, []))
                unscheduled_exams.append(
                    Exam(
                        exam_id=f"EXAM_{sub.subject_id}",
                        subject_id=sub.subject_id,
                        student_count=cnt,
                        status=ScheduleCode.NO_AVAILABLE_TIME_SLOT,
                        status_reason="No available time slots configured.",
                    )
                )
            return ScheduleReport(
                scheduled_exams=[],
                unscheduled_exams=unscheduled_exams,
                is_complete=False,
                total_subjects=len(subjects),
                scheduled_count=0,
                unscheduled_count=len(subjects),
                summary_message="No active time slots available to schedule examinations.",
            )

        # Sort subjects by enrolled student count descending (Most Constrained Variable)
        sorted_subjects = sorted(
            subjects,
            key=lambda s: len(students_by_subject.get(s.subject_id, [])),
            reverse=True,
        )

        for sub in sorted_subjects:
            student_ids = students_by_subject.get(sub.subject_id, [])
            student_count = len(student_ids)
            student_set = set(student_ids)

            assigned = False
            last_failure_reason = ScheduleCode.UNSCHEDULED

            for slot in available_slots:
                # 1. Check Student Conflicts for this slot
                student_conflict = False
                for existing in scheduled_exams:
                    if existing.slot_id == slot.slot_id:
                        existing_students = set(students_by_subject.get(existing.subject_id, []))
                        overlap = student_set.intersection(existing_students)
                        if overlap:
                            student_conflict = True
                            last_failure_reason = ScheduleCode.CONFLICT
                            break
                if student_conflict:
                    continue

                # 2. Check Faculty Availability for this slot
                booked_faculty_ids = {
                    e.faculty_id
                    for e in scheduled_exams
                    if e.slot_id == slot.slot_id and e.faculty_id is not None
                }
                free_faculty = [
                    f for f in available_faculty
                    if f.faculty_id not in booked_faculty_ids
                ]
                if not free_faculty:
                    last_failure_reason = ScheduleCode.FACULTY_UNAVAILABLE
                    continue

                # 3. Find suitable Room using RoomAllocator (Best-Fit)
                allocated_room, room_status = self.room_allocator.allocate_best_fit_room(
                    student_count=student_count,
                    slot_id=slot.slot_id,
                    rooms=rooms,
                    current_schedule=scheduled_exams,
                )

                if not allocated_room:
                    if room_status == "CAPACITY_EXCEEDED":
                        last_failure_reason = ScheduleCode.NO_AVAILABLE_ROOM
                    else:
                        last_failure_reason = ScheduleCode.NO_AVAILABLE_ROOM
                    continue

                # Pick the first free faculty
                assigned_faculty = free_faculty[0]

                # Create Candidate Exam
                candidate_exam = Exam(
                    exam_id=f"EXAM_{sub.subject_id}",
                    subject_id=sub.subject_id,
                    slot_id=slot.slot_id,
                    room_id=allocated_room.room_id,
                    faculty_id=assigned_faculty.faculty_id,
                    student_count=student_count,
                    status=ScheduleCode.SUCCESSFULLY_SCHEDULED,
                    status_reason=f"Scheduled in {allocated_room.name} (Cap: {allocated_room.capacity}), Invigilator: {assigned_faculty.name}",
                )

                # 4. Strict verification through Validator
                validation = Validator.validate_assignment(
                    exam=candidate_exam,
                    existing_exams=scheduled_exams,
                    students_by_subject=students_by_subject,
                    rooms_by_id=rooms_by_id,
                    faculty_by_id=faculty_by_id,
                    timeslots_by_id=timeslots_by_id,
                )

                if validation.is_valid:
                    scheduled_exams.append(candidate_exam)
                    assigned = True
                    break
                else:
                    last_failure_reason = validation.status

            if not assigned:
                unscheduled_exams.append(
                    Exam(
                        exam_id=f"EXAM_{sub.subject_id}",
                        subject_id=sub.subject_id,
                        student_count=student_count,
                        status=last_failure_reason,
                        status_reason=f"Could not find a feasible conflict-free assignment: {last_failure_reason}",
                    )
                )

        scheduled_count = len(scheduled_exams)
        unscheduled_count = len(unscheduled_exams)
        is_complete = unscheduled_count == 0

        summary = (
            f"Scheduling complete: {scheduled_count}/{len(subjects)} subjects scheduled successfully."
            if is_complete
            else f"Scheduling partial: {scheduled_count} scheduled, {unscheduled_count} unscheduled."
        )

        return ScheduleReport(
            scheduled_exams=scheduled_exams,
            unscheduled_exams=unscheduled_exams,
            is_complete=is_complete,
            total_subjects=len(subjects),
            scheduled_count=scheduled_count,
            unscheduled_count=unscheduled_count,
            summary_message=summary,
        )
