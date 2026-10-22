"""
ExamOpt — Distributed Socket Network Studio View (Modern GUI)
Milestone 7: Socket Client-Server Architecture
SRM Institute of Science and Technology, Tiruchirappalli
"""
import tkinter as tk
from tkinter import messagebox
import json
import threading
from typing import Optional

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
COLOR_ACCENT_HOVER = "#4F46E5"
COLOR_SUCCESS = "#10B981"
COLOR_CARD = "#111827"


class NetworkStudioView(tk.Frame):
    """Interactive GUI for hosting, monitoring, and communicating with ExamOpt Socket Servers."""

    def __init__(self, parent, service: ExamService, on_data_changed=None):
        super().__init__(parent, bg=COLOR_BG)
        self.service = service
        self.on_data_changed = on_data_changed
        self.server: Optional[ExamSocketServer] = None

        self._build_ui()

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self, bg=COLOR_SURFACE, padx=16, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        header.pack(fill=tk.X, padx=12, pady=(8, 12))

        tk.Label(
            header,
            text="🌐  Distributed TCP Socket Client-Server Studio",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        ).pack(anchor=tk.W)

        tk.Label(
            header,
            text="True network-decoupled architecture using binary framed TCP sockets and JSON RPC messaging.",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        ).pack(anchor=tk.W, pady=(2, 0))

        # Main Layout: Left Controls + Right Packet Log
        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        left_pane = tk.Frame(body, bg=COLOR_BG, width=380)
        left_pane.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left_pane.pack_propagate(False)

        right_pane = tk.Frame(body, bg=COLOR_SURFACE, highlightthickness=1, highlightbackground=COLOR_BORDER)
        right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- SERVER MANAGEMENT CARD ---
        server_card = tk.Frame(left_pane, bg=COLOR_SURFACE, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        server_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(server_card, text="TCP SERVER CONTROL", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(0, 6))

        # Host & Port fields
        hp_frame = tk.Frame(server_card, bg=COLOR_SURFACE)
        hp_frame.pack(fill=tk.X, pady=2)

        tk.Label(hp_frame, text="Host:", font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(side=tk.LEFT)
        self.host_entry = tk.Entry(hp_frame, width=12, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        self.host_entry.insert(0, DEFAULT_SERVER_HOST)
        self.host_entry.pack(side=tk.LEFT, padx=(4, 10))

        tk.Label(hp_frame, text="Port:", font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(side=tk.LEFT)
        self.port_entry = tk.Entry(hp_frame, width=6, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        self.port_entry.insert(0, str(DEFAULT_SERVER_PORT))
        self.port_entry.pack(side=tk.LEFT, padx=4)

        # Status & Toggle Button
        status_bar = tk.Frame(server_card, bg=COLOR_SURFACE)
        status_bar.pack(fill=tk.X, pady=(8, 4))

        self.server_status_dot = tk.Label(status_bar, text="●", font=("Segoe UI", 10), fg="#EF4444", bg=COLOR_SURFACE)
        self.server_status_dot.pack(side=tk.LEFT, padx=(0, 4))
        self.server_status_text = tk.Label(status_bar, text="Server Stopped", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE)
        self.server_status_text.pack(side=tk.LEFT)

        self.toggle_server_btn = tk.Button(
            server_card,
            text="▶  Start Background Daemon",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_SUCCESS,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            pady=5,
            command=self._toggle_server,
        )
        self.toggle_server_btn.pack(fill=tk.X, pady=(6, 0))

        # --- CLIENT DISPATCH CARD ---
        client_card = tk.Frame(left_pane, bg=COLOR_SURFACE, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        client_card.pack(fill=tk.X)

        tk.Label(client_card, text="CLIENT RPC COMMANDS", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(0, 6))

        # Ping Button
        ping_btn = tk.Button(
            client_card,
            text="⚡  Ping Server & Measure Latency",
            font=("Segoe UI", 8),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor=tk.W,
            padx=10,
            pady=5,
            command=self._client_ping,
        )
        ping_btn.pack(fill=tk.X, pady=3)

        # Generate Button
        sched_btn = tk.Button(
            client_card,
            text="🚀  Dispatch Remote Timetable Request",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_ACCENT,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor=tk.W,
            padx=10,
            pady=5,
            command=self._client_remote_schedule,
        )
        sched_btn.pack(fill=tk.X, pady=3)

        # Remote Validate Button
        val_btn = tk.Button(
            client_card,
            text="🔍  Dispatch Remote Constraint Validation",
            font=("Segoe UI", 8),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor=tk.W,
            padx=10,
            pady=5,
            command=self._client_remote_validate,
        )
        val_btn.pack(fill=tk.X, pady=3)

        # SymPy Model Button
        sym_btn = tk.Button(
            client_card,
            text="📐  Query SymPy Mathematical Model",
            font=("Segoe UI", 8),
            bg=COLOR_CARD,
            fg=COLOR_TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor=tk.W,
            padx=10,
            pady=5,
            command=self._client_remote_symbolic,
        )
        sym_btn.pack(fill=tk.X, pady=3)

        # --- RIGHT: JSON PACKET INSPECTOR ---
        tk.Label(right_pane, text="JSON RPC PACKET WIRE INSPECTOR", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE, padx=12, pady=8).pack(anchor=tk.W)

        self.console = tk.Text(
            right_pane,
            bg=COLOR_CARD,
            fg="#A7F3D0",
            insertbackground="white",
            font=("Consolas", 9),
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self._log_console("ExamOpt Distributed Socket Studio Ready.\nStart the daemon or ping an existing server on the left.")

    def _log_console(self, text: str):
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)

    def _toggle_server(self):
        if self.server is None:
            try:
                host = self.host_entry.get().strip()
                port = int(self.port_entry.get().strip())
                self.server = ExamSocketServer(host, port, self.service)
                self.server.start_in_background()

                self.server_status_dot.config(fg=COLOR_SUCCESS)
                self.server_status_text.config(text=f"Online ({host}:{port})", fg=COLOR_SUCCESS)
                self.toggle_server_btn.config(text="⏹  Stop Daemon", bg="#EF4444")
                self._log_console(f"[SERVER STARTED] Listening on TCP {host}:{port}")
            except Exception as e:
                messagebox.showerror("Server Error", f"Failed to start socket server: {e}")
        else:
            try:
                self.server.stop()
                self.server = None
                self.server_status_dot.config(fg="#EF4444")
                self.server_status_text.config(text="Server Stopped", fg=COLOR_TEXT_MUTED)
                self.toggle_server_btn.config(text="▶  Start Background Daemon", bg=COLOR_SUCCESS)
                self._log_console("[SERVER STOPPED] Port released.")
            except Exception as e:
                messagebox.showerror("Server Error", f"Failed to stop socket server: {e}")

    def _get_client(self) -> ExamSocketClient:
        host = self.host_entry.get().strip()
        port = int(self.port_entry.get().strip())
        return ExamSocketClient(host, port, timeout=5.0)

    def _client_ping(self):
        try:
            with self._get_client() as client:
                ok, latency, data = client.ping()
                self._log_console(f"--> PING Sent to {client.host}:{client.port}")
                self._log_console(f"<-- PONG Received in {latency:.2f}ms | Status: {data.get('status')}")
                self._log_console(json.dumps(data, indent=2))
        except Exception as e:
            self._log_console(f"[PING FAILED] {e}")

    def _client_remote_schedule(self):
        try:
            with self._get_client() as client:
                self._log_console(f"--> SEND: ACTION=GENERATE_SCHEDULE")
                res = client.generate_schedule()
                self._log_console(f"<-- RECV: Success={res.get('success')}, Scheduled={res.get('scheduled_count')}")
                self._log_console(json.dumps(res, indent=2))
                if self.on_data_changed:
                    self.on_data_changed()
        except Exception as e:
            self._log_console(f"[REQUEST FAILED] {e}")

    def _client_remote_validate(self):
        try:
            with self._get_client() as client:
                self._log_console(f"--> SEND: ACTION=VALIDATE_SCHEDULE")
                res = client.validate_schedule()
                self._log_console(f"<-- RECV: IsValid={res.get('is_valid')}")
                self._log_console(json.dumps(res, indent=2))
        except Exception as e:
            self._log_console(f"[VALIDATION FAILED] {e}")

    def _client_remote_symbolic(self):
        try:
            with self._get_client() as client:
                self._log_console(f"--> SEND: ACTION=SYMBOLIC_MODEL")
                res = client.get_symbolic_model()
                self._log_console("<-- RECV: SymPy Sensitivity and LaTeX expressions:")
                self._log_console(json.dumps(res, indent=2))
        except Exception as e:
            self._log_console(f"[SYMBOLIC FAILED] {e}")
