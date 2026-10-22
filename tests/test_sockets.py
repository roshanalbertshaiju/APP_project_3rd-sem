"""
Unit Tests for Milestone 7: TCP Socket Client-Server Architecture
SRM Institute of Science and Technology, Tiruchirappalli
"""
import unittest
import time
import socket

from database.database import Database
from services.exam_service import ExamService
from networking.exam_server import ExamSocketServer
from networking.exam_client import ExamSocketClient
from networking.protocol import send_json_message, recv_json_message


class TestSocketNetworking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_port = 9182
        cls.db = Database(":memory:")
        cls.service = ExamService(cls.db)
        cls.service.load_srm_sample_data()

        cls.server = ExamSocketServer("127.0.0.1", cls.test_port, cls.service)
        cls.server.start_in_background()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_ping_pong(self):
        with ExamSocketClient("127.0.0.1", self.test_port) as client:
            ok, latency_ms, data = client.ping()
            self.assertTrue(ok)
            self.assertGreater(latency_ms, 0.0)
            self.assertEqual(data.get("status"), "ONLINE")

    def test_remote_schedule_generation(self):
        with ExamSocketClient("127.0.0.1", self.test_port) as client:
            res = client.generate_schedule()
            self.assertTrue(res.get("success"))
            self.assertGreater(res.get("scheduled_count"), 0)
            self.assertIn("scheduled_exams", res)

    def test_remote_validation(self):
        with ExamSocketClient("127.0.0.1", self.test_port) as client:
            res = client.validate_schedule()
            self.assertTrue(res.get("success"))
            self.assertIn("is_valid", res)

    def test_remote_symbolic_model(self):
        with ExamSocketClient("127.0.0.1", self.test_port) as client:
            res = client.get_symbolic_model()
            self.assertTrue(res.get("success"))
            self.assertIn("latex", res)
            self.assertIn("objective_latex", res["latex"])


if __name__ == "__main__":
    unittest.main()
