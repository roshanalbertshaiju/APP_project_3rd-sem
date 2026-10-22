"""
ExamOpt — Multi-Threaded TCP Socket Server
Milestone 7: Distributed Socket Programming
SRM Institute of Science and Technology, Tiruchirappalli

Decouples the examination optimization engine into a standalone TCP server daemon.
Handles concurrent client sessions using ThreadingTCPServer and framed JSON messages.
"""
import sys
import time
import socketserver
import threading
import logging
from typing import Dict, Any, Optional

from config import (
    DEFAULT_SERVER_HOST,
    DEFAULT_SERVER_PORT,
    SYSTEM_NAME,
    VERSION,
    INSTITUTION_NAME,
)
from services.exam_service import ExamService
from networking.protocol import send_json_message, recv_json_message
from scheduling.genetic_scheduler import GeneticScheduler
from scheduling.parallel_scheduler import ParallelScheduler
from optimization.symbolic_model import SymbolicTimetableModel

logger = logging.getLogger("ExamSocketServer")


class ExamRequestHandler(socketserver.BaseRequestHandler):
    """Handles an individual client connection over a dedicated thread."""

    def handle(self):
        client_address = self.client_address
        logger.info(f"Accepted client connection from {client_address}")
        service: ExamService = self.server.service

        try:
            while True:
                req = recv_json_message(self.request)
                if req is None:
                    break

                action = req.get("action", "").upper()
                params = req.get("params", {})
                req_id = req.get("req_id", "0")
                logger.debug(f"Received request [{req_id}] Action: {action}")

                response_data = self._dispatch_action(service, action, params)

                res = {
                    "status": "SUCCESS" if response_data.get("success", True) else "ERROR",
                    "action": action,
                    "req_id": req_id,
                    "data": response_data,
                    "timestamp": time.time(),
                }
                send_json_message(self.request, res)

        except (ConnectionResetError, BrokenPipeError):
            logger.info(f"Client disconnected: {client_address}")
        except Exception as e:
            logger.exception(f"Unhandled error handling request from {client_address}: {e}")
            try:
                send_json_message(self.request, {"status": "ERROR", "error": str(e)})
            except Exception:
                pass


    def _dispatch_action(self, service: ExamService, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Routes actions to service methods."""
        if action in ("PING", "HEALTH"):
            return {
                "success": True,
                "system": SYSTEM_NAME,
                "institution": INSTITUTION_NAME,
                "version": VERSION,
                "server_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "ONLINE",
            }

        elif action == "LOAD_SAMPLE_DATA":
            stats = service.load_srm_sample_data()
            return {"success": True, "stats": stats, "message": "SRM sample dataset loaded into server DB."}

        elif action == "GENERATE_SCHEDULE":
            report = service.generate_timetable()
            return {
                "success": report.is_complete,
                "scheduled_count": report.scheduled_count,
                "unscheduled_count": len(report.unscheduled_exams),
                "scheduled_exams": [e.to_dict() for e in report.scheduled_exams],
                "summary": report.summary_message,
            }

        elif action == "OPTIMIZE_GA":
            pop_size = params.get("population_size", 25)
            generations = params.get("generations", 20)
            ga = GeneticScheduler(population_size=pop_size, generations=generations)
            
            subjects = service.get_subjects()
            rooms = service.get_rooms()
            faculty = service.get_faculty()
            slots = service.get_timeslots()
            students_map = {s.subject_id: service.db.get_students_for_subject(s.subject_id) for s in subjects}

            ga_result = ga.optimize(subjects, students_map, faculty, rooms, slots)
            return {
                "success": ga_result.is_fully_valid,
                "ga_result": ga_result.to_dict(),
            }

        elif action == "SEARCH_PARALLEL":
            num_candidates = params.get("candidates", 6)
            ps = ParallelScheduler()
            subjects = service.get_subjects()
            rooms = service.get_rooms()
            faculty = service.get_faculty()
            slots = service.get_timeslots()
            students_map = {s.subject_id: service.db.get_students_for_subject(s.subject_id) for s in subjects}

            res = ps.search_best_schedule(subjects, students_map, faculty, rooms, slots, num_candidates=num_candidates)
            return {"success": True, "parallel_result": res.to_dict()}

        elif action == "VALIDATE_SCHEDULE":
            is_valid, results = service.validate_current_schedule()
            return {
                "success": True,
                "is_valid": is_valid,
                "results": [r.to_dict() for r in results],
            }

        elif action == "GET_TIMETABLE":
            exams = service.get_scheduled_timetable()
            return {
                "success": True,
                "count": len(exams),
                "exams": [e.to_dict() for e in exams],
            }

        elif action == "BENCHMARK":
            ps = ParallelScheduler()
            subjects = service.get_subjects()
            rooms = service.get_rooms()
            faculty = service.get_faculty()
            slots = service.get_timeslots()
            students_map = {s.subject_id: service.db.get_students_for_subject(s.subject_id) for s in subjects}
            candidates = params.get("candidates", 6)
            bm = ps.benchmark_speedup(subjects, students_map, faculty, rooms, slots, num_candidates=candidates)
            return {"success": True, "benchmark": bm}

        elif action == "SYMBOLIC_MODEL":
            model = SymbolicTimetableModel()
            latex = model.get_latex_formulation()
            base_penalties = params.get("penalties", {"consecutive": 4, "faculty": 1, "waste": 35})
            sens = model.perform_sensitivity_analysis(base_penalties)
            return {
                "success": True,
                "latex": latex,
                "sensitivity": sens,
            }

        else:
            return {"success": False, "error": f"Unknown action: {action}"}


class ExamSocketServer(socketserver.ThreadingTCPServer):
    """Threaded TCP server hosting ExamOpt remote services."""
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, host: str = DEFAULT_SERVER_HOST, port: int = DEFAULT_SERVER_PORT, service: Optional[ExamService] = None):
        self.service = service or ExamService()
        self.host = host
        self.port = port
        self._thread: Optional[threading.Thread] = None
        super().__init__((host, port), ExamRequestHandler)

    def start_in_background(self) -> None:
        """Starts server in a background daemon thread."""
        self._thread = threading.Thread(target=self.serve_forever, daemon=True)
        self._thread.start()
        logger.info(f"ExamOpt TCP Socket Server running in background at {self.host}:{self.port}")

    def stop(self) -> None:
        """Shuts down server gracefully."""
        self.shutdown()
        self.server_close()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.info("ExamOpt TCP Socket Server stopped.")


def run_standalone_server(host: str = DEFAULT_SERVER_HOST, port: int = DEFAULT_SERVER_PORT):
    """Runs the socket server in the foreground (blocking)."""
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s [%(name)s]: %(message)s")
    print("=" * 70)
    print(f"EXAMOPT DISTRIBUTED TCP SOCKET SERVER — {VERSION}")
    print(f"Listening on: {host}:{port}")
    print("Press CTRL+C to terminate.")
    print("=" * 70)

    server = ExamSocketServer(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nTerminating server...")
        server.stop()
        print("Server shutdown successfully.")


if __name__ == "__main__":
    h = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SERVER_HOST
    p = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_SERVER_PORT
    run_standalone_server(h, p)
