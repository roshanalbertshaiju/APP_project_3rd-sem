"""
Room Management View Component
Allows full CRUD operations on Examination Halls, Capacity, and Maintenance Status.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING
from models.room import Room

if TYPE_CHECKING:
    from services.exam_service import ExamService


class RoomView(ttk.Frame):
    """Tab for managing exam rooms, capacity limits, and availability."""

    def __init__(self, parent, service: "ExamService", on_data_changed=None):
        super().__init__(parent)
        self.service = service
        self.on_data_changed = on_data_changed
        self._build_ui()

    def _build_ui(self):
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form Panel
        form_frame = ttk.LabelFrame(paned, text="Room / Hall Details")
        paned.add(form_frame, weight=1)

        ttk.Label(form_frame, text="Room ID:").grid(row=0, column=0, sticky=tk.W, padx=8, pady=5)
        self.id_entry = ttk.Entry(form_frame, width=20)
        self.id_entry.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Room / Hall Name:").grid(row=1, column=0, sticky=tk.W, padx=8, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=20)
        self.name_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=5)

        ttk.Label(form_frame, text="Seating Capacity:").grid(row=2, column=0, sticky=tk.W, padx=8, pady=5)
        self.cap_entry = ttk.Spinbox(form_frame, from_=5, to=500, increment=5, width=8)
        self.cap_entry.set(50)
        self.cap_entry.grid(row=2, column=1, sticky=tk.W, padx=8, pady=5)

        self.avail_var = tk.BooleanVar(value=True)
        self.avail_check = ttk.Checkbutton(form_frame, text="Available for Examination", variable=self.avail_var)
        self.avail_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=8, pady=10)

        btn_box = ttk.Frame(form_frame)
        btn_box.grid(row=4, column=0, columnspan=2, pady=15)

        ttk.Button(btn_box, text="➕ Add", command=self.add_room).grid(row=0, column=0, padx=4)
        ttk.Button(btn_box, text="✏️ Update", command=self.update_room).grid(row=0, column=1, padx=4)
        ttk.Button(btn_box, text="🗑️ Delete", command=self.delete_room).grid(row=0, column=2, padx=4)
        ttk.Button(btn_box, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=4)

        form_frame.columnconfigure(1, weight=1)

        # Table Panel
        table_frame = ttk.LabelFrame(paned, text="Examination Halls & Capacity")
        paned.add(table_frame, weight=3)

        cols = ("id", "name", "capacity", "availability")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="Room ID")
        self.tree.heading("name", text="Room / Hall Name")
        self.tree.heading("capacity", text="Max Capacity")
        self.tree.heading("availability", text="Status")

        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("name", width=220, anchor=tk.W)
        self.tree.column("capacity", width=100, anchor=tk.CENTER)
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
        self.name_entry.insert(0, vals[1])
        self.cap_entry.set(vals[2])
        self.avail_var.set(vals[3] == "Available")

    def clear_form(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.cap_entry.set(50)
        self.avail_var.set(True)

    def add_room(self):
        r_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        try:
            cap = int(self.cap_entry.get())
        except ValueError:
            cap = 50
        avail = self.avail_var.get()

        if not r_id or not name:
            messagebox.showwarning("Validation Warning", "Room ID and Name are required.")
            return

        room = Room(r_id, name, cap, is_available=avail)
        try:
            self.service.add_room(room)
            self.refresh()
            self.clear_form()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add room:\n{e}")

    def update_room(self):
        r_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        try:
            cap = int(self.cap_entry.get())
        except ValueError:
            cap = 50
        avail = self.avail_var.get()

        if not r_id or not name:
            messagebox.showwarning("Validation Warning", "Select a room to update.")
            return

        room = Room(r_id, name, cap, is_available=avail)
        try:
            self.service.update_room(room)
            self.refresh()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update room:\n{e}")

    def delete_room(self):
        r_id = self.id_entry.get().strip()
        if not r_id:
            messagebox.showwarning("Warning", "Select a room to delete.")
            return
        if messagebox.askyesno("Confirm Delete", f"Delete room {r_id}?"):
            try:
                self.service.delete_room(r_id)
                self.refresh()
                self.clear_form()
                if self.on_data_changed:
                    self.on_data_changed()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete room:\n{e}")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rooms = self.service.get_rooms()
        for r in rooms:
            status_text = "Available" if r.is_available else "Unavailable"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    r.room_id,
                    r.name,
                    r.capacity,
                    status_text,
                ),
            )
