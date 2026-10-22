"""
Unit Tests for Milestone 9: Multiprocessing Engine (ProcessPoolExecutor)
SRM Institute of Science and Technology, Tiruchirappalli
"""
import unittest

from database.database import Database
from utils.sample_data import populate_srm_sample_data
from scheduling.parallel_scheduler import (
    ParallelScheduler,
    _evaluate_candidate_worker,
)


class TestMultiprocessingScheduler(unittest.TestCase):
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

    def test_worker_function_execution(self):
        # Directly test isolated picklable worker function
        res = _evaluate_candidate_worker(
            candidate_id=1,
            subjects_data=[s.to_dict() for s in self.subjects],
            students_by_subject=self.students_map,
            faculty_data=[f.to_dict() for f in self.faculty],
            rooms_data=[r.to_dict() for r in self.rooms],
            slots_data=[s.to_dict() for s in self.slots],
            random_seed=42,
        )
        self.assertEqual(res["candidate_id"], 1)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["hard_conflicts"], 0)
        self.assertEqual(len(res["scheduled_exams"]), len(self.subjects))

    def test_parallel_scheduler_search(self):
        ps = ParallelScheduler(max_workers=2)
        res = ps.search_best_schedule(
            self.subjects, self.students_map, self.faculty, self.rooms, self.slots, num_candidates=4
        )
        self.assertEqual(res.total_candidates_evaluated, 4)
        self.assertEqual(len(res.best_schedule), len(self.subjects))
        self.assertEqual(res.hard_conflicts, 0)
        self.assertGreater(res.best_fitness, 0.0)


if __name__ == "__main__":
    unittest.main()
