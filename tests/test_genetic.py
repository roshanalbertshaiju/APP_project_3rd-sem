"""
Unit Tests for Milestone 11: Genetic Algorithm Meta-Heuristic
SRM Institute of Science and Technology, Tiruchirappalli
"""
import unittest

from database.database import Database
from utils.sample_data import populate_srm_sample_data
from scheduling.genetic_scheduler import GeneticScheduler


class TestGeneticScheduler(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        populate_srm_sample_data(self.db)
        self.subjects = self.db.get_all_subjects()
        self.rooms = self.db.get_all_rooms()
        self.faculty = self.db.get_all_faculty()
        self.slots = self.db.get_all_timeslots()
        self.students_map = {
            s.subject_id: self.db.get_students_for_subject(s.subject_id)
            for s in self.subjects
        }

    def test_population_initialization(self):
        ga = GeneticScheduler(population_size=15, generations=5)
        pop = ga._initialize_population(
            self.subjects, self.students_map, self.rooms, self.faculty, self.slots
        )
        self.assertEqual(len(pop), 15)
        # Check every individual has assignments for all subjects
        for ind in pop:
            for s in self.subjects:
                self.assertIn(s.subject_id, ind)
                self.assertIn("slot_id", ind[s.subject_id])
                self.assertIn("room_id", ind[s.subject_id])

    def test_crossover_integrity(self):
        ga = GeneticScheduler(population_size=10, generations=5)
        pop = ga._initialize_population(
            self.subjects, self.students_map, self.rooms, self.faculty, self.slots
        )
        parent1 = pop[0]
        parent2 = pop[1]
        child = ga._crossover(parent1, parent2, self.subjects)
        # Verify child contains all subjects
        for s in self.subjects:
            self.assertIn(s.subject_id, child)

    def test_mutation_operator(self):
        ga = GeneticScheduler(population_size=10, generations=5, mutation_rate=1.0)
        pop = ga._initialize_population(
            self.subjects, self.students_map, self.rooms, self.faculty, self.slots
        )
        mutated = ga._mutate(
            pop[0], self.subjects, self.students_map, self.rooms, self.faculty, self.slots
        )
        self.assertEqual(len(mutated), len(self.subjects))

    def test_full_ga_optimization(self):
        ga = GeneticScheduler(population_size=20, generations=10, random_seed=123)
        result = ga.optimize(
            self.subjects, self.students_map, self.rooms, self.faculty, self.slots
        )
        self.assertTrue(result.is_fully_valid)
        self.assertEqual(result.hard_conflicts, 0)
        self.assertEqual(len(result.best_schedule), len(self.subjects))
        self.assertGreater(result.best_fitness, 0.0)
        self.assertGreater(len(result.history), 0)


if __name__ == "__main__":
    unittest.main()
