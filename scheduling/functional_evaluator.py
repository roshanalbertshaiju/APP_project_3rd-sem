"""
ExamOpt — Functional Programming Evaluation Pipeline
Milestone 8: Functional Programming Paradigms (map, filter, reduce, itertools)
SRM Institute of Science and Technology, Tiruchirappalli

Implements pure functional evaluation of examination timetables with zero side effects,
immutable transformations, and higher-order function composition.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set, Any, Optional, Callable
from functools import reduce
import itertools
import operator

from models.exam import Exam
from models.room import Room
from models.faculty import Faculty
from models.timeslot import TimeSlot
from config import (
    WEIGHT_STUDENT_CONSECUTIVE,
    WEIGHT_FACULTY_OVERLOAD,
    WEIGHT_ROOM_SEAT_WASTE,
)


@dataclass(frozen=True)
class FunctionalEvaluationReport:
    """Immutable evaluation report produced by the functional pipeline."""
    total_penalty: float
    fitness_score: float
    consecutive_exam_students: int
    overloaded_faculty_instances: int
    total_seat_wastage: int
    average_room_utilization_pct: float
    breakdown: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_penalty": round(self.total_penalty, 2),
            "fitness_score": round(self.fitness_score, 4),
            "consecutive_exam_students": self.consecutive_exam_students,
            "overloaded_faculty_instances": self.overloaded_faculty_instances,
            "total_seat_wastage": self.total_seat_wastage,
            "average_room_utilization_pct": round(self.average_room_utilization_pct, 1),
            "breakdown": {k: round(v, 2) for k, v in self.breakdown.items()},
        }


# =============================================================================
# PURE FUNCTIONAL FILTER PRIMITIVES
# =============================================================================

def are_slots_consecutive(slot1: TimeSlot, slot2: TimeSlot) -> bool:
    """Pure predicate: True if two slots occur on the same date and are consecutive."""
    if slot1.date != slot2.date:
        return False
    # Exam slots on same date are consecutive if end_time <= start_time or adjacent
    # For SRM standard 2-slot day (09:30-12:30, 13:30-16:30): different slots on same day are consecutive
    return slot1.slot_id != slot2.slot_id


def extract_student_clashes_on_consecutive_slots(
    exam_pair: Tuple[Exam, Exam],
    students_by_subject: Dict[str, List[str]],
    slots_by_id: Dict[str, TimeSlot],
) -> Set[str]:
    """Pure function: returns set of students appearing in both exams if slots are consecutive."""
    e1, e2 = exam_pair
    s1 = slots_by_id.get(e1.slot_id)
    s2 = slots_by_id.get(e2.slot_id)
    if not s1 or not s2 or not are_slots_consecutive(s1, s2):
        return set()
    students_e1 = set(students_by_subject.get(e1.subject_id, []))
    students_e2 = set(students_by_subject.get(e2.subject_id, []))
    return students_e1.intersection(students_e2)


def filter_consecutive_student_instances(
    scheduled_exams: List[Exam],
    students_by_subject: Dict[str, List[str]],
    slots_by_id: Dict[str, TimeSlot],
) -> List[Tuple[Tuple[str, str], Set[str]]]:
    """
    Pure pipeline using itertools.combinations and filter:
    Identifies all exam pairs whose slots are on the same day and have student overlap.
    """
    exam_pairs = list(itertools.combinations(scheduled_exams, 2))
    
    # Filter pairs that have consecutive overlap
    def has_consecutive_overlap(pair: Tuple[Exam, Exam]) -> bool:
        clashes = extract_student_clashes_on_consecutive_slots(pair, students_by_subject, slots_by_id)
        return len(clashes) > 0

    valid_consecutive_pairs = list(filter(has_consecutive_overlap, exam_pairs))

    # Map to tuple of ((subj1, subj2), overlapping_students)
    return list(
        map(
            lambda pair: (
                (pair[0].subject_id, pair[1].subject_id),
                extract_student_clashes_on_consecutive_slots(pair, students_by_subject, slots_by_id),
            ),
            valid_consecutive_pairs,
        )
    )


def filter_overloaded_faculty_duties(
    scheduled_exams: List[Exam],
    slots_by_id: Dict[str, TimeSlot],
    max_duties_per_day: int = 1,
) -> List[Tuple[str, str, int]]:
    """
    Pure pipeline: groups exams by (faculty_id, date) and filters those exceeding daily quota.
    Returns: list of (faculty_id, date, count).
    """
    # Map exams to (faculty_id, date) keys
    faculty_date_pairs = list(
        map(
            lambda e: (e.faculty_id, slots_by_id[e.slot_id].date if e.slot_id in slots_by_id else "UNKNOWN"),
            filter(lambda e: bool(e.faculty_id and e.slot_id), scheduled_exams),
        )
    )

    # Sort for itertools.groupby
    sorted_pairs = sorted(faculty_date_pairs, key=lambda p: (p[0], p[1]))
    grouped = [
        (key[0], key[1], len(list(group)))
        for key, group in itertools.groupby(sorted_pairs, key=lambda p: (p[0], p[1]))
    ]

    # Filter to only groups exceeding max_duties_per_day
    return list(filter(lambda item: item[2] > max_duties_per_day, grouped))


# =============================================================================
# PURE FUNCTIONAL MAP PRIMITIVES
# =============================================================================

def map_seat_wastage(
    scheduled_exams: List[Exam],
    rooms_by_id: Dict[str, Room],
) -> List[int]:
    """Pure map: transforms each scheduled exam into wasted seat count (capacity - student_count)."""
    return list(
        map(
            lambda e: max(0, rooms_by_id[e.room_id].capacity - e.student_count)
            if e.room_id in rooms_by_id
            else 0,
            scheduled_exams,
        )
    )


def map_room_utilization_percentages(
    scheduled_exams: List[Exam],
    rooms_by_id: Dict[str, Room],
) -> List[float]:
    """Pure map: transforms each scheduled exam into room utilization percentage."""
    def calc_util(e: Exam) -> float:
        if e.room_id not in rooms_by_id or rooms_by_id[e.room_id].capacity <= 0:
            return 0.0
        cap = rooms_by_id[e.room_id].capacity
        return min(100.0, (e.student_count / cap) * 100.0)

    return list(map(calc_util, scheduled_exams))


# =============================================================================
# PURE FUNCTIONAL REDUCE PRIMITIVES
# =============================================================================

def reduce_sum(numbers: List[float], initial: float = 0.0) -> float:
    """Pure reduce: aggregates a numeric sequence using operator.add."""
    if not numbers:
        return initial
    return reduce(operator.add, numbers, initial)


# =============================================================================
# COMPOSITE FUNCTIONAL EVALUATOR PIPELINE
# =============================================================================

def evaluate_schedule_functional(
    scheduled_exams: List[Exam],
    students_by_subject: Dict[str, List[str]],
    rooms_by_id: Dict[str, Room],
    faculty_by_id: Dict[str, Faculty],
    slots_by_id: Dict[str, TimeSlot],
    weights: Optional[Dict[str, float]] = None,
) -> FunctionalEvaluationReport:
    """
    Pure higher-order pipeline: Evaluates a schedule's soft constraint quality
    using map, filter, and functools.reduce.
    """
    w_consecutive = (weights or {}).get("consecutive", WEIGHT_STUDENT_CONSECUTIVE)
    w_faculty = (weights or {}).get("faculty", WEIGHT_FACULTY_OVERLOAD)
    w_waste = (weights or {}).get("waste", WEIGHT_ROOM_SEAT_WASTE)

    # 1. Pipeline: Consecutive student instances
    consecutive_instances = filter_consecutive_student_instances(
        scheduled_exams, students_by_subject, slots_by_id
    )
    # Total affected students summed via reduce
    affected_students_counts = list(map(lambda item: len(item[1]), consecutive_instances))
    total_consecutive_students = int(reduce_sum(affected_students_counts, 0.0))
    consecutive_penalty = total_consecutive_students * w_consecutive

    # 2. Pipeline: Overloaded faculty instances
    overloaded_faculty = filter_overloaded_faculty_duties(scheduled_exams, slots_by_id, max_duties_per_day=1)
    excess_duties = list(map(lambda item: item[2] - 1, overloaded_faculty))
    total_excess_duties = int(reduce_sum(excess_duties, 0.0))
    faculty_penalty = total_excess_duties * w_faculty

    # 3. Pipeline: Room seat wastage
    seat_wastages = map_seat_wastage(scheduled_exams, rooms_by_id)
    total_seat_wastage = int(reduce_sum(list(map(float, seat_wastages)), 0.0))
    wastage_penalty = total_seat_wastage * w_waste

    # 4. Pipeline: Room utilization rate
    utilization_rates = map_room_utilization_percentages(scheduled_exams, rooms_by_id)
    avg_utilization = (
        (reduce_sum(utilization_rates, 0.0) / len(utilization_rates))
        if utilization_rates
        else 0.0
    )

    # Aggregate penalties using reduce
    penalties = [consecutive_penalty, faculty_penalty, wastage_penalty]
    total_penalty = reduce_sum(penalties, 0.0)

    # Fitness: bounded score [0, 1000]
    fitness_score = 1000.0 / (1.0 + total_penalty)

    return FunctionalEvaluationReport(
        total_penalty=total_penalty,
        fitness_score=fitness_score,
        consecutive_exam_students=total_consecutive_students,
        overloaded_faculty_instances=total_excess_duties,
        total_seat_wastage=total_seat_wastage,
        average_room_utilization_pct=avg_utilization,
        breakdown={
            "consecutive_penalty": consecutive_penalty,
            "faculty_penalty": faculty_penalty,
            "wastage_penalty": wastage_penalty,
        },
    )
