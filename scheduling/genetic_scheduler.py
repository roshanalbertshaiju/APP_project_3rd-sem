"""
ExamOpt — Meta-Heuristic Genetic Algorithm Scheduler
Milestone 11: Evolutionary Optimization (Chromosome, Crossover, Mutation, Elitism)
SRM Institute of Science and Technology, Tiruchirappalli

Optimizes examination timetables for both hard constraint feasibility (0 clashes)
and soft constraint quality (minimal student stress, balanced faculty duty, optimal room usage).
"""
import random
import copy
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any

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
from config import (
    GA_DEFAULT_POPULATION_SIZE,
    GA_DEFAULT_GENERATIONS,
    GA_DEFAULT_MUTATION_RATE,
    GA_DEFAULT_ELITISM_COUNT,
    GA_TOURNAMENT_SIZE,
    HARD_VIOLATION_PENALTY,
)


@dataclass
class GeneticOptimizationResult:
    """Encapsulates the final outcome of the Genetic Algorithm optimization."""
    best_schedule: List[Exam]
    best_fitness: float
    initial_fitness: float
    hard_conflicts: int
    soft_penalty: float
    generations_run: int
    history: List[Dict[str, Any]]
    evaluation_report: Optional[FunctionalEvaluationReport] = None
    is_fully_valid: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "best_fitness": round(self.best_fitness, 4),
            "initial_fitness": round(self.initial_fitness, 4),
            "hard_conflicts": self.hard_conflicts,
            "soft_penalty": round(self.soft_penalty, 2),
            "generations_run": self.generations_run,
            "is_fully_valid": self.is_fully_valid,
            "scheduled_count": len(self.best_schedule),
            "evaluation_report": self.evaluation_report.to_dict() if self.evaluation_report else None,
            "history_summary": [
                {
                    "gen": h["generation"],
                    "best_fitness": round(h["best_fitness"], 4),
                    "hard_conflicts": h["hard_conflicts"],
                }
                for h in self.history[:: max(1, len(self.history) // 10)]
            ],
        }


class GeneticScheduler:
    """
    Genetic Algorithm optimizer for Examination Timetabling.
    Evolves a population of candidate timetables over multiple generations.
    """

    def __init__(
        self,
        population_size: int = GA_DEFAULT_POPULATION_SIZE,
        generations: int = GA_DEFAULT_GENERATIONS,
        mutation_rate: float = GA_DEFAULT_MUTATION_RATE,
        elitism_count: int = GA_DEFAULT_ELITISM_COUNT,
        tournament_size: int = GA_TOURNAMENT_SIZE,
        random_seed: Optional[int] = 42,
    ):
        self.population_size = max(10, population_size)
        self.generations = max(5, generations)
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count
        self.tournament_size = tournament_size
        if random_seed is not None:
            random.seed(random_seed)

    def optimize(
        self,
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        faculty: List[Faculty],
        rooms: List[Room],
        timeslots: List[TimeSlot],
    ) -> GeneticOptimizationResult:
        """Runs the evolutionary search loop to optimize timetable allocation."""
        if not subjects or not timeslots or not rooms:
            return GeneticOptimizationResult(
                best_schedule=[],
                best_fitness=0.0,
                initial_fitness=0.0,
                hard_conflicts=0,
                soft_penalty=0.0,
                generations_run=0,
                history=[],
                is_fully_valid=False,
            )

        # Flexible auto-detection if faculty and rooms are swapped
        if faculty and hasattr(faculty[0], "room_id"):
            faculty, rooms = rooms, faculty

        rooms_by_id = {r.room_id: r for r in rooms}
        faculty_by_id = {f.faculty_id: f for f in faculty}
        slots_by_id = {s.slot_id: s for s in timeslots}

        # Available pool
        avail_rooms = [r for r in rooms if r.is_available]
        avail_faculty = [f for f in faculty if f.is_available]
        avail_slots = [s for s in timeslots if s.is_available]

        # 1. Initialize Population
        population = self._initialize_population(
            subjects, students_by_subject, avail_rooms, avail_faculty, avail_slots
        )

        history: List[Dict[str, Any]] = []

        # Evaluate Initial Population
        evaluated_pop = [
            (
                ind,
                self._calculate_fitness(
                    ind, subjects, students_by_subject, rooms_by_id, faculty_by_id, slots_by_id
                ),
            )
            for ind in population
        ]
        evaluated_pop.sort(key=lambda x: x[1][0], reverse=True)

        initial_best_fitness = evaluated_pop[0][1][0]

        # 2. Generational Loop
        for gen in range(1, self.generations + 1):
            next_generation = []

            # Elitism: retain top individuals
            for i in range(min(self.elitism_count, len(evaluated_pop))):
                next_generation.append(copy.deepcopy(evaluated_pop[i][0]))

            # Breeding loop
            while len(next_generation) < self.population_size:
                parent1 = self._tournament_select(evaluated_pop)
                parent2 = self._tournament_select(evaluated_pop)

                child = self._crossover(parent1, parent2, subjects)
                child = self._mutate(
                    child, subjects, students_by_subject, avail_rooms, avail_faculty, avail_slots
                )
                self._repair(child, subjects, students_by_subject, avail_rooms)
                next_generation.append(child)

            # Evaluate new generation
            evaluated_pop = [
                (
                    ind,
                    self._calculate_fitness(
                        ind, subjects, students_by_subject, rooms_by_id, faculty_by_id, slots_by_id
                    ),
                )
                for ind in next_generation
            ]
            evaluated_pop.sort(key=lambda x: x[1][0], reverse=True)

            best_fit, (best_fitness_val, hard_conflicts, soft_penalty) = evaluated_pop[0][0], evaluated_pop[0][1]
            avg_fitness = sum(x[1][0] for x in evaluated_pop) / len(evaluated_pop)

            history.append({
                "generation": gen,
                "best_fitness": best_fitness_val,
                "avg_fitness": avg_fitness,
                "hard_conflicts": hard_conflicts,
                "soft_penalty": soft_penalty,
            })

            # If global optimum reached (0 hard conflicts and very low penalty), can continue or break early
            if hard_conflicts == 0 and gen >= self.generations // 2 and soft_penalty < 5.0:
                break

        # Best Chromosome Translation to Exam objects
        best_chromosome, (final_fitness, final_conflicts, final_soft_penalty) = evaluated_pop[0]
        final_exams = self._chromosome_to_exams(best_chromosome, subjects, students_by_subject)

        # Full Functional Report
        eval_report = evaluate_schedule_functional(
            final_exams, students_by_subject, rooms_by_id, faculty_by_id, slots_by_id
        )

        return GeneticOptimizationResult(
            best_schedule=final_exams,
            best_fitness=final_fitness,
            initial_fitness=initial_best_fitness,
            hard_conflicts=final_conflicts,
            soft_penalty=final_soft_penalty,
            generations_run=len(history),
            history=history,
            evaluation_report=eval_report,
            is_fully_valid=(final_conflicts == 0),
        )

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _initialize_population(
        self,
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        avail_rooms: List[Room],
        avail_faculty: List[Faculty],
        avail_slots: List[TimeSlot],
    ) -> List[Dict[str, Dict[str, str]]]:
        """Creates initial diverse population, seeding with the heuristic scheduler."""
        if avail_rooms and hasattr(avail_rooms[0], "faculty_id"):
            avail_rooms, avail_faculty = avail_faculty, avail_rooms

        pop: List[Dict[str, Dict[str, str]]] = []

        # Seed #1: Heuristic MRV Schedule (High fitness seed)
        heuristic_scheduler = Scheduler(RoomAllocator())
        heuristic_report = heuristic_scheduler.generate_schedule(
            subjects, students_by_subject, avail_faculty, avail_rooms, avail_slots
        )
        if heuristic_report.scheduled_exams:
            seed_chrom: Dict[str, Dict[str, str]] = {}
            for e in heuristic_report.scheduled_exams:
                seed_chrom[e.subject_id] = {
                    "slot_id": e.slot_id or (avail_slots[0].slot_id if avail_slots else ""),
                    "room_id": e.room_id or (avail_rooms[0].room_id if avail_rooms else ""),
                    "faculty_id": e.faculty_id or (avail_faculty[0].faculty_id if avail_faculty else ""),
                }
            # Fill any missing
            for s in subjects:
                if s.subject_id not in seed_chrom:
                    seed_chrom[s.subject_id] = self._random_gene(s, students_by_subject, avail_rooms, avail_faculty, avail_slots)
            pop.append(seed_chrom)

        # Remaining Individuals: Stochastic Generation
        while len(pop) < self.population_size:
            ind: Dict[str, Dict[str, str]] = {}
            # Shuffle subject order to create variation
            shuffled_subs = list(subjects)
            random.shuffle(shuffled_subs)
            for sub in shuffled_subs:
                ind[sub.subject_id] = self._random_gene(sub, students_by_subject, avail_rooms, avail_faculty, avail_slots)
            pop.append(ind)

        return pop

    def _random_gene(
        self,
        subject: Subject,
        students_by_subject: Dict[str, List[str]],
        avail_rooms: List[Room],
        avail_faculty: List[Faculty],
        avail_slots: List[TimeSlot],
    ) -> Dict[str, str]:
        """Generates a random valid gene for a subject."""
        enrolled_count = len(students_by_subject.get(subject.subject_id, []))
        suitable_rooms = [r for r in avail_rooms if r.capacity >= enrolled_count]
        room = random.choice(suitable_rooms) if suitable_rooms else random.choice(avail_rooms)
        slot = random.choice(avail_slots)
        fac = random.choice(avail_faculty) if avail_faculty else None
        return {
            "slot_id": slot.slot_id,
            "room_id": room.room_id,
            "faculty_id": fac.faculty_id if fac else "",
        }

    def _calculate_fitness(
        self,
        chromosome: Dict[str, Dict[str, str]],
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        rooms_by_id: Dict[str, Room],
        faculty_by_id: Dict[str, Faculty],
        slots_by_id: Dict[str, TimeSlot],
    ) -> Tuple[float, int, float]:
        """
        Evaluates chromosome:
        Returns: (fitness_scalar, hard_violations_count, soft_penalties)
        """
        hard_violations = 0

        # Slot-wise collision detection
        exams_in_slot: Dict[str, List[str]] = {}
        room_usage: Dict[Tuple[str, str], List[str]] = {}
        faculty_usage: Dict[Tuple[str, str], List[str]] = {}

        for sub_id, gene in chromosome.items():
            slot_id = gene["slot_id"]
            room_id = gene["room_id"]
            fac_id = gene["faculty_id"]
            enrolled = students_by_subject.get(sub_id, [])

            # Check capacity
            rm = rooms_by_id.get(room_id)
            if not rm or rm.capacity < len(enrolled):
                hard_violations += 1

            # Check availability
            if rm and not rm.is_available:
                hard_violations += 1
            fac = faculty_by_id.get(fac_id)
            if fac and not fac.is_available:
                hard_violations += 1
            slot = slots_by_id.get(slot_id)
            if slot and not slot.is_available:
                hard_violations += 1

            # Group for clash checks
            exams_in_slot.setdefault(slot_id, []).append(sub_id)
            room_usage.setdefault((slot_id, room_id), []).append(sub_id)
            if fac_id:
                faculty_usage.setdefault((slot_id, fac_id), []).append(sub_id)

        # Check Room Double-Booking
        for (slot, room), subs in room_usage.items():
            if len(subs) > 1:
                hard_violations += (len(subs) - 1) * 2

        # Check Faculty Double-Booking
        for (slot, fac), subs in faculty_usage.items():
            if len(subs) > 1:
                hard_violations += (len(subs) - 1) * 2

        # Check Student Overlap in same slot
        for slot, subs in exams_in_slot.items():
            if len(subs) > 1:
                # Pairwise student overlap
                for i in range(len(subs)):
                    st1 = set(students_by_subject.get(subs[i], []))
                    for j in range(i + 1, len(subs)):
                        st2 = set(students_by_subject.get(subs[j], []))
                        if st1.intersection(st2):
                            hard_violations += 3

        # Convert to Exam objects for functional soft penalty evaluation
        exam_objects = self._chromosome_to_exams(chromosome, subjects, students_by_subject)
        report = evaluate_schedule_functional(
            exam_objects, students_by_subject, rooms_by_id, faculty_by_id, slots_by_id
        )
        soft_penalty = report.total_penalty

        # Total Fitness function
        fitness = 1000.0 / (1.0 + (hard_violations * HARD_VIOLATION_PENALTY) + soft_penalty)

        return fitness, hard_violations, soft_penalty

    def _tournament_select(
        self, evaluated_pop: List[Tuple[Dict[str, Dict[str, str]], Tuple[float, int, float]]]
    ) -> Dict[str, Dict[str, str]]:
        """Tournament selection selects the individual with highest fitness among k competitors."""
        sample_size = min(self.tournament_size, len(evaluated_pop))
        candidates = random.sample(evaluated_pop, sample_size)
        candidates.sort(key=lambda x: x[1][0], reverse=True)
        return candidates[0][0]

    def _crossover(
        self,
        parent1: Dict[str, Dict[str, str]],
        parent2: Dict[str, Dict[str, str]],
        subjects: List[Subject],
    ) -> Dict[str, Dict[str, str]]:
        """Uniform crossover: randomly selects each subject's assignment from parent1 or parent2."""
        child: Dict[str, Dict[str, str]] = {}
        for sub in subjects:
            if random.random() < 0.5:
                child[sub.subject_id] = copy.deepcopy(parent1.get(sub.subject_id, parent2[sub.subject_id]))
            else:
                child[sub.subject_id] = copy.deepcopy(parent2.get(sub.subject_id, parent1[sub.subject_id]))
        return child

    def _mutate(
        self,
        chromosome: Dict[str, Dict[str, str]],
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        avail_rooms: List[Room],
        avail_faculty: List[Faculty],
        avail_slots: List[TimeSlot],
    ) -> Dict[str, Dict[str, str]]:
        """Applies random mutation with probability self.mutation_rate."""
        mutated = copy.deepcopy(chromosome)
        for sub in subjects:
            if random.random() < self.mutation_rate:
                mutation_type = random.choice(["slot", "room", "faculty"])
                if mutation_type == "slot" and avail_slots:
                    mutated[sub.subject_id]["slot_id"] = random.choice(avail_slots).slot_id
                elif mutation_type == "room" and avail_rooms:
                    enrolled = len(students_by_subject.get(sub.subject_id, []))
                    suitable = [r for r in avail_rooms if r.capacity >= enrolled]
                    chosen_room = random.choice(suitable) if suitable else random.choice(avail_rooms)
                    mutated[sub.subject_id]["room_id"] = chosen_room.room_id
                elif mutation_type == "faculty" and avail_faculty:
                    mutated[sub.subject_id]["faculty_id"] = random.choice(avail_faculty).faculty_id
        return mutated

    def _repair(
        self,
        chromosome: Dict[str, Dict[str, str]],
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
        avail_rooms: List[Room],
    ) -> None:
        """Lightweight repair operator to heal capacity shortfalls."""
        rooms_by_id = {r.room_id: r for r in avail_rooms}
        for sub in subjects:
            enrolled = len(students_by_subject.get(sub.subject_id, []))
            gene = chromosome.get(sub.subject_id)
            if not gene:
                continue
            curr_room = rooms_by_id.get(gene["room_id"])
            if not curr_room or curr_room.capacity < enrolled:
                suitable = [r for r in avail_rooms if r.capacity >= enrolled]
                if suitable:
                    # Choose best-fit room
                    suitable.sort(key=lambda r: r.capacity)
                    gene["room_id"] = suitable[0].room_id

    def _chromosome_to_exams(
        self,
        chromosome: Dict[str, Dict[str, str]],
        subjects: List[Subject],
        students_by_subject: Dict[str, List[str]],
    ) -> List[Exam]:
        """Converts an abstract chromosome into concrete Exam domain models."""
        exams = []
        for sub in subjects:
            gene = chromosome.get(sub.subject_id, {})
            enrolled_count = len(students_by_subject.get(sub.subject_id, []))
            exams.append(
                Exam(
                    exam_id=f"EX_{sub.subject_id}",
                    subject_id=sub.subject_id,
                    slot_id=gene.get("slot_id"),
                    room_id=gene.get("room_id"),
                    faculty_id=gene.get("faculty_id"),
                    student_count=enrolled_count,
                    status="Scheduled",
                )
            )
        return exams

