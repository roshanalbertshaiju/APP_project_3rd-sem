"""
Main GUI Application Window for ExamOpt
SRM Institute of Science and Technology, Tiruchirappalli
Project Team: Suhas V A, Subaash G, Roshan Albert Shaiju
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from config import INSTITUTION_NAME, CAMPUS_NAME, SYSTEM_NAME, VERSION, DATABASE_PATH
from services.exam_service import ExamService
from gui.views.timetable_view import TimetableView
from gui.views.student_view import StudentView
from gui.views.subject_view import SubjectView
from gui.views.faculty_view import FacultyView
from gui.views.room_view import RoomView
from gui.views.timeslot_view import TimeSlotView
from gui.views.viva_suite_view import VivaSuiteView
from gui.views.network_dialog import NetworkConnectivityDialog


class ExamOptApp(tk.Tk):
    """Main Application Window for ExamOpt."""

    def __init__(self, service: Optional[ExamService] = None):
        super().__init__()
        self.service = service or ExamService()
        self.active_socket_server = None

        self.title(f"{SYSTEM_NAME} — {INSTITUTION_NAME} (100% Production Final)")
        self.geometry("1100x720")
        self.minsize(900, 600)

        # Style configuration
        self._configure_styles()
        self._build_header()
        self._build_notebook()
        self._build_footer()

        # Initial refresh
        self.refresh_all_views()

        # Clean shutdown handling
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

    def _build_header(self):
        header_frame = tk.Frame(self, bg="#0D47A1")
        header_frame.pack(fill=tk.X, side=tk.TOP)

        # Title and Subtitle on the left
        text_container = tk.Frame(header_frame, bg="#0D47A1")
        text_container.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=8)

        title_lbl = tk.Label(
            text_container,
            text=f"EXAMOPT — INTELLIGENT EXAMINATION SCHEDULING SYSTEM",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#0D47A1",
        )
        title_lbl.pack(anchor=tk.W)

        sub_text = f"{INSTITUTION_NAME}, {CAMPUS_NAME}  |  Team: Suhas V A, Subaash G, Roshan Albert Shaiju  |  100% Production Final"
        sub_lbl = tk.Label(
            text_container,
            text=sub_text,
            font=("Segoe UI", 9),
            fg="#BBDEFB",
            bg="#0D47A1",
        )
        sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        # Action Buttons on the right
        right_container = tk.Frame(header_frame, bg="#0D47A1")
        right_container.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=8)

        # Hamburger Menu Button
        self._build_hamburger_menu(right_container)

        # Network Connectivity Button
        net_btn = tk.Button(
            right_container,
            text="🌐  Network Server",
            font=("Segoe UI", 10, "bold"),
            bg="#1976D2",
            fg="white",
            activebackground="#2196F3",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.open_network_dialog,
        )
        net_btn.pack(side=tk.RIGHT, padx=6)

    def _build_hamburger_menu(self, parent):
        menu_btn = tk.Menubutton(
            parent,
            text="☰  Menu",
            font=("Segoe UI", 11, "bold"),
            bg="#1565C0",
            fg="white",
            activebackground="#1E88E5",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=12,
            pady=6,
            indicatoron=False,
        )
        menu_btn.pack(side=tk.RIGHT)

        # Hover styling
        menu_btn.bind("<Enter>", lambda e: menu_btn.config(bg="#1E88E5"))
        menu_btn.bind("<Leave>", lambda e: menu_btn.config(bg="#1565C0"))

        # Dropdown Menu
        dropdown = tk.Menu(
            menu_btn,
            tearoff=0,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#212121",
            activebackground="#E3F2FD",
            activeforeground="#0D47A1",
        )
        dropdown.add_command(
            label="⚡  Load SRM Sample Dataset",
            command=self.load_sample_dataset,
        )
        dropdown.add_command(
            label="🚀  Quick Generate Timetable",
            command=self._quick_generate,
        )
        dropdown.add_command(
            label="🌐  Server & Network Connectivity",
            command=self.open_network_dialog,
        )
        dropdown.add_command(
            label="🧪  Open Viva Suite & Review Scenarios",
            command=self._open_verification_tab,
        )
        dropdown.add_separator()
        dropdown.add_command(
            label="🔄  Refresh All Views",
            command=self.refresh_all_views,
        )
        dropdown.add_command(
            label="ℹ️  About ExamOpt",
            command=self.show_about,
        )

        menu_btn["menu"] = dropdown

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 7 Streamlined Production Tabs
        self.timetable_view = TimetableView(self.notebook, self.service, on_data_changed=self.refresh_all_views)
        self.student_view = StudentView(self.notebook, self.service, on_data_changed=self.refresh_all_views)
        self.subject_view = SubjectView(self.notebook, self.service, on_data_changed=self.refresh_all_views)
        self.faculty_view = FacultyView(self.notebook, self.service, on_data_changed=self.refresh_all_views)
        self.room_view = RoomView(self.notebook, self.service, on_data_changed=self.refresh_all_views)
        self.timeslot_view = TimeSlotView(self.notebook, self.service, on_data_changed=self.refresh_all_views)
        self.viva_suite_view = VivaSuiteView(self.notebook, self.service, on_data_changed=self.refresh_all_views)

        self.notebook.add(self.timetable_view, text="📅 Master Timetable")
        self.notebook.add(self.student_view, text="🎓 Students")
        self.notebook.add(self.subject_view, text="📚 Subjects")
        self.notebook.add(self.faculty_view, text="👨‍🏫 Faculty")
        self.notebook.add(self.room_view, text="🏢 Rooms")
        self.notebook.add(self.timeslot_view, text="⏰ Time Slots")
        self.notebook.add(self.viva_suite_view, text="🧪 Academic Review & Viva Suite")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _build_footer(self):
        footer_frame = ttk.Frame(self)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=4)

        db_label = f"Database: SQLite ({DATABASE_PATH})  |  Status: 100% Production Capstone Complete (Milestones 1–12)"
        ttk.Label(footer_frame, text=db_label, font=("Segoe UI", 8), foreground="#555555").pack(side=tk.LEFT)

        self.server_status_var = tk.StringVar(value="Server: Offline (Local Mode)")
        ttk.Label(footer_frame, textvariable=self.server_status_var, font=("Segoe UI", 8, "bold"), foreground="#1565C0").pack(side=tk.LEFT, padx=15)

        ttk.Label(footer_frame, text=f"ExamOpt v{VERSION}", font=("Segoe UI", 8), foreground="#555555").pack(side=tk.RIGHT)

    def _on_tab_changed(self, event):
        # Refresh current tab
        current_tab = self.notebook.select()
        tab_widget = self.nametowidget(current_tab)
        if hasattr(tab_widget, "refresh"):
            tab_widget.refresh()

    def refresh_all_views(self):
        self.timetable_view.refresh()
        self.student_view.refresh()
        self.subject_view.refresh()
        self.faculty_view.refresh()
        self.room_view.refresh()
        self.timeslot_view.refresh()
        if hasattr(self, "viva_suite_view"):
            self.viva_suite_view.refresh()

    def open_network_dialog(self):
        """Opens the Distributed TCP Socket Server & Connectivity dialog."""
        NetworkConnectivityDialog(self, self.service, on_status_changed=self._on_server_status_changed)

    def _on_server_status_changed(self, running: bool, endpoint: Optional[str]):
        """Callback from NetworkConnectivityDialog when server state changes."""
        if running:
            self.server_status_var.set(f"Server: Online ({endpoint})")
        else:
            self.server_status_var.set("Server: Offline (Local Mode)")

    def _on_close(self):
        """Safely clean up background socket server if running upon window exit."""
        if getattr(self, "active_socket_server", None):
            try:
                self.active_socket_server.stop()
            except Exception:
                pass
        self.destroy()

    def load_sample_dataset(self):
        if messagebox.askyesno(
            "Load Sample Data",
            "This will populate the database with realistic SRM IST Tiruchirappalli examination data (Subjects, Students, Faculty, Rooms, Time Slots).\n\nProceed?"
        ):
            stats = self.service.load_srm_sample_data()
            self.refresh_all_views()
            messagebox.showinfo(
                "Data Loaded",
                f"Sample Data Loaded Successfully!\n\n"
                f"• Subjects: {stats['subjects']}\n"
                f"• Students: {stats['students']}\n"
                f"• Faculty: {stats['faculty']}\n"
                f"• Rooms: {stats['rooms']}\n"
                f"• Time Slots: {stats['timeslots']}\n\n"
                f"You can now click '🚀 Generate Timetable'!"
            )

    def _quick_generate(self):
        self.notebook.select(self.timetable_view)
        self.timetable_view.generate_timetable()

    def _open_verification_tab(self):
        self.notebook.select(self.viva_suite_view)

    def show_about(self):
        about_text = (
            f"{SYSTEM_NAME}\n"
            f"{INSTITUTION_NAME}, {CAMPUS_NAME}\n\n"
            f"Project Team:\n"
            f"• Suhas V A\n"
            f"• Subaash G\n"
            f"• Roshan Albert Shaiju\n\n"
            f"Technology Stack:\n"
            f"• Python 3\n"
            f"• SQLite 3\n"
            f"• Tkinter GUI\n\n"
            f"Current Milestone: 100% Production Implementation Complete (Milestones 1–12)\n"
            f"Features: Distributed TCP Sockets, Multiprocessing (GIL Bypassed), Genetic Algorithm, SymPy Modeling, Excel & PDF Exports."
        )
        messagebox.showinfo("About ExamOpt", about_text)



def start_gui():
    app = ExamOptApp()
    app.mainloop()
