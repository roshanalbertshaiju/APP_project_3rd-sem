"""
ExamOpt — Multiprocessing & Parallel Schedule Search Engine
Milestone 9: Parallel Computing & GIL Bypassing (ProcessPoolExecutor)
SRM Institute of Science and Technology, Tiruchirappalli

Leverages ProcessPoolExecutor to spawn independent OS processes, bypassing CPython's
Global Interpreter Lock (GIL) and unlocking true multi-core parallel computation.
"""
import os
import time
import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
from concurrent.futures import ProcessPoolExecutor

from models.subject import Subject
from models.room import Room
from models.faculty import Faculty
from models.timeslot import TimeSlot
from models.exam import Exam
from scheduling.scheduler import Scheduler, ScheduleReport
from scheduling.room_allocator import RoomAllocator
from scheduling.functional_evaluator import (
    evaluate_schedule_functional,
    FunctionalEvaluationReport,
)
from config import DEFAULT_PARALLEL_WORKERS, DEFAULT_CANDIDATE_SCHEDULES


@dataclass
class CandidateResult:
    """Evaluation summary of an individual parallel candidate run."""
    candidate_id: int
    worker_pid: int
    scheduled_exams: List[Dict[str, Any]]
    is_valid: bool
    hard_conflicts: int
    soft_penalty: float
    fitness_score: float
    elapsed_seconds: float


@dataclass
class ParallelSearchResult:
    """Composite result of multi-core parallel candidate evaluation."""
    best_schedule: List[Exam]
    best_candidate_id: int
    total_candidates_evaluated: int
    workers_used: int
    best_fitness: float
    best_soft_penalty: float
    hard_conflicts: int
    elapsed_time_seconds: float
    candidate_summaries: List[Dict[str, Any]]
    evaluation_report: Optional[FunctionalEvaluationReport] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "best_candidate_id": self.best_candidate_id,
            "total_candidates_evaluated": self.total_candidates_evaluated,
            "workers_used": self.workers_used,
            "best_fitness": round(self.best_fitness, 4),
            "best_soft_penalty": round(self.best_soft_penalty, 2),
            "hard_conflicts": self.hard_conflicts,
            "elapsed_time_seconds": round(self.elapsed_time_seconds, 4),
            "candidate_summaries": self.candidate_summaries,
            "evaluation_report": self.evaluation_report.to_dict() if self.evaluation_report else None,
        }


# =============================================================================
# TOP-LEVEL PICKLABLE WORKER FUNCTION FOR MULTIPROCESSING
# =============================================================================

def _evaluate_candidate_worker(
    candidate_id: int,
    subjects_data: List[Dict[str, Any]],
    students_by_subject: Dict[str, List[str]],
    faculty_data: List[Dict[str, Any]],
    rooms_data: List[Dict[str, Any]],
    slots_data: List[Dict[str, Any]],
    random_seed: int,
) -> Dict[str, Any]:
    """
    Independent worker executed inside a separate OS process.
    Bypasses GIL and operates in its own memory space.
    """
    t_start = time.perf_counter()
    pid = os.getpid()
    random.seed(random_seed)

    # Reconstruct domain objects from serialized dictionaries
    subjects = [Subject.from_dict(d) for d in subjects_data]
    faculty = [Faculty.from_dict(d) for d in faculty_data]
    rooms = [Room.from_dict(d) for d in rooms_data]
    slots = [TimeSlot.from_dict(d) for d in slots_data]

    # Stochastic variation: shuffle subjects with slight priority jitter
    shuffled_subjects = list(subjects)
    shuffled_subjects.sort(
        key=lambda s: len(students_by_subject.get(s.subject_id, [])) + random.uniform(-0.5, 0.5),
        reverse=True,
    )

    # Run heuristic scheduling
    scheduler = Scheduler(RoomAllocator())
    report = scheduler.generate_schedule(
        shuffled_subjects, students_by_subject, faculty, rooms, slots
    )

    # Functional evaluation
    rooms_by_id = {r.room_id: r for r in rooms}
    faculty_by_id = {f.faculty_id: f for f in faculty}
    slots_by_id = {s.slot_id: s for s in slots}

    eval_report = evaluate_schedule_functional(
        report.scheduled_exams, students_by_subject, rooms_by_id, faculty_by_id, slots_by_id
    )

    t_end = time.perf_counter()

    return {
        "candidate_id": candidate_id,
        "worker_pid": pid,
        "scheduled_exams": [e.to_dict() for e in report.scheduled_exams],
        "is_valid": report.is_complete and len(report.unscheduled_exams) == 0,
        "hard_conflicts": len(report.unscheduled_exams),
        "soft_penalty": eval_report.total_penalty,
        "fitness_score": eval_report.fitness_score,
        "elapsed_seconds": t_end - t_start,
    }


class ParallelScheduler:
    """
    Coordinates multi-process parallel search across CPU cores.
    """

    def __init__(self, max_workers: Optional[int] = None):
        cpu_count = os.cpu_count() or 4
        self.max_workers = max_workers or min(cpu_count, DEFAULT_PARALLEL_WORKERS)

    def search_best_schedule(
        self,
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        faculty: List[Faculty],
        rooms: List[Room],
        timeslots: List[TimeSlot],
        num_candidates: int = DEFAULT_CANDIDATE_SCHEDULES,
    ) -> ParallelSearchResult:
        """
        Executes parallel candidate searches using ProcessPoolExecutor.
        """
        t0 = time.perf_counter()

        # Serialize objects to dicts for clean multiprocessing pickling
        sub_dicts = [s.to_dict() for s in subjects]
        fac_dicts = [f.to_dict() for f in faculty]
        room_dicts = [r.to_dict() for r in rooms]
        slot_dicts = [s.to_dict() for s in timeslots]

        candidate_args = [
            (
                i + 1,
                sub_dicts,
                students_by_subject,
                fac_dicts,
                room_dicts,
                slot_dicts,
                100 + i * 37,
            )
            for i in range(num_candidates)
        ]

        # Execute parallel workers
        results_data = []
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(_evaluate_candidate_worker, *arg) for arg in candidate_args]
            for future in futures:
                results_data.append(future.result())

        t1 = time.perf_counter()

        # Select candidate with highest fitness score
        results_data.sort(key=lambda x: (x["is_valid"], x["fitness_score"]), reverse=True)
        best = results_data[0]

        best_exams = [Exam.from_dict(d) for d in best["scheduled_exams"]]

        rooms_by_id = {r.room_id: r for r in rooms}
        faculty_by_id = {f.faculty_id: f for f in faculty}
        slots_by_id = {s.slot_id: s for s in timeslots}

        eval_report = evaluate_schedule_functional(
            best_exams, students_by_subject, rooms_by_id, faculty_by_id, slots_by_id
        )

        summaries = [
            {
                "candidate_id": r["candidate_id"],
                "worker_pid": r["worker_pid"],
                "fitness": round(r["fitness_score"], 4),
                "penalty": round(r["soft_penalty"], 2),
                "scheduled": len(r["scheduled_exams"]),
            }
            for r in results_data
        ]

        return ParallelSearchResult(
            best_schedule=best_exams,
            best_candidate_id=best["candidate_id"],
            total_candidates_evaluated=len(results_data),
            workers_used=self.max_workers,
            best_fitness=best["fitness_score"],
            best_soft_penalty=best["soft_penalty"],
            hard_conflicts=best["hard_conflicts"],
            elapsed_time_seconds=t1 - t0,
            candidate_summaries=summaries,
            evaluation_report=eval_report,
        )

    def benchmark_speedup(
        self,
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        faculty: List[Faculty],
        rooms: List[Room],
        timeslots: List[TimeSlot],
        num_candidates: int = 8,
    ) -> Dict[str, Any]:
        """
        Benchmarks execution time: Sequential (1 core) vs Parallel (N cores).
        Demonstrates multi-core speedup and GIL circumvention.
        """
        # Sequential Benchmark (1 worker)
        p_seq = ParallelScheduler(max_workers=1)
        t_seq_start = time.perf_counter()
        _ = p_seq.search_best_schedule(
            subjects, students_by_subject, faculty, rooms, timeslots, num_candidates=num_candidates
        )
        t_seq = time.perf_counter() - t_seq_start

        # Parallel Benchmark (N workers)
        p_par = ParallelScheduler(max_workers=self.max_workers)
        t_par_start = time.perf_counter()
        _ = p_par.search_best_schedule(
            subjects, students_by_subject, faculty, rooms, timeslots, num_candidates=num_candidates
        )
        t_par = time.perf_counter() - t_par_start

        speedup = t_seq / max(1e-5, t_par)
        cpu_cores = os.cpu_count() or 1

        return {
            "cpu_cores_detected": cpu_cores,
            "workers_deployed": self.max_workers,
            "candidates_evaluated": num_candidates,
            "sequential_time_seconds": round(t_seq, 4),
            "parallel_time_seconds": round(t_par, 4),
            "speedup_factor": round(speedup, 2),
            "efficiency_percentage": round((speedup / self.max_workers) * 100, 1),
        }
