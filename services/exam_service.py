"""
Application Service Layer for ExamOpt
Decouples GUI / Future Socket Server from Core Database and Scheduling Engines.
"""
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
import csv

from database.database import Database
from models.student import Student
from models.subject import Subject
from models.faculty import Faculty
from models.room import Room
from models.timeslot import TimeSlot
from models.exam import Exam
from scheduling.scheduler import Scheduler, ScheduleReport
from scheduling.room_allocator import RoomAllocator
from validation.validator import Validator, ValidationResult
from utils.sample_data import populate_srm_sample_data


class ExamService:
    """Central facade for ExamOpt operations."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()
        self.room_allocator = RoomAllocator()
        self.scheduler = Scheduler(self.room_allocator)

    # ------------------------------------------
    # Sample Data Loader
    # ------------------------------------------
    def load_srm_sample_data(self) -> Dict[str, int]:
        """Loads realistic SRM IST Tiruchirappalli sample dataset."""
        return populate_srm_sample_data(self.db)

    # ------------------------------------------
    # Student Operations
    # ------------------------------------------
    def get_students(self) -> List[Student]:
        return self.db.get_all_students()

    def get_student(self, student_id: str) -> Optional[Student]:
        return self.db.get_student(student_id)

    def add_student(self, student: Student) -> bool:
        return self.db.create_student(student)

    def update_student(self, student: Student) -> bool:
        return self.db.update_student(student)

    def delete_student(self, student_id: str) -> bool:
        return self.db.delete_student(student_id)

    def enroll_student(self, student_id: str, subject_id: str) -> bool:
        return self.db.enroll_student(student_id, subject_id)

    def unenroll_student(self, student_id: str, subject_id: str) -> bool:
        return self.db.unenroll_student(student_id, subject_id)

    # ------------------------------------------
    # Subject Operations
    # ------------------------------------------
    def get_subjects(self) -> List[Subject]:
        return self.db.get_all_subjects()

    def get_subject(self, subject_id: str) -> Optional[Subject]:
        return self.db.get_subject(subject_id)

    def add_subject(self, subject: Subject) -> bool:
        return self.db.create_subject(subject)

    def update_subject(self, subject: Subject) -> bool:
        return self.db.update_subject(subject)

    def delete_subject(self, subject_id: str) -> bool:
        return self.db.delete_subject(subject_id)

    # ------------------------------------------
    # Faculty Operations
    # ------------------------------------------
    def get_faculty(self) -> List[Faculty]:
        return self.db.get_all_faculty()

    def add_faculty(self, faculty: Faculty) -> bool:
        return self.db.create_faculty(faculty)

    def update_faculty(self, faculty: Faculty) -> bool:
        return self.db.update_faculty(faculty)

    def delete_faculty(self, faculty_id: str) -> bool:
        return self.db.delete_faculty(faculty_id)

    # ------------------------------------------
    # Room Operations
    # ------------------------------------------
    def get_rooms(self) -> List[Room]:
        return self.db.get_all_rooms()

    def add_room(self, room: Room) -> bool:
        return self.db.create_room(room)

    def update_room(self, room: Room) -> bool:
        return self.db.update_room(room)

    def delete_room(self, room_id: str) -> bool:
        return self.db.delete_room(room_id)

    # ------------------------------------------
    # TimeSlot Operations
    # ------------------------------------------
    def get_timeslots(self) -> List[TimeSlot]:
        return self.db.get_all_timeslots()

    def add_timeslot(self, slot: TimeSlot) -> bool:
        return self.db.create_timeslot(slot)

    def update_timeslot(self, slot: TimeSlot) -> bool:
        return self.db.update_timeslot(slot)

    def delete_timeslot(self, slot_id: str) -> bool:
        return self.db.delete_timeslot(slot_id)

    # ------------------------------------------
    # Helper: Mapping
    # ------------------------------------------
    def get_students_by_subject_map(self) -> Dict[str, List[str]]:
        subjects = self.db.get_all_subjects()
        mapping: Dict[str, List[str]] = {}
        for sub in subjects:
            mapping[sub.subject_id] = self.db.get_students_for_subject(sub.subject_id)
        return mapping

    # ------------------------------------------
    # Exam Operations & Scheduling
    # ------------------------------------------
    def get_all_exams(self) -> List[Exam]:
        return self.db.get_all_exams()

    def clear_exams(self):
        self.db.clear_all_exams()

    def save_schedule(self, exams: List[Exam]):
        """Persists a list of exams into the database."""
        self.db.clear_all_exams()
        for exam in exams:
            self.db.create_exam(exam)

    def generate_timetable(self) -> ScheduleReport:
        """Runs the scheduling engine and persists results into the database."""
        subjects = self.db.get_all_subjects()
        students_map = self.get_students_by_subject_map()
        faculty_list = self.db.get_all_faculty()
        rooms = self.db.get_all_rooms()
        timeslots = self.db.get_all_timeslots()

        report = self.scheduler.generate_schedule(
            subjects=subjects,
            students_by_subject=students_map,
            faculty_list=faculty_list,
            rooms=rooms,
            timeslots=timeslots,
        )

        # Persist scheduled exams in database
        self.db.clear_all_exams()
        for exam in report.scheduled_exams:
            self.db.create_exam(exam)
        for exam in report.unscheduled_exams:
            self.db.create_exam(exam)

        return report

    def validate_current_schedule(self) -> Tuple[bool, List[ValidationResult]]:
        """Validates all scheduled exams currently stored in the database."""
        exams = self.db.get_all_exams()
        students_map = self.get_students_by_subject_map()
        rooms_by_id = {r.room_id: r for r in self.db.get_all_rooms()}
        faculty_by_id = {f.faculty_id: f for f in self.db.get_all_faculty()}
        slots_by_id = {t.slot_id: t for t in self.db.get_all_timeslots()}

        return Validator.validate_full_timetable(
            exams=exams,
            students_by_subject=students_map,
            rooms_by_id=rooms_by_id,
            faculty_by_id=faculty_by_id,
            timeslots_by_id=slots_by_id,
        )

    def export_timetable_to_csv(self, file_path: str) -> bool:
        """Exports the current timetable to CSV."""
        exams = self.db.get_all_exams()
        rooms_by_id = {r.room_id: r for r in self.db.get_all_rooms()}
        faculty_by_id = {f.faculty_id: f for f in self.db.get_all_faculty()}
        slots_by_id = {t.slot_id: t for t in self.db.get_all_timeslots()}
        subs_by_id = {s.subject_id: s for s in self.db.get_all_subjects()}

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Exam ID",
                "Subject Code",
                "Subject Name",
                "Date",
                "Start Time",
                "End Time",
                "Room Name",
                "Room Capacity",
                "Students Enrolled",
                "Invigilator",
                "Status",
            ])
            for e in exams:
                sub = subs_by_id.get(e.subject_id)
                sub_name = sub.name if sub else e.subject_id
                slot = slots_by_id.get(e.slot_id) if e.slot_id else None
                rm = rooms_by_id.get(e.room_id) if e.room_id else None
                fac = faculty_by_id.get(e.faculty_id) if e.faculty_id else None

                writer.writerow([
                    e.exam_id,
                    e.subject_id,
                    sub_name,
                    slot.date if slot else "N/A",
                    slot.start_time if slot else "N/A",
                    slot.end_time if slot else "N/A",
                    rm.name if rm else "N/A",
                    rm.capacity if rm else "N/A",
                    e.student_count,
                    fac.name if fac else "N/A",
                    e.status,
                ])
        return True

    # ------------------------------------------
    # Milestone 8: Functional Evaluation
    # ------------------------------------------
    def evaluate_schedule_functional(self):
        """Runs functional map/filter/reduce pipeline on current schedule."""
        from scheduling.functional_evaluator import evaluate_schedule_functional
        exams = self.db.get_all_exams()
        subjects = self.db.get_all_subjects()
        rooms = {r.room_id: r for r in self.db.get_all_rooms()}
        faculty = {f.faculty_id: f for f in self.db.get_all_faculty()}
        slots = {s.slot_id: s for s in self.db.get_all_timeslots()}
        students_map = {s.subject_id: self.db.get_students_for_subject(s.subject_id) for s in subjects}
        return evaluate_schedule_functional(exams, students_map, rooms, faculty, slots)

    # ------------------------------------------
    # Milestone 9: Multiprocessing Search
    # ------------------------------------------
    def search_parallel_candidates(self, num_candidates: int = 8, max_workers: Optional[int] = None):
        """Executes multi-process parallel candidate search."""
        from scheduling.parallel_scheduler import ParallelScheduler
        subjects = self.db.get_all_subjects()
        rooms = self.db.get_all_rooms()
        faculty = self.db.get_all_faculty()
        slots = self.db.get_all_timeslots()
        students_map = {s.subject_id: self.db.get_students_for_subject(s.subject_id) for s in subjects}

        ps = ParallelScheduler(max_workers=max_workers)
        result = ps.search_best_schedule(
            subjects, students_map, faculty, rooms, slots, num_candidates=num_candidates
        )
        if result.best_schedule:
            self.save_schedule(result.best_schedule)
        return result

    def benchmark_multiprocessing(self, num_candidates: int = 8):
        """Benchmarks sequential (1 core) vs parallel (N cores) execution."""
        from scheduling.parallel_scheduler import ParallelScheduler
        subjects = self.db.get_all_subjects()
        rooms = self.db.get_all_rooms()
        faculty = self.db.get_all_faculty()
        slots = self.db.get_all_timeslots()
        students_map = {s.subject_id: self.db.get_students_for_subject(s.subject_id) for s in subjects}

        ps = ParallelScheduler()
        return ps.benchmark_speedup(
            subjects, students_map, faculty, rooms, slots, num_candidates=num_candidates
        )

    # ------------------------------------------
    # Milestone 10: Symbolic Modeling (SymPy)
    # ------------------------------------------
    def get_symbolic_model(self):
        """Returns SymPy symbolic timetable model."""
        from optimization.symbolic_model import SymbolicTimetableModel
        return SymbolicTimetableModel()

    # ------------------------------------------
    # Milestone 11: Genetic Algorithm Optimization
    # ------------------------------------------
    def optimize_with_genetic_algorithm(self, population_size: int = 30, generations: int = 25, seed: int = 42):
        """Executes Genetic Algorithm optimization and saves best schedule to database."""
        from scheduling.genetic_scheduler import GeneticScheduler
        subjects = self.db.get_all_subjects()
        rooms = self.db.get_all_rooms()
        faculty = self.db.get_all_faculty()
        slots = self.db.get_all_timeslots()
        students_map = {s.subject_id: self.db.get_students_for_subject(s.subject_id) for s in subjects}

        ga = GeneticScheduler(population_size=population_size, generations=generations, random_seed=seed)
        result = ga.optimize(subjects, students_map, faculty, rooms, slots)
        if result.best_schedule and result.is_fully_valid:
            self.save_schedule(result.best_schedule)
        return result

    # ------------------------------------------
    # Milestone 12: Advanced Exports (PDF, Excel)
    # ------------------------------------------
    def export_timetable_to_excel(self, file_path: str) -> str:
        """Exports the current timetable to Microsoft Excel (.xlsx)."""
        from utils.export_manager import ExportManager
        exams = self.db.get_all_exams()
        rooms = {r.room_id: r for r in self.db.get_all_rooms()}
        faculty = {f.faculty_id: f for f in self.db.get_all_faculty()}
        slots = {s.slot_id: s for s in self.db.get_all_timeslots()}
        return ExportManager.export_excel(exams, rooms, faculty, slots, file_path)

    def export_timetable_to_pdf(self, file_path: str) -> str:
        """Exports the current timetable to official PDF format."""
        from utils.export_manager import ExportManager
        exams = self.db.get_all_exams()
        rooms = {r.room_id: r for r in self.db.get_all_rooms()}
        faculty = {f.faculty_id: f for f in self.db.get_all_faculty()}
        slots = {s.slot_id: s for s in self.db.get_all_timeslots()}
        return ExportManager.export_pdf(exams, rooms, faculty, slots, file_path)

