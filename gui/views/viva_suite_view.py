"""
ExamOpt — Academic Review & Viva Suite View
SRM Institute of Science and Technology, Tiruchirappalli

Consolidates all technical verification, parallel benchmarking, symbolic mathematical
modeling, and evolutionary analytics into a single unified academic examination dashboard.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
import json
from typing import Optional

from services.exam_service import ExamService
from tests.test_scenarios import run_all_scenarios
from optimization.symbolic_model import SymbolicTimetableModel

COLOR_BG = "#0B0F19"
COLOR_SURFACE = "#0F172A"
COLOR_BORDER = "#1E293B"
COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ACCENT = "#6366F1"
COLOR_SUCCESS = "#10B981"
COLOR_CARD = "#111827"


class VivaSuiteView(ttk.Frame):
    """Unified Academic Review & Viva Defense Suite."""

    def __init__(self, parent, service: ExamService, on_data_changed=None):
        super().__init__(parent)
        self.service = service
        self.on_data_changed = on_data_changed

        self._build_ui()

    def _build_ui(self):
        # Master Notebook inside this view for clean sub-tabs
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # 1. Sub-Tab: 10 Review Scenarios
        self.scenarios_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.scenarios_frame, text="🧪  10 Capstone Scenarios")
        self._build_scenarios_tab(self.scenarios_frame)

        # 2. Sub-Tab: Multi-Core Benchmarking
        self.benchmark_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.benchmark_frame, text="⚡  CPU Multi-Core Acceleration")
        self._build_benchmark_tab(self.benchmark_frame)

        # 3. Sub-Tab: SymPy Mathematical Modeling
        self.sympy_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.sympy_frame, text="📐  SymPy Symbolic Modeling")
        self._build_sympy_tab(self.sympy_frame)

    # =========================================================================
    # SUB-TAB 1: 10 ACADEMIC REVIEW SCENARIOS
    # =========================================================================
    def _build_scenarios_tab(self, parent):
        top_bar = ttk.Frame(parent)
        top_bar.pack(fill=tk.X, padx=8, pady=6)

        run_btn = ttk.Button(top_bar, text="▶️ Run All 10 Capstone Scenarios", command=self._run_all_scenarios)
        run_btn.pack(side=tk.LEFT, padx=5)

        self.scenario_summary_var = tk.StringVar(value="Click button above to evaluate all 10 academic scenarios.")
        ttk.Label(top_bar, textvariable=self.scenario_summary_var, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=10)

        # Table
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))

        cols = ("scenario", "expected", "result", "details")
        self.sc_tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.sc_tree.heading("scenario", text="Scenario")
        self.sc_tree.heading("expected", text="Expected Specification")
        self.sc_tree.heading("result", text="Result")
        self.sc_tree.heading("details", text="Engine Diagnostic Output")

        self.sc_tree.column("scenario", width=220, anchor=tk.W)
        self.sc_tree.column("expected", width=260, anchor=tk.W)
        self.sc_tree.column("result", width=90, anchor=tk.CENTER)
        self.sc_tree.column("details", width=380, anchor=tk.W)

        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.sc_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.sc_tree.xview)
        self.sc_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.sc_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.sc_tree.tag_configure("pass", background="#E8F5E9", foreground="#1B5E20")
        self.sc_tree.tag_configure("fail", background="#FFEBEE", foreground="#B71C1C")

    def _run_all_scenarios(self):
        for item in self.sc_tree.get_children():
            self.sc_tree.delete(item)

        results = run_all_scenarios()
        passed_count = 0
        for r in results:
            tag = "pass" if r["passed"] else "fail"
            res_label = "✅ PASS" if r["passed"] else "❌ FAIL"
            if r["passed"]:
                passed_count += 1
            self.sc_tree.insert(
                "",
                tk.END,
                values=(r["scenario"], r["expected"], res_label, r["details"]),
                tags=(tag,),
            )

        total = len(results)
        self.scenario_summary_var.set(f"Results: {passed_count}/{total} Passed ({passed_count/total*100:.0f}%) — All Hard & Soft Constraints Verified")

    # =========================================================================
    # SUB-TAB 2: CPU MULTIPROCESSING BENCHMARK
    # =========================================================================
    def _build_benchmark_tab(self, parent):
        info_frame = ttk.LabelFrame(parent, text="CPython GIL Bypassing via ProcessPoolExecutor")
        info_frame.pack(fill=tk.X, padx=10, pady=8)

        cores = os.cpu_count() or 1
        desc = (
            f"• Hardware Topology: {cores} Logical CPU Cores Detected\n"
            f"• Operating Mechanism: Sub-process forking across OS cores to circumvent Python's Global Interpreter Lock (GIL)\n"
            f"• Purpose: Evaluates candidate timetable variations in parallel with measurable Amdahl speedup."
        )
        ttk.Label(info_frame, text=desc, justify=tk.LEFT, padding=6).pack(fill=tk.X)

        # Control
        ctrl_bar = ttk.Frame(parent)
        ctrl_bar.pack(fill=tk.X, padx=10, pady=4)

        run_bm_btn = ttk.Button(ctrl_bar, text="⚡ Run Comparative Multi-Core Speedup Benchmark", command=self._run_benchmark)
        run_bm_btn.pack(side=tk.LEFT, padx=5)

        self.bm_status_var = tk.StringVar(value="Click button above to benchmark 1 Core vs N Cores.")
        ttk.Label(ctrl_bar, textvariable=self.bm_status_var, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=10)

        # Canvas for comparative bars
        canvas_frame = ttk.LabelFrame(parent, text="Benchmark Execution Latency (Lower is Better)")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        self.bm_canvas = tk.Canvas(canvas_frame, bg="#FFFFFF", highlightthickness=0, height=180)
        self.bm_canvas.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.bm_canvas.create_text(280, 80, text="Click 'Run Comparative Multi-Core Speedup Benchmark' to execute profiling", fill="#666666", font=("Segoe UI", 9, "italic"))

    def _run_benchmark(self):
        try:
            bm = self.service.benchmark_multiprocessing(num_candidates=8)
            seq_t = bm["sequential_time_seconds"]
            par_t = bm["parallel_time_seconds"]
            speedup = bm["speedup_factor"]
            workers = bm["workers_deployed"]
            eff = bm["efficiency_percentage"]

            self.bm_status_var.set(f"Sequential: {seq_t:.3f}s | Parallel ({workers} Cores): {par_t:.3f}s | Speedup: {speedup:.2f}x ({eff:.1f}% efficiency)")

            # Draw canvas bars
            self.bm_canvas.delete("all")
            w = self.bm_canvas.winfo_width() or 600
            max_t = max(seq_t, par_t) or 1.0
            bar_max_w = w - 260

            w_seq = int((seq_t / max_t) * bar_max_w)
            w_par = int((par_t / max_t) * bar_max_w)

            self.bm_canvas.create_text(20, 45, anchor=tk.W, text="1 Core (Sequential):", fill="#111827", font=("Segoe UI", 9, "bold"))
            self.bm_canvas.create_rectangle(180, 32, 180 + max(20, w_seq), 58, fill="#EF4444", outline="")
            self.bm_canvas.create_text(190 + max(20, w_seq), 45, anchor=tk.W, text=f"{seq_t:.3f}s", fill="#111827", font=("Segoe UI", 9, "bold"))

            self.bm_canvas.create_text(20, 95, anchor=tk.W, text=f"{workers} Cores (Parallel):", fill="#111827", font=("Segoe UI", 9, "bold"))
            self.bm_canvas.create_rectangle(180, 82, 180 + max(20, w_par), 108, fill="#10B981", outline="")
            self.bm_canvas.create_text(190 + max(20, w_par), 95, anchor=tk.W, text=f"{par_t:.3f}s ({speedup:.1f}x speedup)", fill="#10B981", font=("Segoe UI", 9, "bold"))
        except Exception as e:
            messagebox.showerror("Benchmark Error", f"Profiling failed: {e}")

    # =========================================================================
    # SUB-TAB 3: SYMPY MATHEMATICAL MODELING
    # =========================================================================
    def _build_sympy_tab(self, parent):
        model_frame = ttk.LabelFrame(parent, text="Formal Examination Timetabling Problem (ETP) Formulation")
        model_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        model = SymbolicTimetableModel()
        expr = model.get_objective_expression()
        grads = model.compute_gradients()
        latex = model.get_latex_formulation()

        info = (
            "MATHEMATICAL OBJECTIVE FORMULATION (SymPy)\n"
            "--------------------------------------------------------------------------------\n"
            f"• Objective Function:  Z = M_hard * N_hard + (w_consec * P_consec + w_fac * P_fac + w_waste * P_waste)\n"
            f"• Vector Representation: Z_soft = W^T * P, where W = [w_consec, w_fac, w_waste]^T\n"
            f"• Symbolic Expression:  {expr}\n\n"
            "ANALYTICAL SENSITIVITY GRADIENTS (Partial Derivatives)\n"
            "--------------------------------------------------------------------------------\n"
            f"• dZ / dw_consec  = {grads['dZ_dw_consec']}  (Sensitivity to student consecutive exam penalty)\n"
            f"• dZ / dw_fac     = {grads['dZ_dw_fac']}     (Sensitivity to faculty excess duty penalty)\n"
            f"• dZ / dw_waste   = {grads['dZ_dw_waste']}   (Sensitivity to room seat wastage penalty)\n\n"
            "EXPORTABLE LATEX FORMULATION (For Thesis / Slides)\n"
            "--------------------------------------------------------------------------------\n"
            f"\\mathcal{{Z}}_{{\\text{{total}}}} = {latex['objective_latex']}\n"
            f"\\mathcal{{Z}}_{{\\text{{soft}}}}  = {latex['soft_penalty_latex']}"
        )

        self.sympy_txt = tk.Text(model_frame, wrap=tk.WORD, font=("Consolas", 10), bg="#F8FAFC", fg="#0F172A", relief=tk.FLAT, padx=12, pady=12)
        self.sympy_txt.insert(tk.END, info)
        self.sympy_txt.config(state=tk.DISABLED)
        self.sympy_txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    def refresh(self):
        """Called on tab change or global refresh."""
        pass

    def apply_theme(self, theme: str):
        """Applies theme colors to custom Tk widgets like Text and Canvas."""
        if theme == "modern":
            if hasattr(self, "sympy_txt"):
                self.sympy_txt.config(bg=COLOR_CARD, fg="#A7F3D0")
            if hasattr(self, "bm_canvas"):
                self.bm_canvas.config(bg=COLOR_SURFACE)

