"""
Modern Minimalist GUI Application Window for ExamOpt
SRM Institute of Science and Technology, Tiruchirappalli
Project Team: Suhas V A, Subaash G, Roshan Albert Shaiju

A sleek, modern dark slate interface featuring:
- Obsidian & slate color palette with electric indigo accents
- Clean left sidebar navigation with active indicator strips
- Live status metrics and instant one-click actions
- High-contrast, spacious typography and modern TTK styling
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict

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



# Modern Minimalist Palette (Obsidian & Electric Indigo)
COLOR_BG = "#0B0F19"             # Deep obsidian main background
COLOR_SURFACE = "#0F172A"        # Dark slate surface
COLOR_SIDEBAR = "#080C14"        # Sidebar background
COLOR_SIDEBAR_ACTIVE = "#1E293B" # Active navigation item background
COLOR_BORDER = "#1E293B"         # Subtle hairline border
COLOR_TEXT_PRIMARY = "#F8FAFC"   # Crisp white primary text
COLOR_TEXT_MUTED = "#94A3B8"     # Muted slate gray text
COLOR_TEXT_DIM = "#64748B"       # Dim category text
COLOR_ACCENT = "#6366F1"         # Electric indigo brand accent
COLOR_ACCENT_HOVER = "#4F46E5"   # Darker indigo hover
COLOR_ACCENT_CYAN = "#38BDF8"    # Sky cyan highlight
COLOR_SUCCESS = "#10B981"        # Emerald green success
COLOR_CARD = "#111827"           # Card container background
COLOR_HOVER = "#1E293B"          # General hover state


class ExamOptModernApp(tk.Tk):
    """Modern Minimalist Application Window for ExamOpt."""

    def __init__(self, service: Optional[ExamService] = None):
        super().__init__()
        self.service = service or ExamService()
        self.active_socket_server = None

        self.title(f"{SYSTEM_NAME} — Modern Studio ({INSTITUTION_NAME})")
        self.geometry("1180x750")
        self.minsize(980, 620)
        self.configure(bg=COLOR_BG)

        # Navigation state
        self.current_tab_id = "timetable"
        self.nav_buttons: Dict[str, dict] = {}

        # Style TTK for dark minimalism
        self._configure_modern_styles()

        # Build UI layout
        self._build_layout()

        # Switch to default view
        self._switch_tab("timetable")

        # Initial refresh
        self.refresh_all_views()

        # Clean shutdown handling
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_modern_styles(self):
        """Configures ttk style engine with a dark slate minimalist theme."""
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Global overrides
        style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT_PRIMARY, font=("Segoe UI", 9))

        # Frames & Containers
        style.configure("TFrame", background=COLOR_BG)
        style.configure("Surface.TFrame", background=COLOR_SURFACE)
        style.configure("Card.TFrame", background=COLOR_CARD, relief="flat")
        style.configure("Sidebar.TFrame", background=COLOR_SIDEBAR)

        # Label Frames
        style.configure(
            "TLabelframe",
            background=COLOR_SURFACE,
            bordercolor=COLOR_BORDER,
            darkcolor=COLOR_BORDER,
            lightcolor=COLOR_BORDER,
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            "TLabelframe.Label",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT_MUTED,
            font=("Segoe UI", 9, "bold"),
        )

        # Labels
        style.configure("TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_PRIMARY, font=("Segoe UI", 9))
        style.configure("Muted.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 8))

        # Standard Buttons
        style.configure(
            "TButton",
            background=COLOR_SIDEBAR_ACTIVE,
            foreground=COLOR_TEXT_PRIMARY,
            bordercolor=COLOR_BORDER,
            lightcolor=COLOR_SIDEBAR_ACTIVE,
            darkcolor=COLOR_SIDEBAR_ACTIVE,
            borderwidth=1,
            relief="flat",
            font=("Segoe UI", 9),
            padding=(10, 5),
        )
        style.map(
            "TButton",
            background=[("active", "#334155"), ("pressed", COLOR_ACCENT)],
            foreground=[("active", "#FFFFFF"), ("pressed", "#FFFFFF")],
        )

        # Accent Primary Button
        style.configure(
            "Accent.TButton",
            background=COLOR_ACCENT,
            foreground="#FFFFFF",
            bordercolor=COLOR_ACCENT,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=(12, 6),
        )
        style.map(
            "Accent.TButton",
            background=[("active", COLOR_ACCENT_HOVER), ("pressed", "#4338CA")],
            foreground=[("active", "#FFFFFF")],
        )

        # Treeview (Data Tables)
        style.configure(
            "Treeview",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT_PRIMARY,
            fieldbackground=COLOR_SURFACE,
            borderwidth=0,
            font=("Segoe UI", 9),
            rowheight=28,
        )
        style.map(
            "Treeview",
            background=[("selected", COLOR_ACCENT)],
            foreground=[("selected", "#FFFFFF")],
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_SIDEBAR_ACTIVE,
            foreground=COLOR_TEXT_MUTED,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
            padding=(6, 4),
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#334155")],
            foreground=[("active", COLOR_TEXT_PRIMARY)],
        )

        # Entries & Spinboxes
        style.configure(
            "TEntry",
            fieldbackground=COLOR_SIDEBAR_ACTIVE,
            foreground=COLOR_TEXT_PRIMARY,
            insertcolor=COLOR_ACCENT,
            bordercolor=COLOR_BORDER,
            lightcolor=COLOR_BORDER,
            darkcolor=COLOR_BORDER,
            padding=4,
        )
        style.configure(
            "TSpinbox",
            fieldbackground=COLOR_SIDEBAR_ACTIVE,
            foreground=COLOR_TEXT_PRIMARY,
            arrowcolor=COLOR_TEXT_MUTED,
            bordercolor=COLOR_BORDER,
            lightcolor=COLOR_BORDER,
            darkcolor=COLOR_BORDER,
            padding=4,
        )

        # Checkbutton
        style.configure(
            "TCheckbutton",
            background=COLOR_SURFACE,
            foreground=COLOR_TEXT_PRIMARY,
            indicatorcolor=COLOR_SIDEBAR_ACTIVE,
            font=("Segoe UI", 9),
        )
        style.map("TCheckbutton", indicatorcolor=[("selected", COLOR_ACCENT)])

        # Scrollbars
        style.configure(
            "TScrollbar",
            background=COLOR_SIDEBAR_ACTIVE,
            troughcolor=COLOR_BG,
            bordercolor=COLOR_BG,
            arrowcolor=COLOR_TEXT_MUTED,
            relief="flat",
            borderwidth=0,
        )

        # Paned Window
        style.configure("TPanedwindow", background=COLOR_BG)

    def _build_layout(self):
        """Constructs the master layout: Left Sidebar + Right Content Area."""
        # Master container
        self.master_container = tk.Frame(self, bg=COLOR_BG)
        self.master_container.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar (235px wide)
        self._build_sidebar(self.master_container)

        # Right Main Area
        self.right_container = tk.Frame(self.master_container, bg=COLOR_BG)
        self.right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Top App Header
        self._build_top_header(self.right_container)

        # View Container
        self.view_container = tk.Frame(self.right_container, bg=COLOR_BG)
        self.view_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))

        # Instantiate View Components
        self.views = {
            "timetable": TimetableView(self.view_container, self.service, on_data_changed=self.refresh_all_views),
            "students": StudentView(self.view_container, self.service, on_data_changed=self.refresh_all_views),
            "subjects": SubjectView(self.view_container, self.service, on_data_changed=self.refresh_all_views),
            "faculty": FacultyView(self.view_container, self.service, on_data_changed=self.refresh_all_views),
            "rooms": RoomView(self.view_container, self.service, on_data_changed=self.refresh_all_views),
            "timeslots": TimeSlotView(self.view_container, self.service, on_data_changed=self.refresh_all_views),
            "viva_suite": VivaSuiteView(self.view_container, self.service, on_data_changed=self.refresh_all_views),
        }

        # Apply modern styling to views
        for v in self.views.values():
            if hasattr(v, "apply_theme"):
                v.apply_theme("modern")

        # Bottom Minimal Footer
        self._build_footer(self.right_container)

    def _build_sidebar(self, parent):
        """Builds modern left sidebar with logo, quick actions, navigation, and status."""
        sidebar = tk.Frame(parent, bg=COLOR_SIDEBAR, width=235)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Hairline separator on right of sidebar
        sep = tk.Frame(parent, bg=COLOR_BORDER, width=1)
        sep.pack(side=tk.LEFT, fill=tk.Y)

        # --- Brand Section ---
        brand_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR, padx=16, pady=16)
        brand_frame.pack(fill=tk.X)

        title_box = tk.Frame(brand_frame, bg=COLOR_SIDEBAR)
        title_box.pack(fill=tk.X)

        # Glowing badge icon + Title
        logo_lbl = tk.Label(
            title_box,
            text="⚡",
            font=("Segoe UI", 13),
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_SIDEBAR,
        )
        logo_lbl.pack(side=tk.LEFT, padx=(0, 6))

        title_lbl = tk.Label(
            title_box,
            text="EXAMOPT",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SIDEBAR,
        )
        title_lbl.pack(side=tk.LEFT)

        badge_lbl = tk.Label(
            title_box,
            text="v1.0",
            font=("Segoe UI", 8, "bold"),
            fg=COLOR_ACCENT,
            bg=COLOR_SIDEBAR_ACTIVE,
            padx=6,
            pady=1,
        )
        badge_lbl.pack(side=tk.RIGHT)

        sub_lbl = tk.Label(
            brand_frame,
            text="Intelligent Exam Scheduler",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SIDEBAR,
        )
        sub_lbl.pack(anchor=tk.W, pady=(4, 0))

        campus_lbl = tk.Label(
            brand_frame,
            text=f"{CAMPUS_NAME.upper()}",
            font=("Segoe UI", 7, "bold"),
            fg=COLOR_TEXT_DIM,
            bg=COLOR_SIDEBAR,
        )
        campus_lbl.pack(anchor=tk.W, pady=(1, 0))

        # Divider
        tk.Frame(sidebar, bg=COLOR_BORDER, height=1).pack(fill=tk.X, padx=12, pady=(10, 12))

        # --- Quick Actions Section ---
        actions_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR, padx=12)
        actions_frame.pack(fill=tk.X)

        action_lbl = tk.Label(
            actions_frame,
            text="QUICK ACTIONS",
            font=("Segoe UI", 7, "bold"),
            fg=COLOR_TEXT_DIM,
            bg=COLOR_SIDEBAR,
        )
        action_lbl.pack(anchor=tk.W, pady=(0, 6))

        # Quick Load Button
        load_btn = tk.Button(
            actions_frame,
            text="⚡  Load Sample Data",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_SIDEBAR_ACTIVE,
            fg=COLOR_TEXT_PRIMARY,
            activebackground=COLOR_BORDER,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor=tk.W,
            padx=10,
            pady=6,
            command=self.load_sample_dataset,
        )
        load_btn.pack(fill=tk.X, pady=2)

        # Quick Generate Timetable Button
        gen_btn = tk.Button(
            actions_frame,
            text="🚀  Generate Timetable",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_ACCENT,
            fg="#FFFFFF",
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor=tk.W,
            padx=10,
            pady=6,
            command=self._quick_generate,
        )
        gen_btn.pack(fill=tk.X, pady=(4, 8))

        # Divider
        tk.Frame(sidebar, bg=COLOR_BORDER, height=1).pack(fill=tk.X, padx=12, pady=(4, 12))

        # --- Navigation Menu ---
        nav_frame = tk.Frame(sidebar, bg=COLOR_SIDEBAR, padx=10)
        nav_frame.pack(fill=tk.BOTH, expand=True)

        nav_header = tk.Label(
            nav_frame,
            text="NAVIGATION",
            font=("Segoe UI", 7, "bold"),
            fg=COLOR_TEXT_DIM,
            bg=COLOR_SIDEBAR,
        )
        nav_header.pack(anchor=tk.W, padx=6, pady=(0, 6))

        tabs = [
            ("timetable", "📅  Master Timetable"),
            ("students", "🎓  Students & Courses"),
            ("subjects", "📚  Academic Subjects"),
            ("faculty", "👨‍🏫  Faculty & Invigilators"),
            ("rooms", "🏢  Exam Halls & Venues"),
            ("timeslots", "⏰  Time Slot Sessions"),
            ("viva_suite", "🧪  Academic Review Suite"),
        ]

        for tab_id, label in tabs:
            self._create_nav_button(nav_frame, tab_id, label)

        # --- Sidebar Footer ---
        footer_side = tk.Frame(sidebar, bg=COLOR_SIDEBAR, padx=14, pady=12)
        footer_side.pack(fill=tk.X, side=tk.BOTTOM)

        # Network Server Dialog Launcher
        net_btn = tk.Button(
            footer_side,
            text="🌐  Network & Server Daemon",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_SIDEBAR_ACTIVE,
            fg=COLOR_TEXT_PRIMARY,
            activebackground=COLOR_HOVER,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor=tk.W,
            padx=8,
            pady=4,
            command=self.open_network_dialog,
        )
        net_btn.pack(fill=tk.X, pady=(0, 6))

        # Status Pill
        self.status_pill = tk.Frame(footer_side, bg=COLOR_SIDEBAR_ACTIVE, padx=8, pady=4)
        self.status_pill.pack(fill=tk.X)

        self.sidebar_status_dot = tk.Label(self.status_pill, text="●", font=("Segoe UI", 9), fg=COLOR_SUCCESS, bg=COLOR_SIDEBAR_ACTIVE)
        self.sidebar_status_dot.pack(side=tk.LEFT, padx=(0, 4))

        self.sidebar_status_text = tk.Label(
            self.status_pill,
            text="Local SQLite Engine Active",
            font=("Segoe UI", 8, "bold"),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SIDEBAR_ACTIVE,
        )
        self.sidebar_status_text.pack(side=tk.LEFT)

        team_lbl = tk.Label(
            footer_side,
            text="Team: Suhas, Subaash, Roshan",
            font=("Segoe UI", 7),
            fg=COLOR_TEXT_DIM,
            bg=COLOR_SIDEBAR,
        )
        team_lbl.pack(anchor=tk.W, pady=(6, 0))

    def _create_nav_button(self, parent, tab_id: str, label: str):
        """Creates an interactive navigation item with an active indicator strip."""
        item_frame = tk.Frame(parent, bg=COLOR_SIDEBAR, cursor="hand2")
        item_frame.pack(fill=tk.X, pady=2)

        # Indicator strip (left 3px bar)
        indicator = tk.Frame(item_frame, bg=COLOR_SIDEBAR, width=3)
        indicator.pack(side=tk.LEFT, fill=tk.Y)

        # Text label
        lbl = tk.Label(
            item_frame,
            text=f"  {label}",
            font=("Segoe UI", 9),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SIDEBAR,
            anchor=tk.W,
            pady=7,
        )
        lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Click and hover bindings
        def on_click(e):
            self._switch_tab(tab_id)

        def on_enter(e):
            if self.current_tab_id != tab_id:
                item_frame.config(bg=COLOR_HOVER)
                lbl.config(bg=COLOR_HOVER, fg=COLOR_TEXT_PRIMARY)

        def on_leave(e):
            if self.current_tab_id != tab_id:
                item_frame.config(bg=COLOR_SIDEBAR)
                lbl.config(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUTED)

        for widget in (item_frame, indicator, lbl):
            widget.bind("<Button-1>", on_click)
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        self.nav_buttons[tab_id] = {
            "frame": item_frame,
            "indicator": indicator,
            "label": lbl,
        }

    def _build_top_header(self, parent):
        """Builds modern app header bar with contextual title and utility actions."""
        header = tk.Frame(parent, bg=COLOR_BG, padx=14, pady=12)
        header.pack(fill=tk.X)

        # Left: Active Title & Description
        title_box = tk.Frame(header, bg=COLOR_BG)
        title_box.pack(side=tk.LEFT)

        self.header_title_lbl = tk.Label(
            title_box,
            text="Exam Timetable",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG,
        )
        self.header_title_lbl.pack(anchor=tk.W)

        self.header_sub_lbl = tk.Label(
            title_box,
            text="Master examination schedule, invigilator assignments, and constraint diagnostics",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_BG,
        )
        self.header_sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        # Right: Quick utilities
        right_box = tk.Frame(header, bg=COLOR_BG)
        right_box.pack(side=tk.RIGHT)

        # Network button
        net_btn = tk.Button(
            right_box,
            text="🌐  Network",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT_PRIMARY,
            activebackground=COLOR_SIDEBAR_ACTIVE,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=5,
            command=self.open_network_dialog,
        )
        net_btn.pack(side=tk.RIGHT, padx=4)

        # Refresh button
        refresh_btn = tk.Button(
            right_box,
            text="🔄  Refresh",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT_PRIMARY,
            activebackground=COLOR_SIDEBAR_ACTIVE,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=5,
            command=self.refresh_all_views,
        )
        refresh_btn.pack(side=tk.RIGHT, padx=4)

        # About button
        about_btn = tk.Button(
            right_box,
            text="ℹ️  About",
            font=("Segoe UI", 8),
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_SIDEBAR_ACTIVE,
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=10,
            pady=5,
            command=self.show_about,
        )
        about_btn.pack(side=tk.RIGHT, padx=4)

        # Theme indicator pill
        pill = tk.Label(
            right_box,
            text="✨ Modern Dark",
            font=("Segoe UI", 8, "bold"),
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_SURFACE,
            padx=8,
            pady=4,
        )
        pill.pack(side=tk.RIGHT, padx=8)

        # Subtle bottom line
        tk.Frame(parent, bg=COLOR_BORDER, height=1).pack(fill=tk.X, padx=12, pady=(0, 8))

    def _build_footer(self, parent):
        """Builds bottom minimalist status line."""
        footer = tk.Frame(parent, bg=COLOR_BG, padx=14, pady=4)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        left_lbl = tk.Label(
            footer,
            text=f"Database: SQLite ({DATABASE_PATH})   |   Milestone: 100% Production Capstone (M1–M12 Complete)",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_DIM,
            bg=COLOR_BG,
        )
        left_lbl.pack(side=tk.LEFT)

        right_lbl = tk.Label(
            footer,
            text=f"ExamOpt v{VERSION}  •  SRM IST Tiruchirappalli",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_DIM,
            bg=COLOR_BG,
        )
        right_lbl.pack(side=tk.RIGHT)

    def _switch_tab(self, tab_id: str):
        """Switches the active content view and updates sidebar highlight state."""
        self.current_tab_id = tab_id

        # Update sidebar button states
        for tid, btn_info in self.nav_buttons.items():
            if tid == tab_id:
                btn_info["frame"].config(bg=COLOR_SIDEBAR_ACTIVE)
                btn_info["indicator"].config(bg=COLOR_ACCENT)
                btn_info["label"].config(bg=COLOR_SIDEBAR_ACTIVE, fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
            else:
                btn_info["frame"].config(bg=COLOR_SIDEBAR)
                btn_info["indicator"].config(bg=COLOR_SIDEBAR)
                btn_info["label"].config(bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 9))

        # Update Header Titles
        tab_titles = {
            "timetable": ("Master Examination Timetable", "Interactive exam scheduling, soft constraint quality, GA optimization, and exports"),
            "students": ("Student Directory & Enrollments", "Manage registered students, branches, semesters, and course enrollments"),
            "subjects": ("Academic Curriculum & Subjects", "Manage examination courses, durations, and department requirements"),
            "faculty": ("Faculty & Invigilator Roster", "Manage invigilator details and exam duty availability status"),
            "rooms": ("Examination Halls & Venues", "Manage campus seating capacity, venue availability, and maintenance"),
            "timeslots": ("Session Time Slots", "Configure examination dates, morning/afternoon session hours"),
            "viva_suite": ("Academic Review & Viva Suite", "10 Capstone verification scenarios, multi-core CPU benchmarking, and SymPy formulation"),
        }

        if tab_id in tab_titles:
            title, sub = tab_titles[tab_id]
            self.header_title_lbl.config(text=title)
            self.header_sub_lbl.config(text=sub)

        # Hide all views and show active view
        for v in self.views.values():
            v.pack_forget()

        active_view = self.views.get(tab_id)
        if active_view:
            active_view.pack(fill=tk.BOTH, expand=True)
            if hasattr(active_view, "refresh"):
                active_view.refresh()

    def refresh_all_views(self):
        """Refreshes data across all sub-views."""
        for v in self.views.values():
            if hasattr(v, "refresh"):
                v.refresh()

    def load_sample_dataset(self):
        """Loads the realistic SRM IST Tiruchirappalli sample examination dataset."""
        if messagebox.askyesno(
            "Load Sample Dataset",
            "Populate the database with realistic SRM IST Tiruchirappalli examination data?\n\n"
            "This imports subjects, students, faculty, rooms, and time slots into SQLite."
        ):
            stats = self.service.load_srm_sample_data()
            self.refresh_all_views()
            messagebox.showinfo(
                "Dataset Loaded",
                f"SRM Examination Dataset Successfully Loaded!\n\n"
                f"• Subjects: {stats['subjects']}\n"
                f"• Students: {stats['students']}\n"
                f"• Faculty: {stats['faculty']}\n"
                f"• Rooms: {stats['rooms']}\n"
                f"• Time Slots: {stats['timeslots']}\n\n"
                f"You can now generate the timetable or run review checkpoints!"
            )

    def _quick_generate(self):
        """Switches to timetable view and triggers generation."""
        self._switch_tab("timetable")
        self.views["timetable"].generate_timetable()

    def open_network_dialog(self):
        """Opens the Distributed TCP Socket Server & Connectivity dialog."""
        NetworkConnectivityDialog(self, self.service, on_status_changed=self._on_server_status_changed)

    def _on_server_status_changed(self, running: bool, endpoint: Optional[str]):
        """Callback from NetworkConnectivityDialog when server state changes."""
        if running:
            self.sidebar_status_dot.config(fg="#38BDF8")
            self.sidebar_status_text.config(text=f"TCP Server ({endpoint})", fg="#38BDF8")
        else:
            self.sidebar_status_dot.config(fg=COLOR_SUCCESS)
            self.sidebar_status_text.config(text="Local SQLite Engine Active", fg=COLOR_TEXT_MUTED)

    def _on_close(self):
        """Safely clean up background socket server if running upon window exit."""
        if getattr(self, "active_socket_server", None):
            try:
                self.active_socket_server.stop()
            except Exception:
                pass
        self.destroy()

    def show_about(self):
        """Displays modern About information dialog."""
        about_text = (
            f"{SYSTEM_NAME}\n"
            f"{INSTITUTION_NAME}, {CAMPUS_NAME}\n\n"
            f"Project Team:\n"
            f"• Suhas V A\n"
            f"• Subaash G\n"
            f"• Roshan Albert Shaiju\n\n"
            f"UI Theme: Modern Minimalist Studio (Dark Slate & Indigo)\n"
            f"Current Milestone: 100% Production Capstone (Milestones 1–12 Fully Implemented)\n"
            f"Architecture: Sockets, Multiprocessing, Genetic Algorithm, SymPy Modeling, PDF/Excel Exports"
        )
        messagebox.showinfo("About ExamOpt Modern Studio", about_text)


def start_modern_gui():
    """Entry point to launch the Modern GUI."""
    app = ExamOptModernApp()
    app.mainloop()


if __name__ == "__main__":
    start_modern_gui()
