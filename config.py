"""
ExamOpt — Configuration and Global Constants
SRM Institute of Science and Technology, Tiruchirappalli
Project Team: Suhas V A, Subaash G, Roshan Albert Shaiju
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = os.environ.get("EXAMOPT_DB", str(BASE_DIR / "examopt.db"))

# Academic Info
INSTITUTION_NAME = "SRM Institute of Science and Technology"
CAMPUS_NAME = "Tiruchirappalli Campus"
SYSTEM_NAME = "ExamOpt — Intelligent Examination Scheduling and Optimization System"
VERSION = "1.0.0 (100% Production Implementation)"

# Network / Socket Configuration
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 8080
SOCKET_BUFFER_SIZE = 8192
SOCKET_TIMEOUT = 10.0

# Multiprocessing Configuration
DEFAULT_PARALLEL_WORKERS = 4
DEFAULT_CANDIDATE_SCHEDULES = 8

# Genetic Algorithm Optimization Parameters
GA_DEFAULT_POPULATION_SIZE = 40
GA_DEFAULT_GENERATIONS = 50
GA_DEFAULT_MUTATION_RATE = 0.15
GA_DEFAULT_ELITISM_COUNT = 2
GA_TOURNAMENT_SIZE = 3

# Soft Constraint Weights (SymPy & Penalty Evaluation)
WEIGHT_STUDENT_CONSECUTIVE = 10.0   # Penalty per student with back-to-back exams
WEIGHT_FACULTY_OVERLOAD = 15.0       # Penalty per faculty with >1 duty per day
WEIGHT_ROOM_SEAT_WASTE = 0.5         # Penalty per wasted empty seat
HARD_VIOLATION_PENALTY = 1000.0      # Heavy penalty per hard constraint breach

# Constraint Validation Status Codes
class ValidationCode:
    VALID = "VALID"
    INVALID = "INVALID"
    CONFLICT = "CONFLICT"
    CAPACITY_EXCEEDED = "CAPACITY_EXCEEDED"
    ROOM_UNAVAILABLE = "ROOM_UNAVAILABLE"
    FACULTY_UNAVAILABLE = "FACULTY_UNAVAILABLE"
    DUPLICATE_BOOKING = "DUPLICATE_BOOKING"
    TIMESLOT_UNAVAILABLE = "TIMESLOT_UNAVAILABLE"

# Scheduling Status Codes
class ScheduleCode:
    SUCCESSFULLY_SCHEDULED = "Successfully Scheduled"
    UNSCHEDULED = "Unscheduled"
    CONFLICT = "Conflict"
    NO_AVAILABLE_ROOM = "No Available Room"
    NO_AVAILABLE_TIME_SLOT = "No Available Time Slot"
    FACULTY_UNAVAILABLE = "Faculty Unavailable"

