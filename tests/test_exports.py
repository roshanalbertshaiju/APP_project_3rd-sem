"""
Unit Tests for Milestone 12: Export Manager (Excel, PDF, CSV)
SRM Institute of Science and Technology, Tiruchirappalli
"""
import unittest
import os
import tempfile
import csv

from database.database import Database
from utils.sample_data import populate_srm_sample_data
from services.exam_service import ExamService
from utils.export_manager import ExportManager


class TestExportManager(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.service = ExamService(self.db)
        self.service.load_srm_sample_data()
        self.report = self.service.generate_timetable()

        self.rooms = {r.room_id: r for r in self.service.get_rooms()}
        self.faculty = {f.faculty_id: f for f in self.service.get_faculty()}
        self.slots = {s.slot_id: s for s in self.service.get_timeslots()}

        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_csv_export(self):
        csv_path = os.path.join(self.temp_dir.name, "schedule.csv")
        out = ExportManager.export_csv(
            self.report.scheduled_exams, self.rooms, self.faculty, self.slots, csv_path
        )
        self.assertTrue(os.path.exists(out))
        self.assertGreater(os.path.getsize(out), 0)

        with open(out, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            # Header + 6 scheduled exams
            self.assertEqual(len(rows), len(self.report.scheduled_exams) + 1)

    def test_excel_export(self):
        xlsx_path = os.path.join(self.temp_dir.name, "schedule.xlsx")
        out = ExportManager.export_excel(
            self.report.scheduled_exams, self.rooms, self.faculty, self.slots, xlsx_path
        )
        self.assertTrue(os.path.exists(out))
        self.assertGreater(os.path.getsize(out), 1000)

    def test_pdf_export(self):
        pdf_path = os.path.join(self.temp_dir.name, "schedule.pdf")
        out = ExportManager.export_pdf(
            self.report.scheduled_exams, self.rooms, self.faculty, self.slots, pdf_path
        )
        self.assertTrue(os.path.exists(out))
        self.assertGreater(os.path.getsize(out), 1000)


if __name__ == "__main__":
    unittest.main()
