"""
Subject Management View Component
Allows full CRUD operations on Academic Subjects and Exam Requirements.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING
from models.subject import Subject

if TYPE_CHECKING:
    from services.exam_service import ExamService


class SubjectView(ttk.Frame):
    """Tab for managing examination subjects."""

    def __init__(self, parent, service: "ExamService", on_data_changed=None):
        super().__init__(parent)
        self.service = service
        self.on_data_changed = on_data_changed
        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form Panel
        form_frame = ttk.LabelFrame(paned, text="Subject Details")
        paned.add(form_frame, weight=1)

        ttk.Label(form_frame, text="Subject Code / ID:").grid(row=0, column=0, sticky=tk.W, padx=8, pady=5)
        self.id_entry = ttk.Entry(form_frame, width=20)
        self.id_entry.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Subject Title:").grid(row=1, column=0, sticky=tk.W, padx=8, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=20)
        self.name_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Department:").grid(row=2, column=0, sticky=tk.W, padx=8, pady=5)
        self.dept_entry = ttk.Entry(form_frame, width=20)
        self.dept_entry.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Semester:").grid(row=3, column=0, sticky=tk.W, padx=8, pady=5)
        self.sem_entry = ttk.Spinbox(form_frame, from_=1, to=10, width=5)
        self.sem_entry.set(1)
        self.sem_entry.grid(row=3, column=1, sticky=tk.W, padx=8, pady=5)

        ttk.Label(form_frame, text="Duration (minutes):").grid(row=4, column=0, sticky=tk.W, padx=8, pady=5)
        self.dur_entry = ttk.Spinbox(form_frame, from_=30, to=300, increment=30, width=8)
        self.dur_entry.set(180)
        self.dur_entry.grid(row=4, column=1, sticky=tk.W, padx=8, pady=5)

        btn_box = ttk.Frame(form_frame)
        btn_box.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(btn_box, text="➕ Add", command=self.add_subject).grid(row=0, column=0, padx=4)
        ttk.Button(btn_box, text="✏️ Update", command=self.update_subject).grid(row=0, column=1, padx=4)
        ttk.Button(btn_box, text="🗑️ Delete", command=self.delete_subject).grid(row=0, column=2, padx=4)
        ttk.Button(btn_box, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=4)

        form_frame.columnconfigure(1, weight=1)

        # Table Panel
        table_frame = ttk.LabelFrame(paned, text="Academic Subjects")
        paned.add(table_frame, weight=3)

        cols = ("id", "name", "dept", "sem", "duration", "enrolled_count")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="Subject Code")
        self.tree.heading("name", text="Title")
        self.tree.heading("dept", text="Department")
        self.tree.heading("sem", text="Sem")
        self.tree.heading("duration", text="Duration")
        self.tree.heading("enrolled_count", text="Enrolled Students")

        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("name", width=200, anchor=tk.W)
        self.tree.column("dept", width=140, anchor=tk.W)
        self.tree.column("sem", width=50, anchor=tk.CENTER)
        self.tree.column("duration", width=80, anchor=tk.CENTER)
        self.tree.column("enrolled_count", width=120, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_row_selected)

    def _on_row_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        vals = self.tree.item(selected[0], "values")
        self.clear_form()
        self.id_entry.insert(0, vals[0])
        self.name_entry.insert(0, vals[1])
        self.dept_entry.insert(0, vals[2])
        self.sem_entry.set(vals[3])
        dur = vals[4].replace(" mins", "")
        self.dur_entry.set(dur)

    def clear_form(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dept_entry.delete(0, tk.END)
        self.sem_entry.set(1)
        self.dur_entry.set(180)

    def add_subject(self):
        s_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        try:
            sem = int(self.sem_entry.get())
            dur = int(self.dur_entry.get())
        except ValueError:
            sem, dur = 1, 180

        if not s_id or not name or not dept:
            messagebox.showwarning("Validation Warning", "Subject Code, Title, and Department are required.")
            return

        sub = Subject(s_id, name, dept, sem, dur)
        try:
            self.service.add_subject(sub)
            self.refresh()
            self.clear_form()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add subject:\n{e}")

    def update_subject(self):
        s_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        try:
            sem = int(self.sem_entry.get())
            dur = int(self.dur_entry.get())
        except ValueError:
            sem, dur = 1, 180

        if not s_id or not name or not dept:
            messagebox.showwarning("Validation Warning", "Select a subject to update.")
            return

        sub = Subject(s_id, name, dept, sem, dur)
        try:
            self.service.update_subject(sub)
            self.refresh()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update subject:\n{e}")

    def delete_subject(self):
        s_id = self.id_entry.get().strip()
        if not s_id:
            messagebox.showwarning("Warning", "Select a subject to delete.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete subject {s_id}?"):
            try:
                self.service.delete_subject(s_id)
                self.refresh()
                self.clear_form()
                if self.on_data_changed:
                    self.on_data_changed()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete subject:\n{e}")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        subjects = self.service.get_subjects()
        students_map = self.service.get_students_by_subject_map()

        for sub in subjects:
            count = len(students_map.get(sub.subject_id, []))
            self.tree.insert(
                "",
                tk.END,
                values=(
                    sub.subject_id,
                    sub.name,
                    sub.department,
                    sub.semester,
                    f"{sub.duration_minutes} mins",
                    count,
                ),
            )
