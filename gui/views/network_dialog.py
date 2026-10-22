"""
ExamOpt — Server & Network Connectivity Dialog
SRM Institute of Science and Technology, Tiruchirappalli

Provides a clean pop-up window for managing the TCP Socket Server daemon,
testing network ping latency, and inspecting remote JSON RPC payloads.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
from typing import Optional, Callable

from services.exam_service import ExamService
from networking.exam_server import ExamSocketServer
from networking.exam_client import ExamSocketClient
from config import DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT

COLOR_BG = "#0B0F19"
COLOR_SURFACE = "#0F172A"
COLOR_BORDER = "#1E293B"
COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ACCENT = "#6366F1"
COLOR_SUCCESS = "#10B981"
COLOR_CARD = "#111827"


class NetworkConnectivityDialog(tk.Toplevel):
    """Clean popup window for TCP Socket Server & Client Management."""

    def __init__(self, parent, service: ExamService, on_status_changed: Optional[Callable] = None):
        super().__init__(parent)
        self.service = service
        self.on_status_changed = on_status_changed
        self.title("Server & Network Connectivity — ExamOpt")
        self.geometry("640x520")
        self.minsize(560, 440)
        self.configure(bg=COLOR_BG)

        # Reference to existing server if already running
        self.server: Optional[ExamSocketServer] = getattr(parent, "active_socket_server", None)

        self._build_ui()
        self.transient(parent)
        self.grab_set()

    def _build_ui(self):
        # Header Banner
        header = tk.Frame(self, bg=COLOR_SURFACE, padx=16, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        header.pack(fill=tk.X, padx=12, pady=(12, 8))

        tk.Label(
            header,
            text="🌐  Distributed TCP Socket Server & Connectivity",
            font=("Segoe UI", 11, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        ).pack(anchor=tk.W)

        tk.Label(
            header,
            text="Enables decentralized university operations via 4-byte length-prefixed JSON RPC framing.",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        ).pack(anchor=tk.W, pady=(2, 0))

        # Config & Actions Frame
        ctrl_frame = tk.Frame(self, bg=COLOR_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        ctrl_frame.pack(fill=tk.X, padx=12, pady=(0, 8))

        # Host/Port Controls
        hp_row = tk.Frame(ctrl_frame, bg=COLOR_SURFACE)
        hp_row.pack(fill=tk.X, pady=2)

        tk.Label(hp_row, text="Server Host:", font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(side=tk.LEFT)
        self.host_entry = tk.Entry(hp_row, width=14, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        self.host_entry.insert(0, DEFAULT_SERVER_HOST)
        self.host_entry.pack(side=tk.LEFT, padx=(4, 12))

        tk.Label(hp_row, text="Port:", font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(side=tk.LEFT)
        self.port_entry = tk.Entry(hp_row, width=8, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        self.port_entry.insert(0, str(DEFAULT_SERVER_PORT))
        self.port_entry.pack(side=tk.LEFT, padx=4)

        # Server Toggle & Status
        status_row = tk.Frame(ctrl_frame, bg=COLOR_SURFACE)
        status_row.pack(fill=tk.X, pady=(8, 4))

        self.status_dot = tk.Label(status_row, text="●", font=("Segoe UI", 10), fg="#EF4444", bg=COLOR_SURFACE)
        self.status_dot.pack(side=tk.LEFT, padx=(0, 4))

        self.status_text = tk.Label(status_row, text="Daemon Offline", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE)
        self.status_text.pack(side=tk.LEFT)

        self.toggle_btn = tk.Button(
            status_row,
            text="Start Background Server",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_SUCCESS,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=3,
            command=self._toggle_server,
        )
        self.toggle_btn.pack(side=tk.RIGHT)

        # Action Buttons
        btn_bar = tk.Frame(ctrl_frame, bg=COLOR_SURFACE)
        btn_bar.pack(fill=tk.X, pady=(6, 2))

        ping_btn = tk.Button(
            btn_bar,
            text="⚡  Test Ping Latency",
            font=("Segoe UI", 8),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=8,
            pady=4,
            command=self._ping_server,
        )
        ping_btn.pack(side=tk.LEFT, padx=(0, 6))

        req_btn = tk.Button(
            btn_bar,
            text="🚀  Dispatch Remote Timetable RPC",
            font=("Segoe UI", 8),
            bg=COLOR_ACCENT,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=8,
            pady=4,
            command=self._remote_schedule,
        )
        req_btn.pack(side=tk.LEFT)

        # Wire Packet Inspector Console
        tk.Label(self, text="JSON RPC PACKET WIRE INSPECTOR", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_BG, padx=14).pack(anchor=tk.W, pady=(4, 2))

        self.console = tk.Text(
            self,
            bg=COLOR_CARD,
            fg="#A7F3D0",
            insertbackground="white",
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self._log("ExamOpt Socket Inspector Ready.\nClick 'Start Background Server' or 'Test Ping Latency'.")

        self._update_server_status_ui()

    def _log(self, text: str):
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)

    def _update_server_status_ui(self):
        if self.server:
            self.status_dot.config(fg=COLOR_SUCCESS)
            self.status_text.config(text=f"Daemon Online ({self.server.host}:{self.server.port})", fg=COLOR_SUCCESS)
            self.toggle_btn.config(text="Stop Daemon", bg="#EF4444")
        else:
            self.status_dot.config(fg="#EF4444")
            self.status_text.config(text="Daemon Offline (Local Standalone Mode)", fg=COLOR_TEXT_MUTED)
            self.toggle_btn.config(text="Start Background Server", bg=COLOR_SUCCESS)

    def _toggle_server(self):
        if self.server is None:
            try:
                host = self.host_entry.get().strip()
                port = int(self.port_entry.get().strip())
                self.server = ExamSocketServer(host, port, self.service)
                self.server.start_in_background()
                # Store reference on parent window
                self.master.active_socket_server = self.server
                self._update_server_status_ui()
                self._log(f"[DAEMON STARTED] Listening on TCP {host}:{port}")
                if self.on_status_changed:
                    self.on_status_changed(True, f"{host}:{port}")
            except Exception as e:
                messagebox.showerror("Server Error", f"Could not start socket server: {e}")
        else:
            try:
                self.server.stop()
                self.server = None
                self.master.active_socket_server = None
                self._update_server_status_ui()
                self._log("[DAEMON STOPPED] Port released.")
                if self.on_status_changed:
                    self.on_status_changed(False, None)
            except Exception as e:
                messagebox.showerror("Server Error", f"Could not stop server: {e}")

    def _get_client(self) -> ExamSocketClient:
        host = self.host_entry.get().strip()
        port = int(self.port_entry.get().strip())
        return ExamSocketClient(host, port, timeout=5.0)

    def _ping_server(self):
        try:
            with self._get_client() as client:
                ok, latency_ms, data = client.ping()
                self._log(f"--> PING sent to {client.host}:{client.port}")
                self._log(f"<-- PONG received in {latency_ms:.2f}ms | Server Status: {data.get('status')}")
                self._log(json.dumps(data, indent=2))
        except Exception as e:
            self._log(f"[PING FAILED] {e} (Ensure server daemon is running)")

    def _remote_schedule(self):
        try:
            with self._get_client() as client:
                self._log("--> SEND: ACTION=GENERATE_SCHEDULE")
                res = client.generate_schedule()
                self._log(f"<-- RECV: Success={res.get('success')} | Scheduled={res.get('scheduled_count')} exams")
                self._log(json.dumps(res, indent=2))
        except Exception as e:
            self._log(f"[REQUEST FAILED] {e}")
