"""
Time Slot Management View Component
Allows full CRUD operations on Examination Sessions and Time Periods.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING
from models.timeslot import TimeSlot
from utils.helpers import validate_date_format, validate_time_format

if TYPE_CHECKING:
    from services.exam_service import ExamService


class TimeSlotView(ttk.Frame):
    """Tab for managing examination time slots and scheduling windows."""

    def __init__(self, parent, service: "ExamService", on_data_changed=None):
        super().__init__(parent)
        self.service = service
        self.on_data_changed = on_data_changed
        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form Panel
        form_frame = ttk.LabelFrame(paned, text="Time Slot Details")
        paned.add(form_frame, weight=1)

        ttk.Label(form_frame, text="Slot ID:").grid(row=0, column=0, sticky=tk.W, padx=8, pady=5)
        self.id_entry = ttk.Entry(form_frame, width=20)
        self.id_entry.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Exam Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=8, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Start Time (HH:MM 24h):").grid(row=2, column=0, sticky=tk.W, padx=8, pady=5)
        self.start_entry = ttk.Entry(form_frame, width=20)
        self.start_entry.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="End Time (HH:MM 24h):").grid(row=3, column=0, sticky=tk.W, padx=8, pady=5)
        self.end_entry = ttk.Entry(form_frame, width=20)
        self.end_entry.grid(row=3, column=1, sticky=tk.EW, padx=8, pady=5)

        self.avail_var = tk.BooleanVar(value=True)
        self.avail_check = ttk.Checkbutton(form_frame, text="Slot Available for Booking", variable=self.avail_var)
        self.avail_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=8, pady=10)

        btn_box = ttk.Frame(form_frame)
        btn_box.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(btn_box, text="➕ Add", command=self.add_slot).grid(row=0, column=0, padx=4)
        ttk.Button(btn_box, text="✏️ Update", command=self.update_slot).grid(row=0, column=1, padx=4)
        ttk.Button(btn_box, text="🗑️ Delete", command=self.delete_slot).grid(row=0, column=2, padx=4)
        ttk.Button(btn_box, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=4)

        form_frame.columnconfigure(1, weight=1)

        # Table Panel
        table_frame = ttk.LabelFrame(paned, text="Scheduled Time Windows")
        paned.add(table_frame, weight=3)

        cols = ("id", "date", "start", "end", "availability")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="Slot ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("start", text="Start Time")
        self.tree.heading("end", text="End Time")
        self.tree.heading("availability", text="Status")

        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("date", width=120, anchor=tk.CENTER)
        self.tree.column("start", width=100, anchor=tk.CENTER)
        self.tree.column("end", width=100, anchor=tk.CENTER)
        self.tree.column("availability", width=120, anchor=tk.CENTER)

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
        self.date_entry.insert(0, vals[1])
        self.start_entry.insert(0, vals[2])
        self.end_entry.insert(0, vals[3])
        self.avail_var.set(vals[4] == "Available")

    def clear_form(self):
        self.id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.avail_var.set(True)

    def add_slot(self):
        s_id = self.id_entry.get().strip()
        date_val = self.date_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        avail = self.avail_var.get()

        if not s_id or not date_val or not start or not end:
            messagebox.showwarning("Validation Warning", "All fields are required.")
            return

        if not validate_date_format(date_val):
            messagebox.showerror("Format Error", "Date must be in YYYY-MM-DD format (e.g. 2026-10-10).")
            return

        if not validate_time_format(start) or not validate_time_format(end):
            messagebox.showerror("Format Error", "Times must be in HH:MM format (24-hour, e.g. 09:30).")
            return

        slot = TimeSlot(s_id, date_val, start, end, is_available=avail)
        try:
            self.service.add_timeslot(slot)
            self.refresh()
            self.clear_form()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add time slot:\n{e}")

    def update_slot(self):
        s_id = self.id_entry.get().strip()
        date_val = self.date_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        avail = self.avail_var.get()

        if not s_id or not date_val or not start or not end:
            messagebox.showwarning("Validation Warning", "Select a time slot to update.")
            return

        if not validate_date_format(date_val):
            messagebox.showerror("Format Error", "Date must be in YYYY-MM-DD format.")
            return

        if not validate_time_format(start) or not validate_time_format(end):
            messagebox.showerror("Format Error", "Times must be in HH:MM format (24-hour).")
            return

        slot = TimeSlot(s_id, date_val, start, end, is_available=avail)
        try:
            self.service.update_timeslot(slot)
            self.refresh()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update time slot:\n{e}")

    def delete_slot(self):
        s_id = self.id_entry.get().strip()
        if not s_id:
            messagebox.showwarning("Warning", "Select a time slot to delete.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete time slot {s_id}?"):
            try:
                self.service.delete_timeslot(s_id)
                self.refresh()
                self.clear_form()
                if self.on_data_changed:
                    self.on_data_changed()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete time slot:\n{e}")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        slots = self.service.get_timeslots()
        for s in slots:
            status_text = "Available" if s.is_available else "Unavailable"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    s.slot_id,
                    s.date,
                    s.start_time,
                    s.end_time,
                    status_text,
                ),
            )
