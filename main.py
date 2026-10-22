"""
EXAMOPT — Intelligent Examination Scheduling and Optimization System
SRM Institute of Science and Technology, Tiruchirappalli
Team: Suhas V A, Subaash G, Roshan Albert Shaiju

100% Production Capstone Target: Complete Implementation (Milestones 1–12)
"""
import sys
import argparse
import logging
from config import SYSTEM_NAME, INSTITUTION_NAME, CAMPUS_NAME, VERSION
from services.exam_service import ExamService
from tests.test_scenarios import run_all_scenarios


def setup_logging():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s]: %(message)s",
        datefmt="%H:%M:%S",
    )


def run_cli_demo():
    """Runs a complete end-to-end demonstration in CLI mode."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print("=" * 75)
    print(f"{SYSTEM_NAME}")
    print(f"{INSTITUTION_NAME}, {CAMPUS_NAME}")
    print(f"Version: {VERSION} | Status: 100% Production Capstone Review")
    print("=" * 75)

    service = ExamService()
    print("\n[Step 1/5] Initializing Database & Loading SRM Sample Dataset...")
    stats = service.load_srm_sample_data()
    print(f"  [+] Loaded {stats['subjects']} subjects, {stats['students']} students, {stats['faculty']} faculty,")
    print(f"      {stats['rooms']} rooms, and {stats['timeslots']} time slots.")

    print("\n[Step 2/5] Running Intelligent Scheduling Engine...")
    report = service.generate_timetable()
    print(f"  [+] {report.summary_message}")

    print("\n[Step 3/5] Validating Academic Constraints...")
    is_valid, val_results = service.validate_current_schedule()
    for res in val_results:
        mark = "[PASS]" if res.is_valid else "[FAIL]"
        print(f"    {mark} [{res.status}] {res.message}")

    print("\n[Step 4/5] Generated Examination Timetable:")
    print("-" * 95)
    header = f"{'Exam ID':<10} | {'Subject':<8} | {'Date':<10} | {'Time':<13} | {'Room':<16} | {'Cap':<4} | {'Enr':<4} | {'Invigilator':<18}"
    print(header)
    print("-" * 95)

    rooms = {r.room_id: r for r in service.get_rooms()}
    faculty = {f.faculty_id: f for f in service.get_faculty()}
    slots = {s.slot_id: s for s in service.get_timeslots()}

    for exam in report.scheduled_exams:
        slot = slots.get(exam.slot_id)
        rm = rooms.get(exam.room_id)
        fac = faculty.get(exam.faculty_id)
        print(
            f"{exam.exam_id:<10} | "
            f"{exam.subject_id:<8} | "
            f"{(slot.date if slot else 'N/A'):<10} | "
            f"{(slot.start_time + '-' + slot.end_time if slot else 'N/A'):<13} | "
            f"{(rm.name[:16] if rm else 'N/A'):<16} | "
            f"{(str(rm.capacity) if rm else '-'):<4} | "
            f"{exam.student_count:<4} | "
            f"{(fac.name[:18] if fac else 'N/A'):<18}"
        )
    print("-" * 95)

    print("\n[Step 5/5] Executing 5 Milestone 6 Review Scenarios:")
    print_scenario_results()


def print_scenario_results():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    scenarios = run_all_scenarios()
    passed = 0
    print("\n" + "=" * 80)
    print("EXAMOPT 100% PRODUCTION REVIEW: ACADEMIC CHECKPOINT RESULTS")
    print("=" * 80)
    for sc in scenarios:
        res = "PASS" if sc["passed"] else "FAIL"
        mark = "[PASS]" if sc["passed"] else "[FAIL]"
        if sc["passed"]:
            passed += 1
        print(f"{mark} {sc['scenario']}")
        print(f"       Expected: {sc['expected']}")
        print(f"       Details:  {sc['details']}")
        print("-" * 80)

    total = len(scenarios)
    print(f"TOTAL: {passed}/{total} Scenarios Passed ({passed/total*100:.0f}%)\n")


def run_ga_cli():
    """Runs Genetic Algorithm evolutionary optimization via CLI."""
    service = ExamService()
    service.load_srm_sample_data()
    print("\nRunning Meta-Heuristic Genetic Algorithm (50 Generations)...")
    res = service.optimize_with_genetic_algorithm(population_size=40, generations=50)
    print(f"  [+] Optimization Complete!")
    print(f"  [+] Best Fitness: {res.best_fitness:.4f}")
    print(f"  [+] Hard Constraints Violations: {res.hard_conflicts}")
    print(f"  [+] Soft Penalty Score: {res.soft_penalty:.2f}")
    print(f"  [+] Scheduled Exams: {len(res.best_schedule)}")
    print(f"  [+] Generations Evaluated: {res.generations_run}")


def run_parallel_cli():
    """Runs multiprocessing parallel candidate search via CLI."""
    service = ExamService()
    service.load_srm_sample_data()
    print("\nRunning Multi-Core Parallel Candidate Search...")
    res = service.search_parallel_candidates(num_candidates=8)
    print(f"  [+] Evaluated {res.total_candidates_evaluated} candidates across {res.workers_used} CPU workers in {res.elapsed_time_seconds:.4f}s.")
    print(f"  [+] Selected Best Candidate ID: {res.best_candidate_id}")
    print(f"  [+] Fitness: {res.best_fitness:.4f} | Soft Penalty: {res.best_soft_penalty:.2f}")


def run_benchmark_cli():
    """Runs multiprocessing vs sequential benchmark via CLI."""
    service = ExamService()
    service.load_srm_sample_data()
    print("\nExecuting CPU Multi-Core Benchmarking (Sequential vs Parallel)...")
    bm = service.benchmark_multiprocessing(num_candidates=8)
    print(f"  [+] CPU Logical Cores: {bm['cpu_cores_detected']}")
    print(f"  [+] Workers Deployed: {bm['workers_deployed']}")
    print(f"  [+] Sequential (1 Core): {bm['sequential_time_seconds']:.4f}s")
    print(f"  [+] Parallel ({bm['workers_deployed']} Cores): {bm['parallel_time_seconds']:.4f}s")
    print(f"  [+] Speedup Factor: {bm['speedup_factor']:.2f}x (Efficiency: {bm['efficiency_percentage']:.1f}%)")


def run_export_all_cli():
    """Exports timetable to CSV, Excel, and PDF."""
    service = ExamService()
    service.load_srm_sample_data()
    service.generate_timetable()
    c = service.export_timetable_to_csv("exports/schedule.csv")
    x = service.export_timetable_to_excel("exports/schedule.xlsx")
    p = service.export_timetable_to_pdf("exports/schedule.pdf")
    print(f"\n[+] Timetable exported successfully to 3 formats:")
    print(f"    • CSV:   {c}")
    print(f"    • Excel: {x}")
    print(f"    • PDF:   {p}")


def main():
    parser = argparse.ArgumentParser(description="ExamOpt — Intelligent Examination Scheduling System")
    parser.add_argument("--cli", action="store_true", help="Run end-to-end demonstration in CLI mode")
    parser.add_argument("--scenarios", action="store_true", help="Run the 10 Capstone review scenarios")
    parser.add_argument("--ga", action="store_true", help="Run Genetic Algorithm optimizer")
    parser.add_argument("--parallel", action="store_true", help="Run multiprocessing candidate search")
    parser.add_argument("--benchmark", action="store_true", help="Run multiprocessing vs sequential benchmark")
    parser.add_argument("--export-all", action="store_true", help="Export timetable to CSV, Excel (.xlsx), and PDF (.pdf)")
    parser.add_argument("--server", action="store_true", help="Start standalone TCP socket server daemon")
    parser.add_argument("--port", type=int, default=8080, help="TCP server port (default: 8080)")
    parser.add_argument("--verify-100", action="store_true", help="Comprehensive 100%% Milestone verification")
    parser.add_argument(
        "--theme",
        choices=["modern", "classic"],
        default="modern",
        help="GUI visual theme: 'modern' (sleek obsidian dark slate) or 'classic' (original standard theme)",
    )
    parser.add_argument("--classic", action="store_true", help="Shortcut to launch the classic GUI")
    parser.add_argument("--modern", action="store_true", help="Shortcut to launch the modern GUI")
    args = parser.parse_args()

    setup_logging()

    if args.server:
        from networking.exam_server import run_standalone_server
        run_standalone_server(port=args.port)
    elif args.verify_100 or args.scenarios:
        print_scenario_results()
    elif args.ga:
        run_ga_cli()
    elif args.parallel:
        run_parallel_cli()
    elif args.benchmark:
        run_benchmark_cli()
    elif args.export_all:
        run_export_all_cli()
    elif args.cli:
        run_cli_demo()
    else:
        # Determine theme
        selected_theme = "classic" if args.classic else ("modern" if args.modern else args.theme)
        try:
            if selected_theme == "classic":
                from gui.app import start_gui
                start_gui()
            else:
                from gui.modern_app import start_modern_gui
                start_modern_gui()
        except Exception as e:
            print(f"Notice: Graphical environment unavailable or error ({e}). Running in CLI mode.\n")
            run_cli_demo()


if __name__ == "__main__":
    main()

