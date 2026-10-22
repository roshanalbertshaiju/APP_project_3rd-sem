"""
Script to generate a comprehensive, professionally styled Word document (.docx)
for the ExamOpt Intern Onboarding and Technical Architecture Manual.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding for a table cell (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """Configures borders for a table cell using XML."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    
    border_specs = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for border_name, spec in border_specs.items():
        if spec:
            val, sz, space, color = spec
            element = parse_xml(
                f'<w:{border_name} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="{space}" w:color="{color}"/>'
            )
            borders.append(element)
        else:
            element = parse_xml(f'<w:{border_name} {nsdecls("w")} w:val="none"/>')
            borders.append(element)
    tcPr.append(borders)

def add_callout(doc, title, text, layman_text=None, border_color="0D47A1", bg_color="F0F4F8"):
    """Adds a stylish callout box with a colored left accent border and shaded background."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    set_cell_borders(cell, left=("single", "36", "0", border_color),
                           top=None, bottom=None, right=None)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"📌 {title}\n")
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(11)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(13, 71, 161)
    
    run_tech = p.add_run(f"Technical Definition: ")
    run_tech.font.name = "Segoe UI"
    run_tech.font.size = Pt(10)
    run_tech.font.bold = True
    run_tech.font.color.rgb = RGBColor(30, 41, 59)
    
    run_desc = p.add_run(f"{text}\n")
    run_desc.font.name = "Segoe UI"
    run_desc.font.size = Pt(10)
    run_desc.font.color.rgb = RGBColor(51, 65, 85)
    
    if layman_text:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(4)
        p2.paragraph_format.space_after = Pt(2)
        run_lay_label = p2.add_run("💡 In Layman's Terms: ")
        run_lay_label.font.name = "Segoe UI"
        run_lay_label.font.size = Pt(10)
        run_lay_label.font.bold = True
        run_lay_label.font.color.rgb = RGBColor(180, 83, 9)  # Warm amber/brown
        
        run_lay_desc = p2.add_run(layman_text)
        run_lay_desc.font.name = "Segoe UI"
        run_lay_desc.font.size = Pt(10)
        run_lay_desc.font.italic = True
        run_lay_desc.font.color.rgb = RGBColor(67, 56, 202)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, caption=""):
    """Adds a monospace formatted code snippet block."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    set_cell_borders(cell, left=("single", "24", "0", "94A3B8"),
                           top=("single", "6", "0", "E2E8F0"),
                           bottom=("single", "6", "0", "E2E8F0"),
                           right=("single", "6", "0", "E2E8F0"))
    
    if caption:
        p_cap = cell.paragraphs[0]
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(4)
        run_cap = p_cap.add_run(f"Listing: {caption}")
        run_cap.font.name = "Segoe UI"
        run_cap.font.size = Pt(8.5)
        run_cap.font.bold = True
        run_cap.font.color.rgb = RGBColor(100, 116, 139)
        p_code = cell.add_paragraph()
    else:
        p_code = cell.paragraphs[0]

    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.15
    run = p_code.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(30, 41, 59)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def style_table(table, col_widths, headers, data, align_cols=None):
    """Styles a standard data table with a navy header and alternating striped rows."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_background(hdr_cells[i], "0D47A1")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        set_cell_borders(hdr_cells[i], bottom=("single", "18", "0", "0A387E"))
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        if align_cols and i in align_cols:
            p.alignment = align_cols[i]
        for run in p.runs:
            run.font.name = "Segoe UI"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Data rows
    for row_idx, row_data in enumerate(data):
        row = table.add_row()
        cells = row.cells
        bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            cells[col_idx].text = str(cell_value)
            set_cell_background(cells[col_idx], bg_color)
            set_cell_margins(cells[col_idx], top=80, bottom=80, left=120, right=120)
            set_cell_borders(cells[col_idx], bottom=("single", "4", "0", "E2E8F0"),
                                           top=("single", "4", "0", "E2E8F0"))
            p = cells[col_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            if align_cols and col_idx in align_cols:
                p.alignment = align_cols[col_idx]
            for run in p.runs:
                run.font.name = "Segoe UI"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(51, 65, 85)

    # Set column widths across all rows
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)

def build_document():
    doc = Document()
    
    # 1. Page Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header / Footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = p_ft.add_run("ExamOpt — Intern Engineering Manual | SRM IST Tiruchirappalli")
        f_run.font.name = "Segoe UI"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(148, 163, 184)

    # Helper for headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(17)
        run.font.bold = True
        run.font.color.rgb = RGBColor(13, 71, 161)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(21, 101, 192)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Segoe UI"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(15, 23, 42)
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Segoe UI"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(15, 23, 42)
        r = p.add_run(text)
        r.font.name = "Segoe UI"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(51, 65, 85)
        return p

    # ==========================================
    # COVER / HEADER BANNER
    # ==========================================
    banner_table = doc.add_table(rows=1, cols=1)
    banner_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner_table.autofit = False
    b_cell = banner_table.cell(0, 0)
    b_cell.width = Inches(6.5)
    set_cell_background(b_cell, "0D47A1")
    set_cell_margins(b_cell, top=260, bottom=260, left=240, right=240)
    
    bp1 = b_cell.paragraphs[0]
    bp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    br1 = bp1.add_run("EXAMOPT — SYSTEM ARCHITECTURE &\nINTERN ONBOARDING MANUAL")
    br1.font.name = "Segoe UI"
    br1.font.size = Pt(19)
    br1.font.bold = True
    br1.font.color.rgb = RGBColor(255, 255, 255)
    
    bp2 = b_cell.add_paragraph()
    bp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bp2.paragraph_format.space_before = Pt(8)
    br2 = bp2.add_run("Intelligent Examination Scheduling and Optimization System")
    br2.font.name = "Segoe UI"
    br2.font.size = Pt(12)
    br2.font.color.rgb = RGBColor(187, 222, 251)

    bp3 = b_cell.add_paragraph()
    bp3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bp3.paragraph_format.space_before = Pt(4)
    br3 = bp3.add_run("SRM Institute of Science and Technology, Tiruchirappalli Campus\nProject Team: Suhas V A, Subaash G, Roshan Albert Shaiju | Version 0.5.0")
    br3.font.name = "Segoe UI"
    br3.font.size = Pt(9.5)
    br3.font.color.rgb = RGBColor(227, 242, 253)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==========================================
    # SECTION 1: EXECUTIVE SUMMARY
    # ==========================================
    add_h1("1. Executive Summary & Project Purpose")
    add_p(
        "ExamOpt is an automated, intelligent examination timetable scheduling and optimization engine developed "
        "for university academic operations. In higher-education institutions like SRM IST Tiruchirappalli, generating "
        "an end-of-semester examination timetable manually is an exhausting, multi-week logistical nightmare. "
        "Administrators must ensure that no student has two exams at the same time, no faculty is assigned to multiple "
        "rooms simultaneously, rooms have enough seating capacity without wasting hall space, and unavailable staff "
        "or rooms under maintenance are never scheduled."
    )
    add_p(
        "ExamOpt solves this problem through automated combinatorial optimization. Given a dataset of courses, "
        "enrolled students, classrooms, faculty members, and available exam slots, it generates a mathematically verified, "
        "conflict-free timetable in under 100 milliseconds."
    )
    
    add_callout(
        doc,
        title="Why You Are Handed This Codebase",
        text="The project has achieved its 50% Academic Milestone Checkpoint. The foundational Clean Architecture, "
             "relational SQLite database, 6-point constraint validation engine, Best-Fit room allocation algorithm, "
             "Tkinter desktop GUI, and full 24-test verification suite are completely operational. Your role as an intern "
             "is to take this proven foundation and extend it into advanced optimization, network sockets, and parallel computing.",
        layman_text="The solid concrete foundation and steel pillars of the house are built, tested, and inspected. "
                    "You are now stepping in to build the upper floors, smart electrical wiring, and high-speed elevator!"
    )

    # ==========================================
    # SECTION 2: SYSTEM ARCHITECTURE
    # ==========================================
    add_h1("2. System Architecture & Design Patterns")
    add_p(
        "ExamOpt adheres strictly to Clean Layered Architecture and Loose Coupling. High-level presentation components "
        "never directly touch SQL statements or execute scheduling algorithms; instead, each layer delegates responsibility "
        "to specialized components underneath it."
    )

    add_h2("2.1 Layered Structure Diagram")
    add_code_block(
        doc,
        "┌─────────────────────────────────────────────────────────────┐\n"
        "│       PRESENTATION LAYER (Tkinter Desktop GUI / CLI)         │\n"
        "│       gui/app.py | gui/views/*.py | main.py                │\n"
        "└──────────────────────────────┬──────────────────────────────┘\n"
        "                               │ High-level API calls\n"
        "                               ▼\n"
        "┌─────────────────────────────────────────────────────────────┐\n"
        "│         APPLICATION SERVICE FACADE (services/exam_service)   │\n"
        "│       Coordinates timetable generation, validation & CSV    │\n"
        "└──────────────┬──────────────────────────────┬───────────────┘\n"
        "               │                              │\n"
        "               ▼                              ▼\n"
        "┌──────────────────────────────┐┌──────────────────────────────┐\n"
        "│      SCHEDULING ENGINE       ││ CONSTRAINT VALIDATION ENGINE │\n"
        "│     scheduling/scheduler     ││     validation/validator     │\n"
        "│   (MRV Greedy Heuristic)     ││   (6-point rule checks)      │\n"
        "└──────────────┬───────────────┘└──────────────┬───────────────┘\n"
        "               │                               │\n"
        "               ▼                               │\n"
        "┌──────────────────────────────┐               │\n"
        "│     ROOM ALLOCATOR ENGINE    │               │\n"
        "│   scheduling/room_allocator  │               │\n"
        "│  (Best-Fit Capacity Matcher) │               │\n"
        "└──────────────────────────────┘               ▼\n"
        "                                ┌──────────────────────────────┐\n"
        "                                │   PERSISTENCE LAYER (DAO)    │\n"
        "                                │     database/database.py     │\n"
        "                                │      (SQLite3 Backend)       │\n"
        "                                └──────────────────────────────┘",
        caption="Clean Architecture & Dependency Flow"
    )

    add_h2("2.2 Key Software Design Patterns")
    add_bullet(
        "ExamService acts as a single, unified gateway for all operations. Whether a user clicks 'Generate Timetable' "
        "in the GUI or runs `python main.py --cli`, they call `ExamService.generate_timetable()`. The UI does not need to know "
        "about SQL queries, room sorting logic, or validation loops.",
        bold_prefix="1. Facade Pattern: "
    )
    add_bullet(
        "All database operations are encapsulated in `Database` (database/database.py). No SQL queries are leaked into views, "
        "models, or schedulers. If the storage backend ever changes from SQLite to PostgreSQL, only this single file needs modification.",
        bold_prefix="2. Data Access Object (DAO) / Repository Pattern: "
    )
    add_bullet(
        "The Validator (validation/validator.py) evaluates rules independently from the scheduler. It can validate an individual "
        "candidate assignment during scheduling or perform a full audit on an existing schedule from a database.",
        bold_prefix="3. Specification / Validator Pattern: "
    )
    add_bullet(
        "The RoomAllocator (scheduling/room_allocator.py) encapsulates the Best-Fit room allocation policy as an independent strategy "
        "injected into the Scheduler, allowing future allocation algorithms (e.g., Random-Fit or Proximity-Fit) to be swapped in seamlessly.",
        bold_prefix="4. Strategy Pattern: "
    )
    add_bullet(
        "Domain entities (Student, Exam, Room, etc.) are implemented using pure Python `@dataclass` objects equipped with "
        "`to_dict()` and `from_dict()` methods, keeping business objects clean, immutable, and decoupled from persistence frameworks.",
        bold_prefix="5. Data Transfer Objects (DTO): "
    )

    # ==========================================
    # SECTION 3: DIRECTORY STRUCTURE
    # ==========================================
    add_h1("3. Comprehensive Folder & File Directory")
    add_p("The project is cleanly structured into 8 modular packages:")

    folder_table = doc.add_table(rows=1, cols=3)
    folder_headers = ["Folder / File", "Architectural Role", "Description"]
    folder_data = [
        ["main.py", "Entry Point", "Application bootstrap supporting CLI demo mode (--cli), scenario execution (--scenarios), and desktop Tkinter GUI launch."],
        ["config.py", "Global Settings", "Central constants: database paths, institution metadata, and standard status/error code classes (ValidationCode, ScheduleCode)."],
        ["models/", "Domain Entities", "Pure Python dataclasses (Student, Subject, Faculty, Room, TimeSlot, Enrollment, Exam). Free of SQL or UI dependencies."],
        ["database/", "Data Persistence", "schema.py defines normalized DDL tables and foreign keys. database.py provides thread-safe connection management and full CRUD methods."],
        ["validation/", "Rule Engine", "validator.py implements 6 rigorous hard academic constraint checks, returning structured ValidationResult objects."],
        ["scheduling/", "Optimization", "scheduler.py implements the MRV greedy timetable generator. room_allocator.py implements Best-Fit capacity room matching."],
        ["services/", "Application Layer", "exam_service.py coordinates database, scheduler, and validator operations into high-level business methods."],
        ["gui/", "Desktop Interface", "Tkinter/ttk GUI with responsive tabs for Timetable view, CRUD management of all entities, and live scenario diagnostics."],
        ["utils/", "Utilities & Data", "sample_data.py loads realistic SRM IST datasets. helpers.py provides time/date formatting and regex validation."],
        ["tests/", "Test Suite", "24 automated unit tests across CRUD (test_crud.py), validation (test_validator.py), scheduling (test_scheduler.py), and scenarios (test_scenarios.py)."]
    ]
    style_table(folder_table, [1.3, 1.4, 3.8], folder_headers, folder_data)

    # ==========================================
    # SECTION 4: CORE CONCEPTS
    # ==========================================
    add_h1("4. Core Concepts: Technical Analysis vs. Layman's Terms")
    add_p(
        "To help you master the engineering decisions behind ExamOpt, each major computer science concept used in "
        "the project is explained below with both its rigorous technical definition and a simplified layman's analogy."
    )

    add_callout(
        doc,
        title="Concept 1: Constraint Satisfaction Problem (CSP)",
        text="Timetable generation is an NP-complete combinatorial optimization problem. Formally defined as a triple "
             "(X, D, C), where X is a set of exam variables {X1, X2, ... Xn}, D is their domain of values (combinations of time "
             "slots, rooms, and faculty), and C is a set of constraints that must be satisfied without violation.",
        layman_text="Imagine playing a gigantic game of Sudoku, but instead of putting numbers 1 through 9 into a grid, "
                    "you are assigning university exams into time slots. No two overlapping exams can share the same room "
                    "or have the same students, just like numbers cannot repeat in the same row or column."
    )

    add_callout(
        doc,
        title="Concept 2: Most Constrained Variable (MRV) Greedy Heuristic",
        text="In CSP search algorithms, variable ordering determines computational efficiency. ExamOpt applies the MRV heuristic "
             "(also known as the minimum-remaining-values or fail-first heuristic) by sorting subjects descending by their enrolled "
             "student count before scheduling. Exams with high enrollment are hardest to satisfy because they restrict the search space "
             "the most and demand high-capacity rooms.",
        layman_text="Think of packing a suitcase with large bowling balls and small marbles. If you pack the marbles first, "
                    "you will never fit the bowling balls. But if you pack the heavy bowling balls (huge 120-student exams) first, "
                    "the marbles (small 15-student elective exams) easily slip into the leftover spaces!"
    )

    add_callout(
        doc,
        title="Concept 3: Best-Fit Room Allocation (Bin Packing Problem)",
        text="Assigning exams to examination halls is a classic Bin Packing optimization. Given an exam with student count N "
             "and a set of available unbooked rooms R where capacity(r) >= N, the Best-Fit strategy selects room r* such that "
             "(capacity(r*) - N) is minimized. This minimizes hall fragmentation and reserves large auditoriums for large cohorts.",
        layman_text="The 'Goldilocks' rule: If you have an exam with 35 students, you shouldn't book the 120-seat Main Auditorium "
                    "if the 40-seat Seminar Hall is empty! Booking the smallest room that comfortably fits the students keeps large "
                    "halls open for massive engineering classes."
    )

    add_callout(
        doc,
        title="Concept 4: Hard Constraints vs. Soft Constraints",
        text="Hard constraints represent absolute physical and legal boundaries (binary satisfaction: violations = 0). Soft constraints "
             "represent desirable preferences evaluated via a cost/fitness objective function. ExamOpt strictly enforces all hard "
             "constraints (no student clash, no double-booked room, no overcapacity, no unavailable personnel).",
        layman_text="A hard constraint is a law: a student cannot physically be in two classrooms at the same time. "
                    "A soft constraint is a preference: a student would prefer not having exams on two consecutive mornings. "
                    "A schedule is impossible if a hard constraint fails; it is merely annoying if a soft constraint fails."
    )

    add_callout(
        doc,
        title="Concept 5: Relational Normalization & Referential Integrity",
        text="The database implements 3rd Normal Form (3NF). Many-to-many relationships (Students <-> Subjects) are decoupled "
             "through an associative table `enrollments` with composite primary keys (student_id, subject_id) and foreign keys "
             "with ON DELETE CASCADE. Indexes are added to foreign keys to ensure O(1) query lookups during validation.",
        layman_text="Information is stored exactly once in its own folder. If a student drops out of college, deleting the student "
                    "automatically cleans up their exam registrations instantly, preventing 'ghost' registrations."
    )

    add_callout(
        doc,
        title="Concept 6: Thread-Safe SQLite Connection & Row Factory",
        text="SQLite connections are established with `check_same_thread=False` and `conn.row_factory = sqlite3.Row`. "
             "This allows the database manager to run across multiple threads (e.g. GUI background workers) and returns rows "
             "as key-indexed mappings rather than raw numeric index tuples.",
        layman_text="Instead of having to remember that column #3 is the student's name (`row[3]`), you can write `row['name']`. "
                    "If someone adds a new column to the database in the future, your code won't mysteriously break!"
    )

    # ==========================================
    # SECTION 5: CODEBASE DEEP DIVE
    # ==========================================
    add_h1("5. Codebase Deep Dive: Modules, Classes & Key Methods")
    add_p(
        "Here is the detailed technical inspection of each core class, explaining how the code is structured, "
        "what its arguments represent, and how it executes."
    )

    # 5.1 Models
    add_h2("5.1 Domain Models (`models/`)")
    add_p(
        "The domain models represent pure data objects. Consider `Exam` in `models/exam.py`:"
    )
    add_code_block(
        doc,
        "@dataclass\n"
        "class Exam:\n"
        "    exam_id: str\n"
        "    subject_id: str\n"
        "    slot_id: Optional[str] = None\n"
        "    room_id: Optional[str] = None\n"
        "    faculty_id: Optional[str] = None\n"
        "    student_count: int = 0\n"
        "    status: str = 'Unscheduled'\n"
        "    status_reason: str = ''\n"
        "\n"
        "    def to_dict(self): ...\n"
        "    @classmethod\n"
        "    def from_dict(cls, data: dict): ...",
        caption="models/exam.py — Domain Entity"
    )
    add_p(
        "Explanation: An exam starts with `slot_id=None`, `room_id=None`, `faculty_id=None`, and status `'Unscheduled'`. "
        "As the scheduling engine processes it, it assigns these attributes. The helper methods `to_dict()` and `from_dict()` "
        "allow serialization for database persistence and GUI rendering."
    )

    # 5.2 Persistence
    add_h2("5.2 Database Layer (`database/database.py`)")
    add_p(
        "The `Database` class manages the SQLite database lifecycle. Key methods include:"
    )
    add_bullet(
        "Connects to the SQLite file or `:memory:`, enables foreign key enforcement (`PRAGMA foreign_keys = ON;`), "
        "and executes `schema.py` table creation DDL on startup.",
        bold_prefix="__init__(self, db_path=None): "
    )
    add_bullet(
        "Python context manager (`with self.get_connection() as conn:`) used throughout all CRUD operations. "
        "Ensures ACID transactions: automatically issues `conn.commit()` on success and rolls back on failure.",
        bold_prefix="get_connection(self): "
    )
    add_bullet(
        "Executes a parameterized SQL query across the `enrollments` table: `SELECT student_id FROM enrollments WHERE subject_id = ?`. "
        "Returns the complete list of student IDs enrolled in that subject, preventing SQL injection vulnerabilities.",
        bold_prefix="get_students_for_subject(self, subject_id): "
    )

    # 5.3 Validation
    add_h2("5.3 Constraint Validation Engine (`validation/validator.py`)")
    add_p(
        "The `Validator` class contains static evaluation methods that enforce the university's academic regulations. "
        "The core method is `validate_assignment()`:"
    )
    add_code_block(
        doc,
        "@staticmethod\n"
        "def validate_assignment(exam, existing_exams, students_by_subject, \n"
        "                        rooms_by_id, faculty_by_id, timeslots_by_id) -> ValidationResult:\n"
        "    # 1. Existence: Verify slot, room, and faculty exist\n"
        "    # 2. Availability: Ensure slot, room, and faculty are is_available == True\n"
        "    # 3. Capacity: Ensure student_count <= room.capacity\n"
        "    # 4. Duplicate Room Booking: Ensure no other exam in this slot uses this room\n"
        "    # 5. Faculty Conflict: Ensure invigilator is not in two rooms in this slot\n"
        "    # 6. Student Conflict: Ensure no student is enrolled in 2 exams in this slot\n"
        "    return ValidationResult(ValidationCode.VALID, is_valid=True, ...)",
        caption="validation/validator.py — 6-Point Academic Check"
    )
    add_p(
        "Notice Step 6: Student conflict detection uses Python sets for high performance: "
        "`overlap = set(enrolled_students).intersection(set(other_students))`. If `overlap` is non-empty, "
        "it immediately flags a `ValidationCode.CONFLICT` with the exact count and IDs of the conflicting students."
    )

    # 5.4 Scheduling & Allocation
    add_h2("5.4 Scheduling & Room Allocation Engines (`scheduling/`)")
    add_p(
        "The scheduling pipeline operates in two coordinated classes:"
    )
    add_p(
        "1. RoomAllocator (scheduling/room_allocator.py):",
        bold_prefix="Room Allocation Logic: "
    )
    add_code_block(
        doc,
        "def allocate_best_fit_room(student_count, slot_id, rooms, current_schedule):\n"
        "    available_rooms = get_available_rooms_for_slot(slot_id, rooms, current_schedule)\n"
        "    suitable_rooms = [r for r in available_rooms if r.capacity >= student_count]\n"
        "    if not suitable_rooms:\n"
        "        return None, 'CAPACITY_EXCEEDED'\n"
        "    # Best-fit: Pick smallest suitable room\n"
        "    suitable_rooms.sort(key=lambda r: (r.capacity, r.name))\n"
        "    return suitable_rooms[0], 'OK'",
        caption="scheduling/room_allocator.py — Best-Fit Allocation"
    )

    add_p(
        "2. Scheduler (scheduling/scheduler.py):",
        bold_prefix="Timetable Generation Workflow: "
    )
    add_bullet(
        "Sorts subjects descending by enrollment: `sorted(subjects, key=lambda s: len(students[s.id]), reverse=True)`.",
        bold_prefix="Step A (MRV Sort): "
    )
    add_bullet(
        "Iterates over active time slots. For each slot, checks if any student in this subject is already writing an exam.",
        bold_prefix="Step B (Slot Testing): "
    )
    add_bullet(
        "Finds an unassigned faculty member available for invigilation during this specific slot.",
        bold_prefix="Step C (Faculty Pairing): "
    )
    add_bullet(
        "Calls `room_allocator.allocate_best_fit_room()` to assign the most capacity-efficient room.",
        bold_prefix="Step D (Best-Fit Room): "
    )
    add_bullet(
        "Performs a full audit via `Validator.validate_assignment()`. If valid, registers the exam; if not, logs the failure reason and tries the next slot.",
        bold_prefix="Step E (Validator Double-Check): "
    )

    # 5.5 Services
    add_h2("5.5 Application Facade Service (`services/exam_service.py`)")
    add_p(
        "The `ExamService` class provides high-level business functions for the application:"
    )
    add_bullet(
        "Coordinates `db.get_all_subjects()`, `scheduler.generate_schedule()`, clears the old schedule, and saves new assignments into SQLite in a single call.",
        bold_prefix="generate_timetable(): "
    )
    add_bullet(
        "Audits every exam currently stored in SQLite against all academic constraints using `Validator.validate_full_timetable()`.",
        bold_prefix="validate_current_schedule(): "
    )
    add_bullet(
        "Exports scheduled exams to a formatted CSV file with columns: Exam ID, Subject Code, Name, Date, Time, Room, Capacity, Enrolled, and Invigilator.",
        bold_prefix="export_timetable_to_csv(file_path): "
    )

    # 5.6 GUI & CLI
    add_h2("5.6 Desktop GUI (`gui/`) & CLI Entry Point (`main.py`)")
    add_p(
        "The user interface is built using standard Python `tkinter` and `tkinter.ttk` (no external GUI dependencies required):"
    )
    add_bullet(
        "Main desktop window containing an institution banner, quick action buttons, hamburger menu, and a tabbed `ttk.Notebook`.",
        bold_prefix="gui/app.py: "
    )
    add_bullet(
        "Displays the generated timetable in a sortable, formatted `ttk.Treeview` table, equipped with 'Quick Generate', 'Validate Constraints', and 'Export CSV' buttons.",
        bold_prefix="gui/views/timetable_view.py: "
    )
    add_bullet(
        "Interactive dashboard allowing administrators to click 'Run 50% Review Checkpoints' to live-test and display the 5 academic review scenarios.",
        bold_prefix="gui/views/verification_view.py: "
    )
    add_bullet(
        "Handles command-line arguments (`--cli`, `--scenarios`), sets up UTF-8 logging, and automatically falls back to CLI mode if running in a headless environment.",
        bold_prefix="main.py: "
    )

    # ==========================================
    # SECTION 6: REVIEW SCENARIOS
    # ==========================================
    add_h1("6. Milestone 6 Review Scenarios (The 5 Academic Checkpoints)")
    add_p(
        "To ensure complete academic reliability, ExamOpt implements 5 mandatory test scenarios in `tests/test_scenarios.py`. "
        "All 5 scenarios are verified automatically during every test run:"
    )

    scenario_table = doc.add_table(rows=1, cols=4)
    sc_headers = ["Scenario", "Condition Tested", "Expected Output / Status", "Result"]
    sc_data = [
        ["Test 1", "Standard SRM Sample Dataset (CSE, IT, ECE)", "Conflict-free timetable generated for all subjects (VALID)", "PASS"],
        ["Test 2", "Two exams with shared students in same slot", "Assignment rejected: CONFLICT (Student clash detected)", "PASS"],
        ["Test 3", "54 students placed into a 30-seat classroom", "Assignment rejected: CAPACITY_EXCEEDED (Deficit identified)", "PASS"],
        ["Test 4", "Two exams booked in same room during same slot", "Assignment rejected: DUPLICATE_BOOKING (Room double-booking)", "PASS"],
        ["Test 5", "Exam assigned to room under repair or faculty on leave", "Assignment rejected: ROOM_UNAVAILABLE / FACULTY_UNAVAILABLE", "PASS"]
    ]
    style_table(scenario_table, [1.0, 2.3, 2.4, 0.8], sc_headers, sc_data, align_cols={3: WD_ALIGN_PARAGRAPH.CENTER})

    # ==========================================
    # SECTION 7: DEVELOPER ROADMAP
    # ==========================================
    add_h1("7. Intern Developer Roadmap (Upcoming Post-50% Milestones)")
    add_p(
        "Now that the 50% milestone is achieved, here is your project roadmap. These are the specific features and "
        "technologies you will be implementing next:"
    )

    add_bullet(
        "Deconstruct the monolith into a client-server model. Create a dedicated TCP socket server (`exam_server.py`) "
        "listening on port 8080 that receives scheduling requests in JSON format, executes the engine, and returns schedule payloads.",
        bold_prefix="Milestone 7: Socket Client-Server Architecture: "
    )
    add_bullet(
        "Refactor schedule scoring using Python's functional programming primitives (`map`, `filter`, `reduce`, and `itertools`). "
        "Evaluate timetable quality by calculating penalty metrics across pure functional pipelines.",
        bold_prefix="Milestone 8: Functional Programming Pipelines: "
    )
    add_bullet(
        "Utilize Python's `multiprocessing` module (ProcessPoolExecutor) to generate multiple schedule variations concurrently "
        "across all available CPU cores, selecting the timetable with the highest fitness score.",
        bold_prefix="Milestone 9: Multiprocessing & Parallel Search: "
    )
    add_bullet(
        "Use SymPy (symbolic mathematics) to formulate timetable optimization equations, defining formal penalty weight matrices "
        "for soft constraints such as student exam spread and faculty invigilation load balancing.",
        bold_prefix="Milestone 10: Symbolic Mathematical Optimization (SymPy): "
    )
    add_bullet(
        "Implement Genetic Algorithms (GA) with chromosome representation, crossover, mutation, and elitism selection "
        "to evolve schedules toward global optima.",
        bold_prefix="Milestone 11: Meta-Heuristic Optimization: "
    )

    # ==========================================
    # SECTION 8: QUICKSTART CHEATSHEET
    # ==========================================
    add_h1("8. Intern Developer Cheatsheet & Terminal Commands")
    add_p("Keep this handy cheat sheet open while developing:")

    add_bullet("Launch Desktop Graphical Interface: `python main.py`")
    add_bullet("Run Full Pipeline CLI Demonstration: `python main.py --cli`")
    add_bullet("Run 5 Review Verification Scenarios: `python main.py --scenarios`")
    add_bullet("Run Complete Unit Test Suite (24 tests): `python -m unittest discover tests -v`")
    add_bullet("Reset SQLite Database: Delete `examopt.db` or click 'Reset Database' in GUI Hamburger Menu.")

    add_callout(
        doc,
        title="Golden Rule for Interns",
        text="Before committing any code changes or modifying `scheduling/` or `validation/`, always run "
             "`python -m unittest discover tests -v`. If all 24 tests pass, your changes have satisfied every "
             "academic regulation. If any test fails, use the descriptive test assertion message to debug immediately!",
        layman_text="Never ship a rocket without testing the booster engines first. The 24 automated tests are your flight safety checklist!"
    )

    output_path = os.path.abspath("c:/code/1COLLEGE/APP ExamOPS/ExamOpt_Intern_Technical_Manual.docx")
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    build_document()
