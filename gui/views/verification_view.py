"""
Verification View Component (100% Capstone Review Demonstration)
Runs and displays all 10 academic evaluation scenarios.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from tests.test_scenarios import run_all_scenarios


class VerificationView(ttk.Frame):
    """Tab providing 1-click execution and display of the 5 Milestone 6 Review Scenarios."""

    def __init__(self, parent):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        # Header / Description Banner
        desc_frame = ttk.LabelFrame(self, text="Capstone Review (100% Target) — Comprehensive Academic Verification")
        desc_frame.pack(fill=tk.X, padx=10, pady=8)

        info_text = (
            "This panel runs the 10 academic review scenarios verifying the 100% production implementation:\n"
            "• Tests 1–5: Academic Constraints (Clashes, Best-Fit Seating, Room Allocation, Resource Availability)\n"
            "• Test 6: Milestone 8 Functional Programming Pipeline (map / filter / reduce score accumulation)\n"
            "• Test 7: Milestone 9 Multiprocessing Candidate Engine (ProcessPoolExecutor GIL bypass)\n"
            "• Test 8: Milestone 10 SymPy Symbolic Modeling (Matrix formulation & sensitivity analysis)\n"
            "• Test 9: Milestone 11 Meta-Heuristic Genetic Algorithm (Evolutionary chromosome optimization)\n"
            "• Test 10: Milestone 7 Distributed TCP Socket Client-Server (Length-prefixed JSON RPC)"
        )
        ttk.Label(desc_frame, text=info_text, justify=tk.LEFT, padding=6).pack(fill=tk.X)

        # Control Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=10, pady=4)

        run_btn = ttk.Button(toolbar, text="▶️ Run All 10 Capstone Scenarios", command=self.run_scenarios)
        run_btn.pack(side=tk.LEFT, padx=5)

        self.summary_var = tk.StringVar(value="Click 'Run All 10 Capstone Scenarios' to execute evaluation.")
        ttk.Label(toolbar, textvariable=self.summary_var, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=10)

        # Results Table
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        cols = ("scenario", "expected", "result", "details")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("scenario", text="Scenario")
        self.tree.heading("expected", text="Expected Specification")
        self.tree.heading("result", text="Result")
        self.tree.heading("details", text="Engine Diagnostic Output")

        self.tree.column("scenario", width=200, anchor=tk.W)
        self.tree.column("expected", width=250, anchor=tk.W)
        self.tree.column("result", width=90, anchor=tk.CENTER)
        self.tree.column("details", width=350, anchor=tk.W)

        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Configure row tags for Pass/Fail colors
        self.apply_theme("classic")

    def apply_theme(self, theme: str = "classic"):
        """Configure pass/fail tag colors based on theme."""
        if theme == "modern":
            self.tree.tag_configure("pass", background="#064E3B", foreground="#A7F3D0")
            self.tree.tag_configure("fail", background="#7F1D1D", foreground="#FECACA")
        else:
            self.tree.tag_configure("pass", background="#E8F5E9", foreground="#1B5E20")
            self.tree.tag_configure("fail", background="#FFEBEE", foreground="#B71C1C")

    def run_scenarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        results = run_all_scenarios()
        passed_count = 0

        for r in results:
            tag = "pass" if r["passed"] else "fail"
            res_label = "✅ PASS" if r["passed"] else "❌ FAIL"
            if r["passed"]:
                passed_count += 1

            self.tree.insert(
                "",
                tk.END,
                values=(
                    r["scenario"],
                    r["expected"],
                    res_label,
                    r["details"],
                ),
                tags=(tag,),
            )

        total = len(results)
        self.summary_var.set(f"Results: {passed_count}/{total} Scenarios Passed ({passed_count/total*100:.0f}%)")

        if passed_count == total:
            messagebox.showinfo(
                "Capstone Review Checkpoint Passed",
                f"All {total} Capstone Review Scenarios Passed Successfully!\n\nExamOpt meets all criteria for the 100% Academic Production Capstone Milestone."
            )
        else:
            messagebox.showwarning(
                "Checkpoint Warning",
                f"{passed_count}/{total} passed. Inspect the failures in the table."
            )

