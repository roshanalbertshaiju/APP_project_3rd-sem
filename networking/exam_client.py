"""
ExamOpt — TCP Socket Client API
Milestone 7: Distributed Socket Programming
SRM Institute of Science and Technology, Tiruchirappalli

Provides high-level client interface for interacting with remote ExamOpt server
over TCP network sockets using structured JSON RPC.
"""
import socket
import time
import uuid
from typing import Dict, Any, Optional, Tuple, List

from config import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT, SOCKET_TIMEOUT
from networking.protocol import send_json_message, recv_json_message


class ExamSocketClient:
    """Client for connecting to and invoking remote ExamOpt server services."""

    def __init__(self, host: str = DEFAULT_SERVER_HOST, port: int = DEFAULT_SERVER_PORT, timeout: float = SOCKET_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock: Optional[socket.socket] = None

    def connect(self) -> None:
        """Establishes TCP connection to the server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

    def close(self) -> None:
        """Closes the socket connection."""
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None

    def is_connected(self) -> bool:
        return self.sock is not None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _send_request(self, action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Internal helper to format and transmit request, waiting for response."""
        if not self.sock:
            self.connect()

        req_id = str(uuid.uuid4())[:8]
        req = {
            "action": action,
            "params": params or {},
            "req_id": req_id,
        }
        send_json_message(self.sock, req)
        res = recv_json_message(self.sock, timeout=self.timeout)
        if not res:
            raise ConnectionError("Server closed connection unexpectedly")
        return res

    def ping(self) -> Tuple[bool, float, Dict[str, Any]]:
        """Sends PING request and measures round-trip network latency in milliseconds."""
        t0 = time.perf_counter()
        res = self._send_request("PING")
        latency_ms = (time.perf_counter() - t0) * 1000.0
        success = res.get("status") == "SUCCESS"
        data = res.get("data", {})
        return success, latency_ms, data

    def load_sample_data(self) -> Dict[str, Any]:
        """Instructs server to load the SRM sample dataset."""
        res = self._send_request("LOAD_SAMPLE_DATA")
        return res.get("data", {})

    def generate_schedule(self) -> Dict[str, Any]:
        """Requests server to execute heuristic scheduling."""
        res = self._send_request("GENERATE_SCHEDULE")
        return res.get("data", {})

    def optimize_ga(self, population_size: int = 30, generations: int = 25) -> Dict[str, Any]:
        """Requests server to run Genetic Algorithm optimization."""
        params = {"population_size": population_size, "generations": generations}
        res = self._send_request("OPTIMIZE_GA", params)
        return res.get("data", {})

    def search_parallel(self, candidates: int = 6) -> Dict[str, Any]:
        """Requests server to run multiprocessing parallel candidate search."""
        params = {"candidates": candidates}
        res = self._send_request("SEARCH_PARALLEL", params)
        return res.get("data", {})

    def validate_schedule(self) -> Dict[str, Any]:
        """Requests server to validate the active timetable."""
        res = self._send_request("VALIDATE_SCHEDULE")
        return res.get("data", {})

    def get_timetable(self) -> List[Dict[str, Any]]:
        """Fetches the scheduled exams from the server."""
        res = self._send_request("GET_TIMETABLE")
        return res.get("data", {}).get("exams", [])

    def run_benchmark(self, candidates: int = 6) -> Dict[str, Any]:
        """Requests server to execute multi-core benchmark."""
        params = {"candidates": candidates}
        res = self._send_request("BENCHMARK", params)
        return res.get("data", {}).get("benchmark", {})

    def get_symbolic_model(self) -> Dict[str, Any]:
        """Requests server to return SymPy LaTeX formulas and sensitivity analysis."""
        res = self._send_request("SYMBOLIC_MODEL")
        return res.get("data", {})
