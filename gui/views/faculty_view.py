"""
Faculty Management View Component
Allows full CRUD operations on Invigilator / Faculty Records and Availability.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING
from models.faculty import Faculty

if TYPE_CHECKING:
    from services.exam_service import ExamService


class FacultyView(ttk.Frame):
    """Tab for managing faculty and invigilator availability."""

    def __init__(self, parent, service: "ExamService", on_data_changed=None):
        super().__init__(parent)
        self.service = service
        self.on_data_changed = on_data_changed
        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form Panel
        form_frame = ttk.LabelFrame(paned, text="Faculty Member Details")
        paned.add(form_frame, weight=1)

        ttk.Label(form_frame, text="Faculty ID:").grid(row=0, column=0, sticky=tk.W, padx=8, pady=5)
        self.id_entry = ttk.Entry(form_frame, width=20)
        self.id_entry.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Faculty Name:").grid(row=1, column=0, sticky=tk.W, padx=8, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=20)
        self.name_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Department:").grid(row=2, column=0, sticky=tk.W, padx=8, pady=5)
        self.dept_entry = ttk.Entry(form_frame, width=20)
        self.dept_entry.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=5)

        self.avail_var = tk.BooleanVar(value=True)
        self.avail_check = ttk.Checkbutton(form_frame, text="Available for Invigilation", variable=self.avail_var)
        self.avail_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=8, pady=10)

        btn_box = ttk.Frame(form_frame)
        btn_box.grid(row=4, column=0, columnspan=2, pady=15)

        ttk.Button(btn_box, text="➕ Add", command=self.add_faculty).grid(row=0, column=0, padx=4)
        ttk.Button(btn_box, text="✏️ Update", command=self.update_faculty).grid(row=0, column=1, padx=4)
        ttk.Button(btn_box, text="🗑️ Delete", command=self.delete_faculty).grid(row=0, column=2, padx=4)
        ttk.Button(btn_box, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=4)

        form_frame.columnconfigure(1, weight=1)

        # Table Panel
        table_frame = ttk.LabelFrame(paned, text="Faculty & Invigilators List")
        paned.add(table_frame, weight=3)

        cols = ("id", "name", "dept", "availability")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="Faculty ID")
        self.tree.heading("name", text="Faculty Name")
        self.tree.heading("dept", text="Department")
        self.tree.heading("availability", text="Availability Status")

        self.tree.column("id", width=110, anchor=tk.CENTER)
        self.tree.column("name", width=200, anchor=tk.W)
        self.tree.column("dept", width=160, anchor=tk.W)
        self.tree.column("availability", width=140, anchor=tk.CENTER)

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
        self.avail_var.set(vals[3] == "Available")

    def clear_form(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dept_entry.delete(0, tk.END)
        self.avail_var.set(True)

    def add_faculty(self):
        f_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        avail = self.avail_var.get()

        if not f_id or not name or not dept:
            messagebox.showwarning("Validation Warning", "Faculty ID, Name, and Department are required.")
            return

        fac = Faculty(f_id, name, dept, is_available=avail)
        try:
            self.service.add_faculty(fac)
            self.refresh()
            self.clear_form()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add faculty:\n{e}")

    def update_faculty(self):
        f_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        avail = self.avail_var.get()

        if not f_id or not name or not dept:
            messagebox.showwarning("Validation Warning", "Select a faculty member to update.")
            return

        fac = Faculty(f_id, name, dept, is_available=avail)
        try:
            self.service.update_faculty(fac)
            self.refresh()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update faculty:\n{e}")

    def delete_faculty(self):
        f_id = self.id_entry.get().strip()
        if not f_id:
            messagebox.showwarning("Warning", "Select a faculty member to delete.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete faculty {f_id}?"):
            try:
                self.service.delete_faculty(f_id)
                self.refresh()
                self.clear_form()
                if self.on_data_changed:
                    self.on_data_changed()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete faculty:\n{e}")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        faculty_list = self.service.get_faculty()
        for fac in faculty_list:
            status_text = "Available" if fac.is_available else "Unavailable"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    fac.faculty_id,
                    fac.name,
                    fac.department,
                    status_text,
                ),
            )
