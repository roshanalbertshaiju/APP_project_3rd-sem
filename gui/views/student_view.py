"""
Student Management View Component
Allows full CRUD operations on Students and Course Enrollments.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING
from models.student import Student

if TYPE_CHECKING:
    from services.exam_service import ExamService


class StudentView(ttk.Frame):
    """Tab for managing students and their subject enrollments."""

    def __init__(self, parent, service: "ExamService", on_data_changed=None):
        super().__init__(parent)
        self.service = service
        self.on_data_changed = on_data_changed
        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Panel: Student Form
        form_frame = ttk.LabelFrame(paned, text="Student Details")
        paned.add(form_frame, weight=1)

        ttk.Label(form_frame, text="Register / Student ID:").grid(row=0, column=0, sticky=tk.W, padx=8, pady=5)
        self.id_entry = ttk.Entry(form_frame, width=24)
        self.id_entry.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Student Name:").grid(row=1, column=0, sticky=tk.W, padx=8, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=24)
        self.name_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Department:").grid(row=2, column=0, sticky=tk.W, padx=8, pady=5)
        self.dept_entry = ttk.Entry(form_frame, width=24)
        self.dept_entry.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Semester:").grid(row=3, column=0, sticky=tk.W, padx=8, pady=5)
        self.sem_entry = ttk.Spinbox(form_frame, from_=1, to=10, width=5)
        self.sem_entry.set(1)
        self.sem_entry.grid(row=3, column=1, sticky=tk.W, padx=8, pady=5)

        ttk.Label(form_frame, text="Enrolled Subjects (comma-separated):").grid(
            row=4, column=0, columnspan=2, sticky=tk.W, padx=8, pady=(10, 2)
        )
        self.subs_entry = ttk.Entry(form_frame, width=30)
        self.subs_entry.grid(row=5, column=0, columnspan=2, sticky=tk.EW, padx=8, pady=5)

        btn_box = ttk.Frame(form_frame)
        btn_box.grid(row=6, column=0, columnspan=2, pady=15)

        ttk.Button(btn_box, text="➕ Add", command=self.add_student).grid(row=0, column=0, padx=4)
        ttk.Button(btn_box, text="✏️ Update", command=self.update_student).grid(row=0, column=1, padx=4)
        ttk.Button(btn_box, text="🗑️ Delete", command=self.delete_student).grid(row=0, column=2, padx=4)
        ttk.Button(btn_box, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=4)

        form_frame.columnconfigure(1, weight=1)

        # Right Panel: Student Table
        table_frame = ttk.LabelFrame(paned, text="Enrolled Students")
        paned.add(table_frame, weight=3)

        cols = ("id", "name", "dept", "sem", "enrolled_subjects")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="Student ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("dept", text="Department")
        self.tree.heading("sem", text="Sem")
        self.tree.heading("enrolled_subjects", text="Enrolled Subjects")

        self.tree.column("id", width=120, anchor=tk.CENTER)
        self.tree.column("name", width=150, anchor=tk.W)
        self.tree.column("dept", width=120, anchor=tk.W)
        self.tree.column("sem", width=50, anchor=tk.CENTER)
        self.tree.column("enrolled_subjects", width=220, anchor=tk.W)

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
        self.subs_entry.insert(0, vals[4])

    def clear_form(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dept_entry.delete(0, tk.END)
        self.sem_entry.set(1)
        self.subs_entry.delete(0, tk.END)

    def add_student(self):
        s_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        try:
            sem = int(self.sem_entry.get())
        except ValueError:
            sem = 1
        subs_raw = self.subs_entry.get().strip()
        subs = [s.strip() for s in subs_raw.split(",") if s.strip()]

        if not s_id or not name or not dept:
            messagebox.showwarning("Validation Warning", "Student ID, Name, and Department are required.")
            return

        stu = Student(s_id, name, dept, sem, subs)
        try:
            self.service.add_student(stu)
            self.refresh()
            self.clear_form()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student:\n{e}")

    def update_student(self):
        s_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        try:
            sem = int(self.sem_entry.get())
        except ValueError:
            sem = 1
        subs_raw = self.subs_entry.get().strip()
        subs = [s.strip() for s in subs_raw.split(",") if s.strip()]

        if not s_id or not name or not dept:
            messagebox.showwarning("Validation Warning", "Select a student to update.")
            return

        stu = Student(s_id, name, dept, sem, subs)
        try:
            self.service.update_student(stu)
            self.refresh()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student:\n{e}")

    def delete_student(self):
        s_id = self.id_entry.get().strip()
        if not s_id:
            messagebox.showwarning("Warning", "Select a student to delete.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete student {s_id}?"):
            try:
                self.service.delete_student(s_id)
                self.refresh()
                self.clear_form()
                if self.on_data_changed:
                    self.on_data_changed()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student:\n{e}")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        students = self.service.get_students()
        for stu in students:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    stu.student_id,
                    stu.name,
                    stu.department,
                    stu.semester,
                    ", ".join(stu.enrolled_subject_ids),
                ),
            )
