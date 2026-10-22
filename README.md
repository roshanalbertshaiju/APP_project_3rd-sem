# EXAMOPT — INTELLIGENT EXAMINATION SCHEDULING AND OPTIMIZATION SYSTEM

**Institution**: SRM Institute of Science and Technology, Tiruchirappalli Campus  
**Project Team**:
* Suhas V A
* Subaash G
* Roshan Albert Shaiju

**Technology Stack**: Python 3, SQLite 3, Tkinter GUI, Unittest, SymPy, openpyxl, reportlab  
**Current Milestone**: **100% Production Final (Milestones 1–12 Fully Implemented)**  

---

## 📌 Project Overview

**ExamOpt** is an automated, intelligent examination timetable scheduling and optimization platform developed for university academic operations. It resolves complex academic constraints—such as student exam collisions, room seating capacity thresholds, invigilator clashes, and facility availability—to generate conflict-free, feasible timetables.

The system is architected with strict loose coupling:
```text
               ┌──────────────────────┐
               │     Tkinter GUI      │
               └──────────┬───────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │  Application Service │
               └──────────┬───────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
   ┌──────────────────┐      ┌──────────────────┐
   │    Scheduler     │◄────►│    Validator     │
   └─────────┬────────┘      └─────────┬────────┘
             │                         │
             ▼                         ▼
   ┌──────────────────┐      ┌──────────────────┐
   │  Room Allocator  │      │ SQLite Database  │
   └──────────────────┘      └──────────────────┘
```

---

## 🚀 Quick Start & Execution

### 1. Launch via Windows Batch Files (.bat)
Double-click whichever interface you prefer directly from the project folder:
* **`run_modern_gui.bat`** — Launches the **Modern Minimalist Studio** (sleek obsidian dark slate, responsive sidebar navigation, 7 clean role-based tabs, and academic review suite).
* **`run_classic_gui.bat`** — Launches the **Classic University Theme** (clean blue top notebook tab layout with 7 production tabs).
* **`run_examopt.bat`** — Default launcher (defaults to Modern Minimalist Studio).

### 2. Launch via Python CLI
```bash
# Launch Modern Minimalist GUI (Default)
python main.py
python main.py --theme modern

# Launch Classic GUI
python main.py --theme classic
```
* Use **⚡ Load SRM Sample Dataset** to populate realistic course, student, faculty, and room records with one click.
* Click **🚀 Quick Generate Timetable** to run the scheduling engine and display the conflict-free timetable.
* Click **🧬 AI Optimize (GA)** in the Timetable tab to evolve schedules with soft constraint minimization.
* Click **🔍 Validate** to run the validation engine on the current schedule.
* Click **📐 Soft Quality Score** to inspect functional evaluation metrics (room utilization, student gaps, faculty load).
* Click **📊 Excel** or **📄 PDF** to generate official examination publications.
* Access **🧪 Academic Review & Viva Suite** for 10 Capstone scenarios, CPU multi-core speedup benchmarking, and SymPy formulation.
* Click **🌐 Network Server** to toggle the TCP Socket Daemon and test ping latency.

### 2. Run End-to-End CLI Demonstration
```bash
python main.py --cli
```
Executes the full pipeline: initializes SQLite, populates sample data, runs the scheduling engine, validates all academic constraints, displays the generated timetable in a formatted table, and runs the 5 review scenarios.

### 3. Run Milestone 6 Review Scenarios
```bash
python main.py --scenarios
```

### 4. Run Automated Test Suite
```bash
python -m unittest discover tests -v
```

---

## 📋 100% Production Implementation Status

```text
CURRENT PROJECT STATUS: 100% (PRODUCTION CAPSTONE COMPLETE)

Completed Milestones 1–12:
✓ Milestone 1–2: Foundation & Relational Schema (SQLite 3NF, PRAGMA foreign_keys = ON, ACID context managers)
✓ Milestone 3: Pure Domain Layer & Serialization (to_dict/from_dict for JSON RPC)
✓ Milestone 4: 6-Point Academic Constraint Validator (Clashes, capacity, availability, room double-booking)
✓ Milestone 5: Heuristic Scheduler & Best-Fit Seating (MRV heuristic + bin-packing room allocator)
✓ Milestone 6: Dual-Theme Desktop GUI & 5 Baseline Scenarios (Modern Obsidian & Classic University)
✓ Milestone 7: Distributed TCP Socket Client-Server (Length-prefixed JSON RPC daemon + client)
✓ Milestone 8: Functional Programming Pipelines (map/filter/reduce soft penalty evaluation)
✓ Milestone 9: Multiprocessing Engine (ProcessPoolExecutor bypassing CPython GIL across CPU cores)
✓ Milestone 10: Symbolic Mathematical Optimization (SymPy analytical gradients & penalty matrices)
✓ Milestone 11: Meta-Heuristic Evolutionary Optimization (Genetic Algorithm chromosome evolution)
✓ Milestone 12: Production Exports & 53-Test Suite (Official PDF, styled Excel .xlsx, CSV + 10 Scenarios)
```

---

## 🧪 100% Capstone Review Scenarios Verified

| Scenario | Description / Technology | Expected Status | Result |
| :--- | :--- | :--- | :---: |
| **Test 1** | Valid SRM sample dataset $\rightarrow$ Full timetable generated | `VALID` | **PASS** |
| **Test 2** | Two exams with shared students in same slot $\rightarrow$ Conflict rejected | `CONFLICT` | **PASS** |
| **Test 3** | Room capacity insufficient for enrolled cohort $\rightarrow$ Deficit flagged | `CAPACITY_EXCEEDED` | **PASS** |
| **Test 4** | Same room assigned twice in same time slot $\rightarrow$ Rejection | `DUPLICATE_BOOKING` | **PASS** |
| **Test 5** | Exam assigned to room under repair or faculty on leave $\rightarrow$ Rejected | `ROOM_UNAVAILABLE` / `FACULTY_UNAVAILABLE` | **PASS** |
| **Test 6** | Functional Programming Pipeline (`map`/`filter`/`reduce`) | Fitness & soft penalty evaluated | **PASS** |
| **Test 7** | Multiprocessing Candidate Engine (`ProcessPoolExecutor`) | 0-clash schedule across CPU processes | **PASS** |
| **Test 8** | SymPy Symbolic Modeling ($\mathcal{Z} = \mathbf{w}^T \mathbf{P}$, $\partial \mathcal{Z}/\partial w_i$) | Analytical gradients verified | **PASS** |
| **Test 9** | Meta-Heuristic Genetic Algorithm (GA evolution) | 0 conflicts, minimized soft penalty | **PASS** |
| **Test 10**| Distributed TCP Socket Client-Server RPC Roundtrip | Binary framed JSON payload returned | **PASS** |

---

## 📁 Directory Structure

```text
ExamOpt/
│
├── main.py                     # Application entry point (GUI, CLI, Sockets & Optimization)
├── config.py                   # Global constants, codes, and paths
├── README.md                   # Project documentation and milestone report
│
├── models/                     # Pure Python domain models
│   ├── student.py              # Student (id, name, department, semester)
│   ├── subject.py              # Subject (id, name, department, duration)
│   ├── faculty.py              # Faculty (id, name, department, is_available)
│   ├── room.py                 # Room (id, name, capacity, is_available)
│   ├── timeslot.py             # TimeSlot (id, date, start_time, end_time, is_available)
│   ├── enrollment.py           # Student-Subject enrollment relation
│   └── exam.py                 # Exam requirement and scheduled exam assignment
│
├── database/                   # SQLite persistence layer (3NF)
│   ├── schema.py               # Table DDL definitions with foreign keys
│   └── database.py             # Full CRUD operations for all entities
│
├── validation/                 # Constraint Validation Engine
│   └── validator.py            # Multi-constraint detection and status codes
│
├── scheduling/                 # Scheduling & Optimization Engines
│   ├── room_allocator.py       # Best-Fit capacity matcher
│   ├── scheduler.py            # Heuristic MRV timetable generator
│   ├── functional_evaluator.py # Milestone 8: map/filter/reduce pipelines
│   ├── parallel_scheduler.py   # Milestone 9: ProcessPoolExecutor (GIL bypass)
│   └── genetic_scheduler.py    # Milestone 11: Meta-heuristic Genetic Algorithm
│
├── networking/                 # Milestone 7: Distributed Socket Layer
│   ├── protocol.py             # 4-byte length-prefixed JSON wire framing
│   ├── exam_server.py          # Threaded TCP Socket Server daemon
│   └── exam_client.py          # High-level client API & RPC wrapper
│
├── optimization/               # Milestone 10: Symbolic Mathematical Modeling
│   └── symbolic_model.py       # SymPy objective formulation & sensitivity analysis
│
├── services/                   # Application Service Layer
│   └── exam_service.py         # Unified facade for GUI, CLI, and Socket Server
│
├── gui/                        # Tkinter Modern Obsidian & Classic Themes
│   ├── app.py                  # Classic University notebook window
│   ├── modern_app.py           # Sleek Obsidian Studio with sidebar navigation
│   └── views/                  # Modular view components
│       ├── timetable_view.py   # Timetable viewer & 3-format exports
│       ├── genetic_view.py     # Live GA convergence chart & controls
│       ├── network_view.py     # TCP socket server control & wire inspector
│       ├── benchmark_view.py   # Multi-core CPU profiling & speedup chart
│       ├── student_view.py     # Student & enrollment management
│       ├── subject_view.py     # Subject management
│       ├── faculty_view.py     # Faculty management
│       ├── room_view.py        # Room management
│       ├── timeslot_view.py    # Session management
│       └── verification_view.py# 10 Capstone Review Scenarios viewer
│
├── utils/                      # Helper utilities
│   ├── helpers.py              # Formatting & validation helpers
│   ├── sample_data.py          # SRM IST Tiruchirappalli sample datasets
│   └── export_manager.py       # Milestone 12: PDF, Excel (.xlsx), CSV exports
│
└── tests/                      # Automated Verification Suite (53 automated tests)
    ├── test_crud.py            # SQLite CRUD tests
    ├── test_validator.py       # Constraint validation tests
    ├── test_scheduler.py       # Heuristic scheduler tests
    ├── test_scenarios.py       # 10 Capstone Review Scenarios
    ├── test_functional.py      # Milestone 8: map/filter/reduce tests
    ├── test_multiprocessing.py # Milestone 9: ProcessPoolExecutor tests
    ├── test_sympy.py           # Milestone 10: SymPy symbolic model tests
    ├── test_genetic.py         # Milestone 11: Genetic algorithm tests
    ├── test_sockets.py         # Milestone 7: TCP socket tests
    └── test_exports.py         # Milestone 12: PDF & Excel export tests
```

#   A P P _ p r o j e c t _ 3 r d - s e m  
 