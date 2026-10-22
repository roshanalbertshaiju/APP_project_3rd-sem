"""
Script to generate a professional PowerPoint presentation (.pptx) for ExamOpt
SRM Institute of Science and Technology, Tiruchirappalli
Advanced Programming Practice (APP) - 2nd Year B.Tech CSE Core
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_NAVY = RGBColor(13, 71, 161)      # #0D47A1
    PRIMARY_BLUE = RGBColor(21, 101, 192)   # #1565C0
    ACCENT_CYAN = RGBColor(2, 136, 209)     # #0288D1
    SLATE_DARK = RGBColor(15, 23, 42)       # #0F172A
    SLATE_TEXT = RGBColor(51, 65, 85)       # #334155
    MUTED_TEXT = RGBColor(100, 116, 139)    # #64748B
    CARD_BG = RGBColor(248, 250, 252)       # #F8FAFC
    CARD_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
    WHITE = RGBColor(255, 255, 255)
    EMERALD = RGBColor(16, 185, 129)        # #10B981

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="EXAMOPT — ADVANCED PROGRAMMING PRACTICE (APP)"):
        # Top banner accent line
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        accent.fill.solid()
        accent.fill.fore_color.rgb = PRIMARY_BLUE
        accent.line.fill.background()

        # Category / Subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Segoe UI"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY_BLUE

        # Main Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.7), Inches(0.65))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = SLATE_DARK

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_NAVY
    bg1.line.fill.background()

    # Inner decorative container
    inner1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.9), Inches(11.333), Inches(5.7))
    inner1.fill.solid()
    inner1.fill.fore_color.rgb = RGBColor(18, 80, 175)
    inner1.line.color.rgb = RGBColor(40, 110, 215)
    inner1.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY — TIRUCHIRAPPALLI"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(187, 222, 251)
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "EXAMOPT"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(4)

    p2 = tf1.add_paragraph()
    p2.text = "Intelligent Examination Timetable Scheduling & Optimization System"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(227, 242, 253)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "COURSE: Advanced Programming Practice (APP) | 2nd Year B.Tech CSE (Core)\nMILESTONE: 100% Production Capstone Review (All Milestones 1–12 Complete)\nTEAM: Suhas V A  •  Subaash G  •  Roshan Albert Shaiju"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(12)
    p3.font.color.rgb = WHITE
    p3.line_spacing = 1.3

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Project Motivation", "THE CHALLENGE")

    # Card 1: The Manual Dilemma
    add_card(s2, 0.8, 1.5, 3.6, 5.2)
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📌 The Administrative Nightmare"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• In university operations, exam scheduling is a high-stakes, manual ordeal spanning 2–3 weeks.\n\n• Multiple departments (CSE, IT, ECE) share electives, creating non-trivial student overlaps.\n\n• Classrooms vary widely in capacity (15 to 120 seats), leading to room fragmentation or severe shortages.\n\n• Human error inevitably leads to student exam clashes and double-booked halls."
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.25

    # Card 2: Computational Nature
    add_card(s2, 4.8, 1.5, 3.6, 5.2)
    tb = s2.shapes.add_textbox(Inches(5.0), Inches(1.7), Inches(3.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚙️ NP-Hard Complexity"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Formulated as an Examination Timetabling Problem (ETP), a proven NP-hard Constraint Satisfaction Problem (CSP).\n\n• Search space scales combinatorially: O((T × R × F)^S).\n\n• Brute force search is mathematically impossible for realistic university cohorts (10^20+ states).\n\n• Requires intelligent heuristics and rigorous constraint satisfaction algorithms."
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.25

    # Card 3: The ExamOpt Solution
    add_card(s2, 8.8, 1.5, 3.7, 5.2)
    tb = s2.shapes.add_textbox(Inches(9.0), Inches(1.7), Inches(3.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🚀 The ExamOpt Solution"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Automated, heuristic timetable generation in < 100 milliseconds.\n\n• Guarantees 100% satisfaction of all hard academic constraints.\n\n• Implements Best-Fit room allocation to eliminate empty seat waste.\n\n• Comprehensive Tkinter GUI + CLI + persistent SQLite database.\n\n• Validated through 24 automated tests and 5 academic review checkpoints."
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.25

    # ==========================================
    # SLIDE 3: SYSTEM ARCHITECTURE & DESIGN PATTERNS
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Clean Layered Architecture & Design Patterns", "SYSTEM DESIGN")

    add_card(s3, 0.8, 1.5, 5.7, 5.2)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🏛️ Tiered Clean Architecture"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Presentation Layer (Tkinter Modern Studio / Classic / CLI)\n  │  Calls high-level API methods only\n  ▼\nApplication Service Facade (ExamService)\n  │  Coordinates database, scheduling & validation\n  ├────────────────────────┬────────────────────────┐\n  ▼                        ▼                        ▼\nScheduling Engine    Validation Engine      SQLite Database\n(MRV Heuristic)      (6 Constraint Rules)   (Thread-Safe DAO)\n  │\n  ▼\nRoom Allocator Engine\n(Best-Fit Capacity Matcher)"
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_DARK
    p.line_spacing = 1.15

    add_card(s3, 6.8, 1.5, 5.7, 5.2)
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Software Design Patterns"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(8)

    patterns = [
        ("1. Facade Pattern (services/exam_service.py):", "Single unified gateway hiding SQL, scheduling, and validation complexities from the UI."),
        ("2. DAO / Repository Pattern (database/database.py):", "Encapsulates all SQLite persistence. Swapping database engines requires modifying only this class."),
        ("3. Strategy Pattern (scheduling/room_allocator.py):", "Isolates Best-Fit allocation strategy so alternative policies can be plugged in seamlessly."),
        ("4. Specification Pattern (validation/validator.py):", "Encapsulates academic rules into independent, reusable evaluation methods."),
        ("5. DTO Pattern (models/*.py):", "Pure Python dataclasses (@dataclass) for clean data transfer across layers.")
    ]
    for name, desc in patterns:
        p = tf.add_paragraph()
        p.text = f"{name} {desc}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = SLATE_TEXT
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 4: RELATIONAL DATABASE & DATA INTEGRITY
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Relational Database Design & Data Integrity", "PERSISTENCE LAYER")

    # Left: Database Schema Table
    add_card(s4, 0.8, 1.5, 6.2, 5.2)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.8), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🗄️ Normalized Schema (3NF in SQLite)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• students (student_id PK, name, department, semester)\n• subjects (subject_id PK, name, department, semester, duration)\n• enrollments (student_id FK, subject_id FK) -> Composite PK\n• faculty (faculty_id PK, name, department, is_available)\n• rooms (room_id PK, name, capacity, is_available)\n• timeslots (slot_id PK, date, start_time, end_time, is_available)\n• exams (exam_id PK, subject_id FK, slot_id FK, room_id FK, faculty_id FK, student_count, status, status_reason)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.3

    # Right: Integrity & Performance
    add_card(s4, 7.3, 1.5, 5.2, 5.2)
    tb = s4.shapes.add_textbox(Inches(7.5), Inches(1.7), Inches(4.8), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔒 Integrity & Performance Features"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Foreign Key Enforcement:\n  Explicitly executed 'PRAGMA foreign_keys = ON;'\n\n• Cascading Actions:\n  ON DELETE CASCADE for enrollments;\n  ON DELETE SET NULL for scheduled exam resources.\n\n• Query Optimization (B-Tree Indices):\n  CREATE INDEX idx_enrollments_subject ON enrollments(subject_id);\n  CREATE INDEX idx_exams_slot ON exams(slot_id);\n  Ensures O(1) / O(log N) lookup speeds during validation.\n\n• ACID Transactions & Injection Defense:\n  Managed via 'with conn:' context managers and parameterized queries ('?')."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.25

    # ==========================================
    # SLIDE 5: CONSTRAINT VALIDATION ENGINE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Constraint Validation Engine (6 Hard Checks)", "RULE AUDITING")

    rules = [
        ("1. Input Integrity", "Verifies all required entities exist and foreign IDs are valid.", "INVALID"),
        ("2. Resource Availability", "Confirms timeslot, room, and faculty are marked active (is_available=1).", "ROOM / FACULTY_UNAVAILABLE"),
        ("3. Room Seating Capacity", "Enforces student_count <= room.capacity; computes exact seat deficit.", "CAPACITY_EXCEEDED"),
        ("4. Duplicate Room Booking", "Prevents two exams from occupying the same room during the same timeslot.", "DUPLICATE_BOOKING"),
        ("5. Faculty Clash Prevention", "Ensures an invigilator is never assigned to two rooms at the same time.", "FACULTY_UNAVAILABLE"),
        ("6. Student Collision (Set Theory)", "Set intersection of enrolled cohorts in the same slot must be empty.", "CONFLICT")
    ]

    for i, (title, desc, code) in enumerate(rules):
        row = i // 2
        col = i % 2
        l = 0.8 + col * 5.9
        t = 1.4 + row * 1.8
        add_card(s5, l, t, 5.6, 1.6)
        tb = s5.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.15), Inches(5.2), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BLUE

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_TEXT

        p = tf.add_paragraph()
        p.text = f"Status Code: {code}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(194, 65, 12)

    # ==========================================
    # SLIDE 6: INTELLIGENT SCHEDULING ENGINE
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Intelligent Scheduling Engine (MRV Heuristic)", "OPTIMIZATION ENGINE")

    add_card(s6, 0.8, 1.5, 5.7, 5.2)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💡 Most Constrained Variable (MRV)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• The Fail-First Principle:\n  In CSPs, scheduling the most restrictive variables first drastically prunes the search tree.\n\n• Sort by Enrollment Descending:\n  sorted(subjects, key=lambda s: len(students[s.id]), reverse=True)\n\n• Why It Works:\n  Large cohorts (e.g. 80 students) have very few eligible halls and conflict with the most students. By placing them first, small electives easily slip into the remaining timeslots without forcing backtracking."
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.3

    add_card(s6, 6.8, 1.5, 5.7, 5.2)
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔄 Timetable Generation Pipeline"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Filter Active Resources:\n   Isolate timeslots and faculty where is_available == True.\n\n2. Slot-by-Slot Collision Audit:\n   Check student set overlap: set(A).intersection(set(B)) == 0.\n\n3. Faculty Matching:\n   Identify available, unbooked invigilators for the slot.\n\n4. Best-Fit Room Allocation:\n   Match the tightest capacity hall to prevent seat waste.\n\n5. Defensive Validator Verification:\n   Candidate exam is fully verified before committing to database."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.25

    # ==========================================
    # SLIDE 7: BEST-FIT ROOM ALLOCATION
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Best-Fit Room Allocation (Bin Packing Problem)", "CAPACITY OPTIMIZATION")

    add_card(s7, 0.8, 1.5, 5.7, 5.2)
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📦 The Bin Packing Challenge"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• First-Fit Flaw:\n  First-Fit assigns the first room where Capacity >= Students. If a 15-student class runs first, it might grab the 120-seat Auditorium, leaving a 70-student class stranded later.\n\n• The 'Goldilocks' Principle (Best-Fit):\n  Picks the smallest room that comfortably fits the cohort:\n  min(capacity(r) - student_count) for all r in AvailableRooms.\n\n• Benefits:\n  Eliminates hall capacity fragmentation and preserves large venues for large cohorts."
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.3

    add_card(s7, 6.8, 1.5, 5.7, 5.2)
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💻 Algorithm Implementation"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "def allocate_best_fit_room(student_count, slot_id, rooms, schedule):\n    # 1. Unbooked rooms in slot\n    available = get_available_rooms_for_slot(slot_id, rooms, schedule)\n\n    # 2. Filter sufficient capacity\n    suitable = [r for r in available if r.capacity >= student_count]\n    if not suitable:\n        return None, 'CAPACITY_EXCEEDED'\n\n    # 3. Best-Fit: Sort ascending by capacity\n    suitable.sort(key=lambda r: (r.capacity, r.name))\n    return suitable[0], 'OK'"
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_DARK
    p.line_spacing = 1.2

    # ==========================================
    # SLIDE 8: USER INTERFACE (DUAL THEME)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "User Interface Design: Modern Studio & Classic UI", "PRESENTATION LAYER")

    # Left: Modern Minimalist Studio
    add_card(s8, 0.8, 1.5, 5.7, 5.2)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎨 Modern Minimalist Studio (gui/modern_app.py)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Obsidian Dark Palette:\n  Engineered with deep obsidian (#0B0F19) and slate surfaces (#0F172A) with electric indigo accents (#6366F1).\n\n• Responsive Sidebar Navigation:\n  Clean left sidebar with active indicator strips, replacing traditional top tabs.\n\n• Live Status Header:\n  Features glowing status metrics and instant one-click actions (Generate, Validate, Export CSV).\n\n• High-Contrast Typography:\n  Spacious Segoe UI fonts and modern TTK styling."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.25

    # Right: Classic Theme & Capabilities
    add_card(s8, 6.8, 1.5, 5.7, 5.2)
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🖥️ Features & Entity Management"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Classic University Theme (gui/app.py):\n  Original institutional navy banner with notebook tabs for traditional environments.\n\n• Full CRUD Dialogues:\n  Dedicated views for Students, Subjects, Faculty, Rooms, and TimeSlots with search filtering.\n\n• Live Diagnostics Tab:\n  Verification view executing the 5 review scenarios interactively with visual pass/fail badges.\n\n• CSV Exporter:\n  Generates administrative reports with complete exam metadata."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_TEXT
    p.line_spacing = 1.25

    # ==========================================
    # SLIDE 9: 50% REVIEW CHECKPOINTS & TESTING
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Milestone 6 Review Scenarios & Test Suite", "ACADEMIC CHECKPOINTS")

    # Table of 5 Scenarios
    table_shape = s9.shapes.add_table(rows=6, cols=4, left=Inches(0.8), top=Inches(1.5), width=Inches(11.733), height=Inches(3.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.5)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(4.3)
    table.columns[3].width = Inches(1.433)

    sc_headers = ["Scenario", "Condition Tested", "Expected Output / Status", "Status"]
    for i, h in enumerate(sc_headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = WHITE

    sc_data = [
        ("Test 1", "Standard SRM Sample Dataset (CSE, IT, ECE)", "Conflict-free timetable generated for all subjects (VALID)", "PASS"),
        ("Test 2", "Two exams with shared students in same slot", "Assignment rejected: CONFLICT (Student clash detected)", "PASS"),
        ("Test 3", "54 students placed into a 30-seat classroom", "Assignment rejected: CAPACITY_EXCEEDED (Deficit flagged)", "PASS"),
        ("Test 4", "Two exams booked in same room during same slot", "Assignment rejected: DUPLICATE_BOOKING (Room double-booking)", "PASS"),
        ("Test 5", "Exam assigned to room under repair or faculty on leave", "Assignment rejected: ROOM_UNAVAILABLE / FACULTY_UNAVAILABLE", "PASS"),
    ]

    for r_idx, (sc, cond, exp, res) in enumerate(sc_data, start=1):
        row_cells = [table.cell(r_idx, 0), table.cell(r_idx, 1), table.cell(r_idx, 2), table.cell(r_idx, 3)]
        row_cells[0].text = sc
        row_cells[1].text = cond
        row_cells[2].text = exp
        row_cells[3].text = res

        bg = RGBColor(241, 245, 249) if r_idx % 2 == 1 else WHITE
        for c_idx, cell in enumerate(row_cells):
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            for p in cell.text_frame.paragraphs:
                p.font.name = "Segoe UI"
                p.font.size = Pt(9.5)
                if c_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = EMERALD
                    p.alignment = PP_ALIGN.CENTER
                else:
                    p.font.color.rgb = SLATE_TEXT

    # Bottom metric badge
    add_card(s9, 0.8, 5.6, 11.733, 1.1)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(0.9))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "🧪 Complete Verification Suite: 24 Automated Unit Tests Passing (0.010s Execution Time)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p = tf.add_paragraph()
    p.text = "Includes 6 CRUD tests (test_crud.py), 8 validator tests (test_validator.py), 5 scheduler tests (test_scheduler.py), and 5 scenario tests (test_scenarios.py). Uses in-memory SQLite (:memory:) for isolated, clean execution."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 10: ADVANCED CAPSTONE ARCHITECTURE (MILESTONES 7-12)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Advanced Capstone Modules (Milestones 7–12 Realized)", "100% IMPLEMENTATION")

    milestones = [
        ("Milestone 7: Distributed TCP Socket Server", "Standalone daemon (exam_server.py) with length-prefixed JSON RPC framing and concurrent multi-client handling."),
        ("Milestone 8: Functional Programming Pipelines", "Pure functional evaluation via map(), filter(), functools.reduce() computing soft penalties without side-effects."),
        ("Milestone 9: Multiprocessing Engine (GIL Bypassed)", "Circumvents CPython's GIL across CPU cores with ProcessPoolExecutor, evaluating candidate schedules in parallel."),
        ("Milestone 10: SymPy Symbolic Mathematical Modeling", "Formal objective loss Z = w^T P with analytical sensitivity analysis and partial gradient calculation."),
        ("Milestones 11 & 12: Genetic Algorithm & Multi-Format Exports", "Evolutionary chromosome optimization with elitism, official PDF reports, styled Excel workbooks, and 53 automated unit tests.")
    ]

    for i, (title, desc) in enumerate(milestones):
        t = 1.5 + i * 1.05
        add_card(s10, 0.8, t, 11.733, 0.95)
        tb = s10.shapes.add_textbox(Inches(1.0), Inches(t + 0.1), Inches(11.3), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BLUE

        p = tf.add_paragraph()
        p.text = desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 11: CONCLUSION & Q&A
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    bg11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg11.fill.solid()
    bg11.fill.fore_color.rgb = DARK_NAVY
    bg11.line.fill.background()

    inner11 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    inner11.fill.solid()
    inner11.fill.fore_color.rgb = RGBColor(18, 80, 175)
    inner11.line.color.rgb = RGBColor(40, 110, 215)

    tb11 = s11.shapes.add_textbox(Inches(2.0), Inches(1.8), Inches(9.333), Inches(4.0))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    p = tf11.paragraphs[0]
    p.text = "ExamOpt Summary & Key Takeaways"
    p.font.name = "Segoe UI"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(16)

    p = tf11.add_paragraph()
    p.text = "✓ 100% Production Capstone Target Fully Realized & Mathematically Verified\n✓ Clean Tiered Architecture with Facade, DAO, Strategy & Specification Patterns\n✓ 100% Conflict-Free Timetable Generation in Sub-100ms Execution\n✓ Meta-Heuristic Genetic Algorithm Minimizes Student Stress & Hall Wastage\n✓ Multi-Core Parallel Computing (ProcessPoolExecutor) Bypassing the Python GIL\n✓ Distributed TCP Socket Daemon & Client Architecture with Length-Prefixed JSON\n✓ 53 Automated Unit Tests & 10 Capstone Academic Review Scenarios Verified (100% PASS)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(227, 242, 253)
    p.line_spacing = 1.3
    p.space_after = Pt(16)

    p = tf11.add_paragraph()
    p.text = "Thank You! Questions & Answers"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(187, 222, 251)

    # Save presentation
    output_path = os.path.abspath("c:/code/1COLLEGE/APP ExamOPS/ExamOpt_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
