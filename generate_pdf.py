"""
Script to generate a comprehensive, publication-quality Question Bank PDF for ExamOpt
SRM Institute of Science and Technology, Tiruchirappalli
Advanced Programming Practice (APP) - 2nd Year B.Tech CSE Core
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Numbered Canvas for dynamic "Page X of Y" and running headers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Suppress running header on page 1
        if self._pageNumber > 1:
            self.drawString(
                54, 750,
                "ExamOpt — Advanced Programming Practice (APP) Viva Question Bank | SRM IST Tiruchirappalli"
            )
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Running Footer on all pages
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — 2ND YEAR B.TECH CSE (CORE) REVIEW CHECKPOINT")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)

        self.restoreState()


def build_question_bank_pdf():
    pdf_path = os.path.abspath("c:/code/1COLLEGE/APP ExamOPS/question_bank.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY_NAVY = colors.HexColor("#0D47A1")
    DEEP_BLUE = colors.HexColor("#1565C0")
    SLATE_DARK = colors.HexColor("#0F172A")
    SLATE_BODY = colors.HexColor("#334155")
    MUTED_GRAY = colors.HexColor("#64748B")
    BG_CARD = colors.HexColor("#F8FAFC")
    BORDER_CARD = colors.HexColor("#E2E8F0")
    CODE_BG = colors.HexColor("#F1F5F9")
    AMBER_INTENT = colors.HexColor("#B45309")
    GREEN_SUCCESS = colors.HexColor("#047857")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=PRIMARY_NAVY,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=SLATE_BODY,
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=PRIMARY_NAVY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    q_title_style = ParagraphStyle(
        "QTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=DEEP_BLUE,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    intent_style = ParagraphStyle(
        "IntentStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11.5,
        textColor=AMBER_INTENT,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=SLATE_BODY,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=SLATE_BODY,
        leftIndent=12,
        spaceAfter=3,
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B"),
    )

    story = []

    # ==========================================
    # HEADER BANNER TABLE
    # ==========================================
    header_data = [
        [
            Paragraph("<b>SRM INSTITUTE OF SCIENCE AND TECHNOLOGY</b><br/>Tiruchirappalli Campus — Department of Computer Science & Engineering", ParagraphStyle("HdrInst", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.white)),
            Paragraph("<b>ACADEMIC YEAR 2026–2027</b><br/>2nd Year B.Tech CSE (Core)", ParagraphStyle("HdrYear", fontName="Helvetica", fontSize=8.5, leading=11, textColor=colors.HexColor("#E2E8F0"), alignment=2))
        ],
        [
            Paragraph("<b>EXAMOPT — ADVANCED PROGRAMMING PRACTICE (APP) VIVA QUESTION BANK</b><br/><font size=8.5 color='#BBDEFB'>50% Academic Review Checkpoint • Theoretical Proofs, Algorithmic Analysis & Code Defense</font>", ParagraphStyle("HdrMain", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=colors.white)),
            Paragraph("<b>Team Members:</b><br/>Suhas V A<br/>Subaash G<br/>Roshan Albert Shaiju", ParagraphStyle("HdrTeam", fontName="Helvetica", fontSize=8, leading=10.5, textColor=colors.HexColor("#E2E8F0"), alignment=2))
        ]
    ]

    header_table = Table(header_data, colWidths=[380, 124])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_NAVY),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("TOPPADDING", (0, 1), (-1, 1), 4),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#1E88E5")),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))

    # Introductory Note
    intro_p = Paragraph(
        "<b>Purpose & Guide:</b> This document compiles the comprehensive question bank and oral defense guide for the "
        "50% Academic Milestone Checkpoint of <b>ExamOpt</b> in the <i>Advanced Programming Practice (APP)</i> course. "
        "Questions are organized into technical pillars reflecting SRM IST evaluation rubrics: Object-Oriented Architecture, "
        "Combinatorial Algorithms, Relational Database Engineering, Academic Constraint Auditing, and Python Systems Internals.",
        body_style
    )
    story.append(intro_p)
    story.append(Spacer(1, 8))

    def add_callout_q(q_num, q_title, intent_text, answer_paragraphs, code_snippet=None):
        q_elements = []
        # Question Title
        q_elements.append(Paragraph(f"<b>Q{q_num}: {q_title}</b>", q_title_style))
        # Faculty Intent
        q_elements.append(Paragraph(f"<b>Faculty Evaluation Intent:</b> {intent_text}", intent_style))
        # Answer paragraphs
        for ans in answer_paragraphs:
            if ans.startswith("•"):
                q_elements.append(Paragraph(f"&bull; {ans[1:].strip()}", bullet_style))
            else:
                q_elements.append(Paragraph(ans, body_style))

        if code_snippet:
            code_p = Paragraph(code_snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)
            code_table = Table([[code_p]], colWidths=[490])
            code_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_CARD),
                ("PADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            q_elements.append(Spacer(1, 3))
            q_elements.append(code_table)

        q_elements.append(Spacer(1, 6))

        # Box the entire question
        outer_table = Table([[q_elements]], colWidths=[504])
        outer_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
            ("BOX", (0, 0), (-1, -1), 0.75, BORDER_CARD),
            ("LINELEFT", (0, 0), (0, 0), 3.0, PRIMARY_NAVY),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(outer_table)
        story.append(Spacer(1, 8))

    # =========================================================================
    # PILLAR 1: ARCHITECTURE & DESIGN PATTERNS
    # =========================================================================
    story.append(Paragraph("PILLAR 1: SOFTWARE ARCHITECTURE & DESIGN PATTERNS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_NAVY, spaceBefore=1, spaceAfter=8))

    add_callout_q(
        1,
        "What software design patterns are implemented in ExamOpt? Where are they in the codebase?",
        "Tests if students understand architectural separation of concerns or merely wrote an ad-hoc monolithic script.",
        [
            "ExamOpt incorporates four core Gang of Four (GoF) / Enterprise design patterns:",
            "• <b>Facade Pattern (<code>services/exam_service.py</code>):</b> <code>ExamService</code> acts as a high-level API orchestrator, decoupling UI/CLI clients from database queries, scheduling logic, and constraint validation.",
            "• <b>Data Access Object (DAO) / Repository Pattern (<code>database/database.py</code>):</b> All SQLite operations and raw SQL queries are strictly contained in <code>Database</code>. Migrating to PostgreSQL or MySQL requires changes only to this single class.",
            "• <b>Strategy Pattern (<code>scheduling/room_allocator.py</code>):</b> <code>RoomAllocator</code> encapsulates the Best-Fit capacity matching strategy independently from <code>Scheduler</code>, allowing dynamic swapping of allocation policies (e.g., First-Fit, Largest-Fit).",
            "• <b>Specification / Validator Pattern (<code>validation/validator.py</code>):</b> Academic regulations are isolated into static, pure validation functions returning standardized <code>ValidationResult</code> DTOs.",
            "• <b>Data Transfer Objects (DTO) (<code>models/*.py</code>):</b> Pure Python <code>@dataclass</code> structures decouple internal records from persistence frameworks."
        ]
    )

    add_callout_q(
        2,
        "Why did you use Python @dataclass for your models instead of standard classes or dictionaries?",
        "Evaluates mastery of modern Python OOP features (PEP 557) and defensive programming.",
        [
            "Standard dictionaries lack schema enforcement and type checking, leading to runtime <code>KeyError</code> bugs. Conversely, traditional Python classes require verbose boilerplate code for <code>__init__</code>, <code>__repr__</code>, and equality checking.",
            "We utilized <code>@dataclass</code> across all models (<code>Student</code>, <code>Subject</code>, <code>Room</code>, <code>Faculty</code>, <code>TimeSlot</code>, <code>Exam</code>) because:",
            "• <b>Boilerplate Elimination:</b> Automatically synthesizes constructor, string representation, and comparison operators.",
            "• <b>Static Typing Support:</b> Enforces type hints (e.g., <code>student_count: int = 0</code>, <code>is_available: bool = True</code>).",
            "• <b>Explicit Serialization:</b> Every model implements standardized <code>to_dict()</code> and <code>from_dict()</code> methods, enabling two-way translation between SQLite records, GUI widgets, and upcoming TCP socket JSON messages."
        ]
    )

    add_callout_q(
        3,
        "Explain the flow of data when a user clicks 'Generate Timetable' in the GUI.",
        "Checks end-to-end trace comprehension across the tiered architecture.",
        [
            "The data flow strictly adheres to top-down delegation without circular dependencies:",
            "1. <b>Presentation Layer (<code>gui/views/timetable_view.py</code>):</b> User clicks the button; the event handler invokes <code>self.service.generate_timetable()</code>.",
            "2. <b>Service Layer (<code>services/exam_service.py</code>):</b> Extracts active subjects, faculty, rooms, timeslots, and enrollment mappings from <code>Database</code>.",
            "3. <b>Scheduling Engine (<code>scheduling/scheduler.py</code>):</b> Sorts subjects by enrollment descending (MRV heuristic) and checks candidate timeslots.",
            "4. <b>Allocation Strategy (<code>scheduling/room_allocator.py</code>):</b> Assigns the smallest suitable unbooked hall via Best-Fit.",
            "5. <b>Constraint Auditing (<code>validation/validator.py</code>):</b> Performs defensive 6-point validation on candidate assignments.",
            "6. <b>Persistence & View Update:</b> The service commits the generated exams to SQLite and updates the GUI Treeview."
        ]
    )

    # =========================================================================
    # PILLAR 2: ALGORITHMS & COMPLEXITY
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("PILLAR 2: ALGORITHMS, HEURISTICS & COMPUTATIONAL COMPLEXITY", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_NAVY, spaceBefore=1, spaceAfter=8))

    add_callout_q(
        4,
        "What is the computational complexity of the Examination Timetabling Problem (ETP)? Why not use Brute Force?",
        "Probes foundational Discrete Mathematics, Graph Theory, and Analysis of Algorithms knowledge.",
        [
            "The Examination Timetabling Problem is a proven <b>NP-hard combinatorial optimization problem</b> (reducible to Graph Vertex Coloring and Bin Packing).",
            "Given $S$ subjects, $T$ timeslots, $R$ rooms, and $F$ faculty members, the brute-force search space is $O((T \\times R \\times F)^S)$.",
            "For our realistic SRM dataset (6 subjects, 6 slots, 7 rooms, 6 faculty): $(6 \\times 7 \\times 6)^6 = 252^6 \\approx 2.56 \\times 10^{14}$ combinations. For an entire university semester (50 subjects), the search space exceeds $10^{100}$ states, which is mathematically impossible to evaluate before the heat death of the universe.",
            "Hence, ExamOpt employs a <b>greedy heuristic constraint satisfaction algorithm</b> that solves the timetable in $O(S \\cdot T \\cdot R)$ time, terminating in under 10 milliseconds."
        ]
    )

    add_callout_q(
        5,
        "Explain the Most Constrained Variable (MCV / MRV) Heuristic in scheduler.py.",
        "Verifies that students understand why their heuristic works rather than just copying search code.",
        [
            "In Constraint Satisfaction Problems (CSP), the <b>Most Constrained Variable (MCV)</b> (also known as the Minimum Remaining Values or <i>Fail-First</i> principle) dictates that the variable with the fewest valid options should be assigned first.",
            "In <code>scheduling/scheduler.py</code>, we apply this by sorting subjects descending by enrolled student count:",
            "<code>sorted_subjects = sorted(subjects, key=lambda s: len(students_by_subject[s.id]), reverse=True)</code>",
            "<b>Why this is optimal:</b> High-enrollment courses (e.g., 80 students) require large auditoriums (which are scarce) and create student conflicts across multiple departments. If small classes are scheduled first, they consume large halls or block optimal slots, forcing massive backtracking later. Placing large courses first guarantees early feasibility."
        ]
    )

    add_callout_q(
        6,
        "Explain the Best-Fit Room Allocation algorithm. What is its advantage over First-Fit?",
        "Assesses understanding of resource fragmentation and classic bin-packing heuristics.",
        [
            "Assigning classrooms to exams is an instance of the <b>Bin Packing Problem</b>.",
            "• <b>First-Fit Flaw:</b> Simply assigns the first available room where $Capacity \\ge Students$. If a 15-student elective runs first, First-Fit might allocate the 120-seat Auditorium, stranding a 70-student engineering course later with no hall large enough.",
            "• <b>Best-Fit Strategy:</b> Filters unbooked, active rooms where $Capacity \\ge Students$, then sorts them ascending by capacity: <code>suitable_rooms.sort(key=lambda r: (r.capacity, r.name))</code>.",
            "• <b>Mathematical Objective:</b> Minimizes wasted seat capacity $(Capacity(r) - Students)$ per slot, preserving high-capacity venues for high-capacity cohorts."
        ],
        code_snippet="def allocate_best_fit_room(student_count, slot_id, rooms, schedule):\n    available = get_available_rooms_for_slot(slot_id, rooms, schedule)\n    suitable = [r for r in available if r.capacity >= student_count]\n    if not suitable:\n        return None, 'CAPACITY_EXCEEDED'\n    suitable.sort(key=lambda r: (r.capacity, r.name)) # Smallest adequate room\n    return suitable[0], 'OK'"
    )

    add_callout_q(
        7,
        "How is student collision detected? What data structures make this operation fast?",
        "Checks if students understand hash-based data structures versus naive quadratic list searches.",
        [
            "Two exams $E_1$ and $E_2$ scheduled in the same timeslot clash if any student is enrolled in both subjects: $\\text{Cohort}(E_1) \\cap \\text{Cohort}(E_2) \\ne \\emptyset$.",
            "In <code>validation/validator.py</code>, we implement this using <b>Python Sets (hash tables)</b>:",
            "<code>current_students_set = set(enrolled_students)</code><br/>"
            "<code>overlap = current_students_set.intersection(set(other_students))</code>",
            "<b>Complexity Comparison:</b>",
            "• Naive nested list iteration: $O(N_1 \\times N_2)$ quadratic comparisons.",
            "• Hash Set Intersection: $O(\\min(N_1, N_2))$ average time. In a university with thousands of enrollments, set intersection executes in microseconds."
        ]
    )

    # =========================================================================
    # PILLAR 3: DATABASE & SQL ENGINEERING
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("PILLAR 3: DATABASE ENGINEERING & DATA INTEGRITY (SQLITE)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_NAVY, spaceBefore=1, spaceAfter=8))

    add_callout_q(
        8,
        "What Normal Form is your database schema in? Explain your table relationships.",
        "Tests core DBMS theory: functional dependencies, normalization, and relational modeling.",
        [
            "The database schema in <code>database/schema.py</code> is normalized to <b>3rd Normal Form (3NF)</b>:",
            "• <b>1NF:</b> All attributes are atomic (no repeating groups or multi-valued columns).",
            "• <b>2NF:</b> All non-key attributes are fully functionally dependent on the entire primary key.",
            "• <b>3NF:</b> No transitive functional dependencies exist ($X \\to Y \\to Z$).",
            "<b>Relational Decomposition:</b> The many-to-many relationship between <code>students</code> and <code>subjects</code> is resolved via the associative junction table <code>enrollments</code> with a composite primary key <code>PRIMARY KEY (student_id, subject_id)</code>."
        ]
    )

    add_callout_q(
        9,
        "Why did you explicitly execute 'PRAGMA foreign_keys = ON;'? Explain your cascade rules.",
        "Evaluates practical knowledge of SQLite quirks and referential integrity maintenance.",
        [
            "By default in SQLite 3, foreign key constraints are disabled for backwards compatibility with legacy applications. To enforce relational integrity, we explicitly execute <code>PRAGMA foreign_keys = ON;</code> upon opening every connection.",
            "<b>Deliberate Cascading Rules:</b>",
            "• <code>enrollments</code> table: <code>FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE</code>. If a student withdraws or is deleted, all their subject registrations vanish automatically, preventing orphaned 'ghost' enrollments.",
            "• <code>exams</code> table: <code>FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL</code>. If a physical room is decommissioned, the scheduled exam remains intact but its <code>room_id</code> reverts to <code>NULL</code>, signaling administrators to reallocate a venue."
        ]
    )

    add_callout_q(
        10,
        "Why did you create indices on foreign keys? What is the performance impact?",
        "Checks indexing mechanics, B-trees, and query optimization.",
        [
            "In relational databases, primary keys are indexed automatically using B-Trees, but foreign keys are not.",
            "During timetable validation, the engine repeatedly executes queries such as:<br/>"
            "<code>SELECT student_id FROM enrollments WHERE subject_id = ?;</code> and <code>SELECT * FROM exams WHERE slot_id = ?;</code>",
            "Without indices, SQLite must perform a full-table sequential scan ($O(N)$).",
            "We created explicit secondary B-Tree indices in <code>database/schema.py</code>:<br/>"
            "• <code>CREATE INDEX idx_enrollments_subject ON enrollments(subject_id);</code><br/>"
            "• <code>CREATE INDEX idx_exams_slot ON exams(slot_id);</code><br/>"
            "This drops query lookups from $O(N)$ full table scans to $O(\\log N)$ index searches."
        ]
    )

    add_callout_q(
        11,
        "How do you ensure ACID transactions and protect against SQL Injection?",
        "Assesses transaction management, data safety, and secure programming practices.",
        [
            "• <b>Atomicity & Consistency (ACID):</b> In <code>database/database.py</code>, all modifications are wrapped in Python's context manager: <code>with self.get_connection() as conn:</code>. If an exception occurs, the transaction automatically rolls back. If all statements execute successfully, <code>conn.commit()</code> commits all changes atomically.",
            "• <b>SQL Injection Prevention:</b> Every SQL command strictly utilizes parameterized queries with <code>?</code> placeholders (e.g., <code>cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))</code>). String concatenation (<code>f'SELECT ... {id}'</code>) is strictly prohibited across the codebase, neutralizing SQL injection vectors."
        ]
    )

    # =========================================================================
    # PILLAR 4: TESTING & 50% CHECKPOINTS
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("PILLAR 4: CONSTRAINT VALIDATION & THE 5 MILESTONE CHECKPOINTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_NAVY, spaceBefore=1, spaceAfter=8))

    add_callout_q(
        12,
        "What are the 5 Milestone 6 Review Scenarios and what does each test verify?",
        "Directly tests compliance with the Milestone 6 academic review requirements.",
        [
            "The 5 mandatory review scenarios in <code>tests/test_scenarios.py</code> verify all hard constraints under isolated harnesses:",
            "• <b>Test 1 (Valid Data Schedule Generation):</b> Populates the realistic SRM sample dataset across CSE, IT, and ECE. Asserts that all 6 exams are scheduled and that <code>Validator.validate_full_timetable()</code> returns <code>is_valid == True</code>.",
            "• <b>Test 2 (Student Conflict Detection):</b> Assigns two subjects sharing enrolled students (RA03, RA04) to the same slot. Asserts rejection with status <code>ValidationCode.CONFLICT</code>.",
            "• <b>Test 3 (Capacity Exceeded Detection):</b> Attempts to schedule 54 students into a 30-capacity lab. Asserts rejection with status <code>ValidationCode.CAPACITY_EXCEEDED</code> and verifies the 24-seat deficit calculation.",
            "• <b>Test 4 (Duplicate Room Booking):</b> Books two distinct exams in the same room and same timeslot. Asserts rejection with status <code>ValidationCode.DUPLICATE_BOOKING</code>.",
            "• <b>Test 5 (Resource Availability Rejection):</b> Schedules exams with a room under renovation or a professor on medical leave. Asserts rejections with <code>ROOM_UNAVAILABLE</code> and <code>FACULTY_UNAVAILABLE</code>."
        ]
    )

    add_callout_q(
        13,
        "Why do unit tests use an in-memory database (:memory:) instead of the disk database?",
        "Evaluates professional test hygiene and isolation.",
        [
            "In <code>tests/test_crud.py</code> and <code>tests/test_scenarios.py</code>, we instantiate the database with <code>Database(':memory:')</code>.",
            "<b>Engineering Advantages:</b>",
            "• <b>Test Isolation & Idempotence:</b> Each test runs on a pristine RAM database. Tests cannot contaminate each other or corrupt production <code>examopt.db</code> data.",
            "• <b>Zero Disk I/O Latency:</b> Memory reads/writes execute in nanoseconds, allowing our entire 24-test suite to complete in <b>0.010 seconds</b>.",
            "• <b>Automatic Teardown:</b> Once test execution finishes, RAM is released instantly with no residual scratch files."
        ]
    )

    # =========================================================================
    # PILLAR 5: PYTHON INTERNALS & POST-50% ROADMAP
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("PILLAR 5: PYTHON SYSTEMS INTERNALS & THE POST-50% ROADMAP", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_NAVY, spaceBefore=1, spaceAfter=8))

    add_callout_q(
        14,
        "Why does your roadmap mandate Multiprocessing instead of Threading for schedule search?",
        "The quintessential Python systems interview question: The Global Interpreter Lock (GIL).",
        [
            "In CPython, the <b>Global Interpreter Lock (GIL)</b> is a mutex that prevents multiple native OS threads from executing Python bytecodes simultaneously.",
            "• <b>I/O-Bound vs. CPU-Bound Tasks:</b> Threading is effective for network I/O or GUI responsiveness (waiting for user clicks). However, timetable optimization (evaluating thousands of candidate permutations) is purely <b>CPU-bound mathematical computation</b>.",
            "• <b>Multiprocessing Solution:</b> By deploying Python's <code>multiprocessing</code> module (specifically <code>ProcessPoolExecutor</code>), we spawn separate operating system processes. Each process hosts its own independent Python interpreter and memory space, bypassing the GIL and unlocking 100% parallel computation across all CPU cores."
        ]
    )

    add_callout_q(
        15,
        "How will the TCP Socket Client-Server architecture work in Milestone 7?",
        "Checks technical clarity on the upcoming networking milestone.",
        [
            "Currently, ExamOpt runs as a desktop application. In Milestone 7, we will decouple it into a distributed network architecture:",
            "• <b>Socket Server (<code>exam_server.py</code>):</b> A standalone daemon listening on a dedicated TCP port (e.g., 8080) using Python's low-level <code>socket</code> library.",
            "• <b>Message Protocol:</b> Requests and responses will be serialized as UTF-8 encoded JSON payloads (e.g., <code>{'command': 'GENERATE_SCHEDULE', 'payload': ...}</code>).",
            "• <b>Architectural Advantage:</b> Because we already encapsulated all business logic in <code>ExamService</code> and implemented <code>to_dict()</code>/<code>from_dict()</code> on domain models, the socket server simply unmarshals JSON, delegates to <code>ExamService</code>, and marshals the resulting <code>ScheduleReport</code> back over the network socket."
        ]
    )

    add_callout_q(
        16,
        "How will Functional Programming (map, filter, reduce) be used in Milestone 8?",
        "Evaluates functional paradigm application within the course curriculum.",
        [
            "In Milestone 8, schedule evaluation will be rewritten from imperative loops to pure functional pipelines:",
            "• <code>filter()</code>: Isolate exams violating soft preferences (e.g., extracting students scheduled for consecutive exam slots).",
            "• <code>map()</code>: Calculate mathematical penalty scores or venue occupancy ratios for each scheduled exam.",
            "• <code>functools.reduce()</code>: Aggregate individual penalty scores into a single scalar fitness value for the entire timetable without mutating global state."
        ]
    )

    add_callout_q(
        17,
        "What is the difference between Hard Constraints and Soft Constraints in ExamOpt?",
        "Distinguishes binary constraint satisfaction from mathematical objective optimization.",
        [
            "• <b>Hard Constraints (Milestones 1–6):</b> Mandatory physical and institutional laws (binary satisfaction: must have 0 violations). Examples: no student exam clash, no room double-booking, no seating capacity overflow, and no unavailable staff. If any hard constraint fails, the timetable is completely invalid.",
            "• <b>Soft Constraints (Milestones 10–11):</b> Desirable academic preferences evaluated via a cost/fitness function. Examples: maximizing rest days between exams for students, balancing invigilation duty hours evenly among professors, and avoiding exams on Saturday afternoons. Timetables are scored and optimized using Genetic Algorithms to minimize total penalty cost."
        ]
    )

    # =========================================================================
    # PILLAR 6: VIVA DEFENSE & RAPID-FIRE TRICK QUESTIONS
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("PILLAR 6: VIVA DEFENSE & RAPID-FIRE TRICK QUESTIONS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_NAVY, spaceBefore=1, spaceAfter=8))

    rapid_fire_data = [
        [
            Paragraph("<b>Examiner Challenge / Trick Question</b>", ParagraphStyle("TH1", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white)),
            Paragraph("<b>Exact Model Response & Code Pointer</b>", ParagraphStyle("TH2", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white))
        ],
        [
            Paragraph("<i>'What happens if 500 students enroll in a subject and the largest auditorium seats only 120?'</i>", body_style),
            Paragraph("The <code>RoomAllocator</code> detects that no room satisfies <code>capacity >= 500</code>. It returns <code>(None, 'CAPACITY_EXCEEDED')</code>. The <code>Scheduler</code> marks the exam as <code>Unscheduled</code> with an explicit capacity error rather than crashing or overflowing a room.", body_style)
        ],
        [
            Paragraph("<i>'Can two exams happen in the same room at the same time if they are different subjects?'</i>", body_style),
            Paragraph("<b>Never.</b> <code>Validator.validate_assignment()</code> explicitly checks <code>other.slot_id == exam.slot_id and other.room_id == exam.room_id</code> and rejects the assignment with <code>DUPLICATE_BOOKING</code>.", body_style)
        ],
        [
            Paragraph("<i>'Show me your code handles faculty on leave.'</i>", body_style),
            Paragraph("In <code>scheduling/scheduler.py</code>, we filter <code>available_faculty = [f for f in faculty_list if f.is_available]</code>. Furthermore, Test 5 in <code>tests/test_scenarios.py</code> specifically verifies that assigning an unavailable faculty triggers <code>FACULTY_UNAVAILABLE</code>.", body_style)
        ],
        [
            Paragraph("<i>'What was your individual contribution to the project?'</i>", body_style),
            Paragraph("Clearly state your designated module: e.g., <i>'I engineered the 3NF SQLite schema, DAO layer, and transactional CRUD operations in <code>database/</code>'</i>, or <i>'I designed the 6-point constraint validation engine and automated test suites in <code>validation/</code> and <code>tests/</code>'</i>, or <i>'I implemented the MRV heuristic scheduler and Best-Fit room allocation in <code>scheduling/</code>'</i>.", body_style)
        ]
    ]

    rf_table = Table(rapid_fire_data, colWidths=[180, 324])
    rf_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_CARD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(rf_table)
    story.append(Spacer(1, 12))

    # ==========================================
    # APPENDIX: TERMINAL COMMANDS CHEATSHEET
    # ==========================================
    story.append(Paragraph("APPENDIX: TERMINAL COMMANDS CHEATSHEET", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_NAVY, spaceBefore=1, spaceAfter=8))

    cmd_data = [
        [Paragraph("<b>Command Line Instruction</b>", ParagraphStyle("CH1", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Description / Viva Demonstration Purpose</b>", ParagraphStyle("CH2", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white))],
        [Paragraph("<code>python main.py</code>", code_style), Paragraph("Launches the Modern Obsidian Studio desktop interface (Default).", body_style)],
        [Paragraph("<code>python main.py --theme classic</code>", code_style), Paragraph("Launches the Classic University Tabbed Notebook desktop interface.", body_style)],
        [Paragraph("<code>python main.py --cli</code>", code_style), Paragraph("Executes full end-to-end demonstration in CLI mode (ideal for headless lab PCs).", body_style)],
        [Paragraph("<code>python main.py --scenarios</code>", code_style), Paragraph("Directly runs and evaluates the 5 mandatory Milestone 6 academic scenarios.", body_style)],
        [Paragraph("<code>python -m unittest discover tests -v</code>", code_style), Paragraph("Runs the complete 24-test automated verification suite (~0.010s execution).", body_style)],
    ]
    cmd_table = Table(cmd_data, colWidths=[200, 304])
    cmd_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DEEP_BLUE),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_CARD),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_CARD]),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(cmd_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Question bank PDF successfully built at: {pdf_path}")

    # On Windows, question_bank.pdf is already accessible as Question_Bank.pdf
    print(f"Question Bank PDF ready at: {pdf_path}")

if __name__ == "__main__":
    build_question_bank_pdf()
