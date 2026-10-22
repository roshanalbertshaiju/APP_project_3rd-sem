"""
Capstone Academic Review Checkpoint Scenarios (100% Production Target)
SRM Institute of Science and Technology, Tiruchirappalli
Authors: Suhas V A, Subaash G, Roshan Albert Shaiju

Test 1: Valid examination data -> Timetable generated
Test 2: Two exams conflict for students -> Conflict detected
Test 3: Room capacity insufficient -> Capacity violation detected
Test 4: Same room assigned twice -> Duplicate booking detected
Test 5: Unavailable faculty/room -> Assignment rejected
"""

import unittest
from typing import List, Dict, Any

from config import ValidationCode, ScheduleCode
from database.database import Database
from models.student import Student
from models.subject import Subject
from models.faculty import Faculty
from models.room import Room
from models.timeslot import TimeSlot
from models.exam import Exam
from validation.validator import Validator
from scheduling.scheduler import Scheduler
from scheduling.room_allocator import RoomAllocator
from utils.sample_data import populate_srm_sample_data


def run_scenario_1() -> Dict[str, Any]:
    """Test 1: Valid examination data -> Timetable generated"""
    db = Database(":memory:")
    populate_srm_sample_data(db)

    subjects = db.get_all_subjects()
    rooms = db.get_all_rooms()
    faculty = db.get_all_faculty()
    timeslots = db.get_all_timeslots()
    students_map = {s.subject_id: db.get_students_for_subject(s.subject_id) for s in subjects}

    scheduler = Scheduler()
    report = scheduler.generate_schedule(subjects, students_map, faculty, rooms, timeslots)

    rooms_by_id = {r.room_id: r for r in rooms}
    faculty_by_id = {f.faculty_id: f for f in faculty}
    slots_by_id = {t.slot_id: t for t in timeslots}

    is_valid, results = Validator.validate_full_timetable(
        report.scheduled_exams, students_map, rooms_by_id, faculty_by_id, slots_by_id
    )

    passed = (
        report.is_complete
        and report.scheduled_count == len(subjects)
        and is_valid
        and len(report.unscheduled_exams) == 0
    )

    return {
        "scenario": "Test 1: Valid examination data",
        "expected": "Conflict-free timetable generated for all subjects",
        "passed": passed,
        "details": f"Scheduled {report.scheduled_count}/{len(subjects)} subjects. Full validation passed: {is_valid}.",
    }


def run_scenario_2() -> Dict[str, Any]:
    """Test 2: Two exams conflict for students -> Conflict detected"""
    # Setup: 2 subjects with overlapping students assigned to the same time slot
    students_by_subject = {
        "CS301": ["RA01", "RA02", "RA03", "RA04"],
        "CS302": ["RA03", "RA04", "RA05", "RA06"],  # Overlapping students: RA03, RA04
    }
    rooms = {"R1": Room("R1", "LH 101", 50), "R2": Room("R2", "LH 102", 50)}
    faculty = {"F1": Faculty("F1", "Dr. Raman", "CSE"), "F2": Faculty("F2", "Dr. Priya", "CSE")}
    timeslots = {"TS1": TimeSlot("TS1", "2026-10-10", "09:30", "12:30")}

    exam1 = Exam("EX_CS301", "CS301", "TS1", "R1", "F1", student_count=4)
    exam2 = Exam("EX_CS302", "CS302", "TS1", "R2", "F2", student_count=4)

    # Validate exam2 against already scheduled exam1
    res = Validator.validate_assignment(exam2, [exam1], students_by_subject, rooms, faculty, timeslots)

    passed = (not res.is_valid) and (res.status == ValidationCode.CONFLICT) and ("student" in res.message.lower())

    return {
        "scenario": "Test 2: Two exams conflict for students",
        "expected": "Conflict detected (Status: CONFLICT)",
        "passed": passed,
        "details": f"Status: {res.status}. Message: {res.message}",
    }


def run_scenario_3() -> Dict[str, Any]:
    """Test 3: Room capacity insufficient -> Capacity violation detected"""
    students_by_subject = {
        "CS301": [f"RA{i}" for i in range(1, 55)],  # 54 students
    }
    rooms = {"R_TINY": Room("R_TINY", "Small Lab", capacity=30)}  # Capacity: 30
    faculty = {"F1": Faculty("F1", "Dr. Raman", "CSE")}
    timeslots = {"TS1": TimeSlot("TS1", "2026-10-10", "09:30", "12:30")}

    exam = Exam("EX_CS301", "CS301", "TS1", "R_TINY", "F1", student_count=54)

    res = Validator.validate_assignment(exam, [], students_by_subject, rooms, faculty, timeslots)

    passed = (not res.is_valid) and (res.status == ValidationCode.CAPACITY_EXCEEDED)

    return {
        "scenario": "Test 3: Room capacity insufficient",
        "expected": "Capacity violation detected (Status: CAPACITY_EXCEEDED)",
        "passed": passed,
        "details": f"Status: {res.status}. Message: {res.message}",
    }


def run_scenario_4() -> Dict[str, Any]:
    """Test 4: Same room assigned twice -> Duplicate booking detected"""
    students_by_subject = {
        "CS301": [f"RA{i}" for i in range(1, 20)],
        "EC301": [f"EC{i}" for i in range(1, 20)],
    }
    rooms = {"R1": Room("R1", "Main Hall", capacity=100)}
    faculty = {"F1": Faculty("F1", "Dr. Raman", "CSE"), "F2": Faculty("F2", "Dr. Suresh", "ECE")}
    timeslots = {"TS1": TimeSlot("TS1", "2026-10-10", "09:30", "12:30")}

    exam1 = Exam("EX_CS301", "CS301", "TS1", "R1", "F1", student_count=19)
    # Different exam and faculty, but SAME room R1 in SAME timeslot TS1
    exam2 = Exam("EX_EC301", "EC301", "TS1", "R1", "F2", student_count=19)

    res = Validator.validate_assignment(exam2, [exam1], students_by_subject, rooms, faculty, timeslots)

    passed = (not res.is_valid) and (res.status == ValidationCode.DUPLICATE_BOOKING)

    return {
        "scenario": "Test 4: Same room assigned twice",
        "expected": "Duplicate booking detected (Status: DUPLICATE_BOOKING)",
        "passed": passed,
        "details": f"Status: {res.status}. Message: {res.message}",
    }


def run_scenario_5() -> Dict[str, Any]:
    """Test 5: Unavailable faculty/room -> Assignment rejected"""
    students_by_subject = {"CS301": ["RA01", "RA02"]}
    rooms = {
        "R_AVAIL": Room("R_AVAIL", "Hall 1", 50, is_available=True),
        "R_CLOSED": Room("R_CLOSED", "Repair Hall", 50, is_available=False),
    }
    faculty = {
        "F_LEAVE": Faculty("F_LEAVE", "Dr. Leave", "CSE", is_available=False),
        "F_ACTIVE": Faculty("F_ACTIVE", "Dr. Active", "CSE", is_available=True),
    }
    timeslots = {"TS1": TimeSlot("TS1", "2026-10-10", "09:30", "12:30", is_available=True)}

    # Sub-test A: Unavailable room
    exam_bad_room = Exam("EX_A", "CS301", "TS1", "R_CLOSED", "F_ACTIVE", student_count=2)
    res_room = Validator.validate_assignment(exam_bad_room, [], students_by_subject, rooms, faculty, timeslots)

    # Sub-test B: Unavailable faculty
    exam_bad_faculty = Exam("EX_B", "CS301", "TS1", "R_AVAIL", "F_LEAVE", student_count=2)
    res_faculty = Validator.validate_assignment(exam_bad_faculty, [], students_by_subject, rooms, faculty, timeslots)

    passed = (
        (not res_room.is_valid and res_room.status == ValidationCode.ROOM_UNAVAILABLE)
        and (not res_faculty.is_valid and res_faculty.status == ValidationCode.FACULTY_UNAVAILABLE)
    )

    return {
        "scenario": "Test 5: Unavailable faculty/room",
        "expected": "Assignments rejected (Status: ROOM_UNAVAILABLE / FACULTY_UNAVAILABLE)",
        "passed": passed,
        "details": f"Room check: {res_room.status}. Faculty check: {res_faculty.status}.",
    }


def run_scenario_6() -> Dict[str, Any]:
    """Test 6: Functional Programming Evaluation Pipeline (map/filter/reduce)"""
    from scheduling.functional_evaluator import evaluate_schedule_functional
    db = Database(":memory:")
    populate_srm_sample_data(db)
    subjects = db.get_all_subjects()
    rooms = {r.room_id: r for r in db.get_all_rooms()}
    faculty = {f.faculty_id: f for f in db.get_all_faculty()}
    slots = {s.slot_id: s for s in db.get_all_timeslots()}
    students_map = {s.subject_id: db.get_students_for_subject(s.subject_id) for s in subjects}

    scheduler = Scheduler()
    report = scheduler.generate_schedule(subjects, students_map, list(faculty.values()), list(rooms.values()), list(slots.values()))

    eval_report = evaluate_schedule_functional(report.scheduled_exams, students_map, rooms, faculty, slots)
    passed = eval_report.fitness_score > 0 and eval_report.total_penalty >= 0

    return {
        "scenario": "Test 6: Functional Pipeline (map/filter/reduce)",
        "expected": "Pure functional evaluation computes fitness & soft penalties",
        "passed": passed,
        "details": f"Fitness: {eval_report.fitness_score:.2f}, Soft Penalty: {eval_report.total_penalty:.1f}, Room Util: {eval_report.average_room_utilization_pct:.1f}%.",
    }


def run_scenario_7() -> Dict[str, Any]:
    """Test 7: Multiprocessing Parallel Candidate Search (Bypassing GIL)"""
    from scheduling.parallel_scheduler import ParallelScheduler
    db = Database(":memory:")
    populate_srm_sample_data(db)
    subjects = db.get_all_subjects()
    rooms = db.get_all_rooms()
    faculty = db.get_all_faculty()
    slots = db.get_all_timeslots()
    students_map = {s.subject_id: db.get_students_for_subject(s.subject_id) for s in subjects}

    ps = ParallelScheduler(max_workers=2)
    res = ps.search_best_schedule(subjects, students_map, faculty, rooms, slots, num_candidates=4)
    passed = (res.total_candidates_evaluated == 4 and res.hard_conflicts == 0 and len(res.best_schedule) == len(subjects))

    return {
        "scenario": "Test 7: Multiprocessing Search (ProcessPoolExecutor)",
        "expected": "Multi-core search discovers 0-clash schedule across processes",
        "passed": passed,
        "details": f"Evaluated {res.total_candidates_evaluated} candidates in {res.elapsed_time_seconds:.3f}s. Best Candidate ID: {res.best_candidate_id}.",
    }


def run_scenario_8() -> Dict[str, Any]:
    """Test 8: SymPy Symbolic Mathematical Modeling & Sensitivity Analysis"""
    from optimization.symbolic_model import SymbolicTimetableModel
    model = SymbolicTimetableModel()
    expr = model.get_objective_expression()
    grads = model.compute_gradients()
    sens = model.perform_sensitivity_analysis({"consecutive": 4, "faculty": 1, "waste": 30})

    passed = (
        "M_hard" in str(expr)
        and str(grads["dZ_dw_consec"]) == "P_consec"
        and sens["base_loss"] > 0
    )

    return {
        "scenario": "Test 8: SymPy Symbolic Mathematical Modeling",
        "expected": "Symbolic loss formulation & partial derivative sensitivity analysis",
        "passed": passed,
        "details": f"Objective: {expr}. dZ/dw_consec = {grads['dZ_dw_consec']}. Base Loss: {sens['base_loss']}.",
    }


def run_scenario_9() -> Dict[str, Any]:
    """Test 9: Meta-Heuristic Genetic Algorithm (Evolutionary Optimization)"""
    from scheduling.genetic_scheduler import GeneticScheduler
    db = Database(":memory:")
    populate_srm_sample_data(db)
    subjects = db.get_all_subjects()
    rooms = db.get_all_rooms()
    faculty = db.get_all_faculty()
    slots = db.get_all_timeslots()
    students_map = {s.subject_id: db.get_students_for_subject(s.subject_id) for s in subjects}

    ga = GeneticScheduler(population_size=15, generations=10, random_seed=42)
    res = ga.optimize(subjects, students_map, faculty, rooms, slots)
    passed = res.is_fully_valid and res.hard_conflicts == 0 and len(res.best_schedule) == len(subjects)

    return {
        "scenario": "Test 9: Meta-Heuristic Genetic Algorithm (GA)",
        "expected": "Evolutionary chromosome crossover/mutation yields optimal timetable",
        "passed": passed,
        "details": f"Generations: {res.generations_run}, Fitness: {res.best_fitness:.2f}, Conflicts: {res.hard_conflicts}.",
    }


def run_scenario_10() -> Dict[str, Any]:
    """Test 10: Distributed TCP Socket Client-Server Roundtrip"""
    import time
    from services.exam_service import ExamService
    from networking.exam_server import ExamSocketServer
    from networking.exam_client import ExamSocketClient

    db = Database(":memory:")
    service = ExamService(db)
    service.load_srm_sample_data()

    test_port = 9271
    server = ExamSocketServer("127.0.0.1", test_port, service)
    server.start_in_background()
    time.sleep(0.2)

    try:
        with ExamSocketClient("127.0.0.1", test_port) as client:
            ok, latency_ms, data = client.ping()
            res = client.generate_schedule()
            passed = ok and res.get("success") and res.get("scheduled_count") > 0
            details = f"Ping Latency: {latency_ms:.2f}ms. Remote Scheduled: {res.get('scheduled_count')} exams."
    finally:
        server.stop()

    return {
        "scenario": "Test 10: Distributed TCP Socket Client-Server",
        "expected": "Binary length-prefixed JSON RPC message roundtrip over TCP socket",
        "passed": passed,
        "details": details,
    }


def run_all_scenarios() -> List[Dict[str, Any]]:
    """Runs all 10 review scenarios covering 100% implementation."""
    return [
        run_scenario_1(),
        run_scenario_2(),
        run_scenario_3(),
        run_scenario_4(),
        run_scenario_5(),
        run_scenario_6(),
        run_scenario_7(),
        run_scenario_8(),
        run_scenario_9(),
        run_scenario_10(),
    ]


class TestScenarios(unittest.TestCase):
    """Unittest suite wrapping the 10 Capstone Review Scenarios."""

    def test_scenario_1_valid_data(self):
        res = run_scenario_1()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_2_student_conflict(self):
        res = run_scenario_2()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_3_capacity_insufficient(self):
        res = run_scenario_3()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_4_duplicate_booking(self):
        res = run_scenario_4()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_5_unavailable_entities(self):
        res = run_scenario_5()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_6_functional_pipeline(self):
        res = run_scenario_6()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_7_multiprocessing(self):
        res = run_scenario_7()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_8_sympy_symbolic(self):
        res = run_scenario_8()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_9_genetic_algorithm(self):
        res = run_scenario_9()
        self.assertTrue(res["passed"], res["details"])

    def test_scenario_10_socket_roundtrip(self):
        res = run_scenario_10()
        self.assertTrue(res["passed"], res["details"])


if __name__ == "__main__":
    unittest.main()

