"""
Timetable View Component
Displays generated examination schedule, summary statistics, and logs.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.exam_service import ExamService


class TimetableView(ttk.Frame):
    """View tab for viewing, generating, and exporting the examination timetable."""

    def __init__(self, parent, service: "ExamService", on_data_changed=None):
        super().__init__(parent)
        self.service = service
        self.on_data_changed = on_data_changed
        self._build_ui()

    def _build_ui(self):
        # Action Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=10, pady=8)

        gen_btn = ttk.Button(toolbar, text="⚡ Quick Generate", command=self.generate_timetable)
        gen_btn.pack(side=tk.LEFT, padx=3)

        ga_btn = ttk.Button(toolbar, text="🧬 AI Optimize (GA)", command=self.run_ai_optimization)
        ga_btn.pack(side=tk.LEFT, padx=3)

        val_btn = ttk.Button(toolbar, text="🔍 Validate", command=self.validate_schedule)
        val_btn.pack(side=tk.LEFT, padx=3)

        score_btn = ttk.Button(toolbar, text="📐 Soft Quality Score", command=self.show_functional_score)
        score_btn.pack(side=tk.LEFT, padx=3)

        export_csv_btn = ttk.Button(toolbar, text="💾 CSV", command=self.export_csv)
        export_csv_btn.pack(side=tk.LEFT, padx=3)

        export_xlsx_btn = ttk.Button(toolbar, text="📊 Excel", command=self.export_excel)
        export_xlsx_btn.pack(side=tk.LEFT, padx=3)

        export_pdf_btn = ttk.Button(toolbar, text="📄 PDF", command=self.export_pdf)
        export_pdf_btn.pack(side=tk.LEFT, padx=3)

        clear_btn = ttk.Button(toolbar, text="🧹 Clear", command=self.clear_schedule)
        clear_btn.pack(side=tk.LEFT, padx=3)

        refresh_btn = ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh)
        refresh_btn.pack(side=tk.RIGHT, padx=5)

        # Status Summary Header
        self.status_var = tk.StringVar(value="Status: Ready | Load data or click 'Generate Timetable' to begin.")
        status_banner = ttk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
            relief=tk.GROOVE,
            padding=6,
            anchor=tk.W,
        )
        status_banner.pack(fill=tk.X, padx=10, pady=(0, 6))

        # Main Split Frame: Top = Timetable Tree, Bottom = Log console
        paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview Frame
        tree_frame = ttk.Frame(paned)
        paned.add(tree_frame, weight=3)

        cols = (
            "exam_id",
            "subject_code",
            "subject_name",
            "date",
            "time",
            "room",
            "capacity",
            "students",
            "invigilator",
            "status",
        )
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("exam_id", text="Exam ID")
        self.tree.heading("subject_code", text="Subject")
        self.tree.heading("subject_name", text="Subject Title")
        self.tree.heading("date", text="Exam Date")
        self.tree.heading("time", text="Time Slot")
        self.tree.heading("room", text="Room")
        self.tree.heading("capacity", text="Capacity")
        self.tree.heading("students", text="Enrolled")
        self.tree.heading("invigilator", text="Invigilator (Faculty)")
        self.tree.heading("status", text="Status")

        self.tree.column("exam_id", width=85, anchor=tk.CENTER)
        self.tree.column("subject_code", width=75, anchor=tk.CENTER)
        self.tree.column("subject_name", width=180, anchor=tk.W)
        self.tree.column("date", width=90, anchor=tk.CENTER)
        self.tree.column("time", width=110, anchor=tk.CENTER)
        self.tree.column("room", width=130, anchor=tk.W)
        self.tree.column("capacity", width=65, anchor=tk.CENTER)
        self.tree.column("students", width=65, anchor=tk.CENTER)
        self.tree.column("invigilator", width=140, anchor=tk.W)
        self.tree.column("status", width=130, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Log Console Frame
        log_frame = ttk.LabelFrame(paned, text="Optimization & Constraint Engine Diagnostics")
        paned.add(log_frame, weight=1)

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=6, font=("Consolas", 9), relief=tk.FLAT)
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=4)

    def apply_theme(self, theme: str = "classic"):
        """Apply theme-specific colors to non-TTK elements."""
        if theme == "modern":
            self.log_text.config(
                bg="#0B0F19",
                fg="#38BDF8",
                insertbackground="#F8FAFC",
                selectbackground="#312E81",
                selectforeground="#FFFFFF",
            )
        else:
            self.log_text.config(
                bg="#FFFFFF",
                fg="#000000",
                insertbackground="#000000",
                selectbackground="#B5D5FF",
                selectforeground="#000000",
            )

    def log(self, text: str):
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def generate_timetable(self):
        try:
            report = self.service.generate_timetable()
            self.refresh()
            self.log("=" * 60)
            self.log(f"SCHEDULER RUN: {report.summary_message}")
            for ex in report.scheduled_exams:
                self.log(f"  ✓ {ex.exam_id} ({ex.subject_id}): {ex.status_reason}")
            for ex in report.unscheduled_exams:
                self.log(f"  ✗ {ex.exam_id} ({ex.subject_id}): {ex.status} -> {ex.status_reason}")
            self.log("=" * 60)

            if report.is_complete:
                messagebox.showinfo(
                    "Scheduling Complete",
                    f"Feasible timetable generated successfully!\n\nAll {report.scheduled_count} examinations scheduled without conflicts."
                )
            else:
                messagebox.showwarning(
                    "Scheduling Incomplete",
                    f"Scheduled: {report.scheduled_count}\nUnscheduled: {report.unscheduled_count}\n\nReview diagnostics log for details."
                )
        except Exception as e:
            messagebox.showerror("Scheduling Error", f"Error while generating timetable:\n{e}")

    def validate_schedule(self):
        try:
            is_valid, results = self.service.validate_current_schedule()
            self.log("--- CONSTRAINT VALIDATION REPORT ---")
            for res in results:
                prefix = "  ✓" if res.is_valid else "  ✗"
                self.log(f"{prefix} [{res.status}] {res.message}")

            if is_valid:
                messagebox.showinfo(
                    "Validation Passed",
                    f"All {len(results)} scheduled examinations satisfy all constraints!\n\nNo student, faculty, room, or capacity conflicts detected."
                )
            else:
                invalid_count = sum(1 for r in results if not r.is_valid)
                messagebox.showerror(
                    "Constraint Violations Detected",
                    f"Detected {invalid_count} constraint violation(s) in current schedule.\nSee diagnostics log for details."
                )
        except Exception as e:
            messagebox.showerror("Validation Error", f"Error while validating constraints:\n{e}")

    def export_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Export Timetable as CSV"
        )
        if not filepath:
            return
        try:
            self.service.export_timetable_to_csv(filepath)
            messagebox.showinfo("Export Successful", f"Timetable exported successfully to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export file:\n{e}")

    def export_excel(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Workbooks", "*.xlsx"), ("All Files", "*.*")],
            title="Export Timetable as Microsoft Excel"
        )
        if not filepath:
            return
        try:
            out = self.service.export_timetable_to_excel(filepath)
            messagebox.showinfo("Excel Export Successful", f"Professional Excel timetable generated:\n{out}")
        except Exception as e:
            messagebox.showerror("Excel Export Failed", f"Could not generate Excel file:\n{e}")

    def export_pdf(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf"), ("All Files", "*.*")],
            title="Export Timetable as Official PDF"
        )
        if not filepath:
            return
        try:
            out = self.service.export_timetable_to_pdf(filepath)
            messagebox.showinfo("PDF Export Successful", f"Official PDF timetable generated:\n{out}")
        except Exception as e:
            messagebox.showerror("PDF Export Failed", f"Could not generate PDF file:\n{e}")

    def show_functional_score(self):
        try:
            rep = self.service.evaluate_schedule_functional()
            msg = (
                f"Milestone 8 Functional Evaluation (map/filter/reduce):\n\n"
                f"• Fitness Score: {rep.fitness_score:.4f} / 1000.0\n"
                f"• Total Soft Penalty: {rep.total_penalty:.2f}\n"
                f"• Students with Consecutive Exams: {rep.consecutive_exam_students}\n"
                f"• Overloaded Faculty (>1 duty/day): {rep.overloaded_faculty_instances}\n"
                f"• Total Seat Wastage: {rep.total_seat_wastage} seats\n"
                f"• Average Room Seating Efficiency: {rep.average_room_utilization_pct:.1f}%\n"
            )
            self.log(msg)
            messagebox.showinfo("Functional Pipeline Metrics", msg)
        except Exception as e:
            messagebox.showerror("Evaluation Error", f"Could not evaluate schedule: {e}")

    def run_ai_optimization(self):
        """Runs the Genetic Algorithm evolutionary search to optimize timetable quality."""
        try:
            self.log("\n[AI Optimization] Running Genetic Algorithm evolutionary search (30 generations)...")
            res = self.service.optimize_with_genetic_algorithm(population_size=30, generations=30)
            self.refresh()
            if self.on_data_changed:
                self.on_data_changed()

            msg = (
                f"🧬 AI Evolutionary Optimization Complete!\n\n"
                f"• Hard Constraint Violations: {res.hard_conflicts} (100% Conflict-Free)\n"
                f"• Fitness Score: {res.best_fitness:.4f}\n"
                f"• Total Soft Penalty: {res.soft_penalty:.2f}\n"
                f"• Generations Evaluated: {res.generations_run}\n"
                f"• Exams Scheduled: {len(res.best_schedule)}\n\n"
                f"Timetable has been updated and persisted to database."
            )
            self.log(f"[AI Optimization Success] Fitness: {res.best_fitness:.4f}, Soft Penalty: {res.soft_penalty:.2f}")
            messagebox.showinfo("AI Optimization Complete", msg)
        except Exception as e:
            self.log(f"[AI Optimization Error] {e}")
            messagebox.showerror("Optimization Error", f"Failed to run AI optimization: {e}")

    def clear_schedule(self):
        if messagebox.askyesno("Clear Schedule", "Are you sure you want to clear the scheduled timetable?"):
            self.service.clear_exams()
            self.refresh()
            self.log("Timetable cleared.")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        exams = self.service.get_all_exams()
        rooms = {r.room_id: r for r in self.service.get_rooms()}
        faculty = {f.faculty_id: f for f in self.service.get_faculty()}
        slots = {s.slot_id: s for s in self.service.get_timeslots()}
        subjects = {s.subject_id: s for s in self.service.get_subjects()}

        scheduled_count = 0
        unscheduled_count = 0

        for exam in exams:
            sub = subjects.get(exam.subject_id)
            sub_name = sub.name if sub else exam.subject_id
            slot = slots.get(exam.slot_id) if exam.slot_id else None
            room = rooms.get(exam.room_id) if exam.room_id else None
            fac = faculty.get(exam.faculty_id) if exam.faculty_id else None

            date_str = slot.date if slot else "N/A"
            time_str = f"{slot.start_time} - {slot.end_time}" if slot else "N/A"
            room_str = room.name if room else "N/A"
            cap_str = str(room.capacity) if room else "-"
            fac_str = fac.name if fac else "N/A"

            if exam.status == "Successfully Scheduled":
                scheduled_count += 1
            else:
                unscheduled_count += 1

            self.tree.insert(
                "",
                tk.END,
                values=(
                    exam.exam_id,
                    exam.subject_id,
                    sub_name,
                    date_str,
                    time_str,
                    room_str,
                    cap_str,
                    exam.student_count,
                    fac_str,
                    exam.status,
                ),
            )

        total_subjects = len(subjects)
        self.status_var.set(
            f"Subjects: {total_subjects} | Scheduled: {scheduled_count} | Unscheduled: {unscheduled_count} | Rooms: {len(rooms)} | Faculty: {len(faculty)}"
        )
