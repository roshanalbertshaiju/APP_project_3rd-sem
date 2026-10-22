"""
ExamOpt — Multiprocessing Benchmark Studio View (Modern GUI)
Milestone 9: Multiprocessing & Parallel Computing (GIL Bypassing)
SRM Institute of Science and Technology, Tiruchirappalli
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
import time
from typing import Optional

from services.exam_service import ExamService

COLOR_BG = "#0B0F19"
COLOR_SURFACE = "#0F172A"
COLOR_BORDER = "#1E293B"
COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ACCENT = "#6366F1"
COLOR_ACCENT_HOVER = "#4F46E5"
COLOR_SUCCESS = "#10B981"
COLOR_CARD = "#111827"


class BenchmarkStudioView(tk.Frame):
    """Interactive GUI for demonstrating GIL bypassing and multi-core speedup."""

    def __init__(self, parent, service: ExamService, on_data_changed=None):
        super().__init__(parent, bg=COLOR_BG)
        self.service = service
        self.on_data_changed = on_data_changed

        self._build_ui()

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self, bg=COLOR_SURFACE, padx=16, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        header.pack(fill=tk.X, padx=12, pady=(8, 12))

        tk.Label(
            header,
            text="⚡  Multiprocessing & Multi-Core Acceleration Studio",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        ).pack(anchor=tk.W)

        tk.Label(
            header,
            text="Bypasses CPython's Global Interpreter Lock (GIL) via ProcessPoolExecutor to deliver true parallel CPU speedup.",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        ).pack(anchor=tk.W, pady=(2, 0))

        # Hardware & Parameters Bar
        top_grid = tk.Frame(self, bg=COLOR_BG)
        top_grid.pack(fill=tk.X, padx=12, pady=(0, 10))

        # System Hardware Card
        hw_card = tk.Frame(top_grid, bg=COLOR_SURFACE, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        hw_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        tk.Label(hw_card, text="SYSTEM HARDWARE TOPOLOGY", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(0, 6))

        cores = os.cpu_count() or 1
        info_lines = [
            ("Logical CPU Cores:", f"{cores} Cores Available"),
            ("CPython Execution:", "Sub-process Forking (GIL Bypassed)"),
            ("Master Process PID:", f"PID {os.getpid()}"),
        ]
        for lbl, val in info_lines:
            row = tk.Frame(hw_card, bg=COLOR_SURFACE)
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=lbl, font=("Segoe UI", 8), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(side=tk.LEFT)
            tk.Label(row, text=val, font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_SURFACE).pack(side=tk.RIGHT)

        # Benchmark Controls Card
        ctrl_card = tk.Frame(top_grid, bg=COLOR_SURFACE, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        ctrl_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        tk.Label(ctrl_card, text="BENCHMARK PARAMETERS", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(0, 6))

        c_row = tk.Frame(ctrl_card, bg=COLOR_SURFACE)
        c_row.pack(fill=tk.X, pady=4)
        tk.Label(c_row, text="Candidate Schedules:", font=("Segoe UI", 8), fg=COLOR_TEXT_PRIMARY, bg=COLOR_SURFACE).pack(side=tk.LEFT)
        self.cand_var = tk.IntVar(value=8)
        cand_spin = tk.Spinbox(c_row, from_=4, to=32, increment=4, textvariable=self.cand_var, width=6, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        cand_spin.pack(side=tk.RIGHT)

        run_bench_btn = tk.Button(
            ctrl_card,
            text="⚡  Run Multiprocessing Speedup Benchmark",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_ACCENT,
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            pady=6,
            command=self._run_benchmark,
        )
        run_bench_btn.pack(fill=tk.X, pady=(6, 0))

        # Results Dashboard
        dash = tk.Frame(self, bg=COLOR_SURFACE, padx=14, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        dash.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        tk.Label(dash, text="ACCELERATION & BENCHMARK METRICS", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(0, 8))

        # Metric Tiles
        tiles = tk.Frame(dash, bg=COLOR_SURFACE)
        tiles.pack(fill=tk.X, pady=(0, 12))

        self.seq_lbl = self._create_tile(tiles, "Single-Core Sequential Time", "--", 0, 0)
        self.par_lbl = self._create_tile(tiles, "Multi-Core Parallel Time", "--", 0, 1)
        self.speedup_lbl = self._create_tile(tiles, "Observed Speedup Factor", "--", 0, 2)
        self.eff_lbl = self._create_tile(tiles, "Core Parallel Efficiency", "--", 0, 3)

        # Canvas Bar Comparison
        tk.Label(dash, text="EXECUTION LATENCY COMPARISON (LOWER IS BETTER)", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(4, 4))
        self.canvas = tk.Canvas(dash, bg=COLOR_CARD, highlightthickness=0, height=130)
        self.canvas.pack(fill=tk.X, expand=True)
        self._draw_placeholder_bars()

    def _create_tile(self, parent, title: str, initial_val: str, row: int, col: int) -> tk.Label:
        box = tk.Frame(parent, bg=COLOR_CARD, padx=10, pady=6, highlightthickness=1, highlightbackground=COLOR_BORDER)
        box.grid(row=row, column=col, sticky=tk.NSEW, padx=4, pady=2)
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(box, text=title, font=("Segoe UI", 7, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor=tk.W)
        val_lbl = tk.Label(box, text=initial_val, font=("Segoe UI", 12, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        val_lbl.pack(anchor=tk.W, pady=(2, 0))
        return val_lbl

    def _draw_placeholder_bars(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            300, 65,
            text="Click 'Run Multiprocessing Speedup Benchmark' to execute live comparative profiling",
            fill=COLOR_TEXT_MUTED,
            font=("Segoe UI", 9, "italic"),
        )

    def _run_benchmark(self):
        try:
            candidates = self.cand_var.get()
            bm = self.service.benchmark_multiprocessing(num_candidates=candidates)

            seq_t = bm["sequential_time_seconds"]
            par_t = bm["parallel_time_seconds"]
            speedup = bm["speedup_factor"]
            eff = bm["efficiency_percentage"]

            self.seq_lbl.config(text=f"{seq_t:.3f} s")
            self.par_lbl.config(text=f"{par_t:.3f} s", fg=COLOR_SUCCESS)
            self.speedup_lbl.config(text=f"{speedup:.2f}x", fg=COLOR_SUCCESS)
            self.eff_lbl.config(text=f"{eff:.1f} %")

            # Draw Bars
            self._draw_bars(seq_t, par_t, bm["workers_deployed"])
        except Exception as e:
            messagebox.showerror("Benchmark Error", f"Failed to execute parallel benchmark: {e}")

    def _draw_bars(self, seq_t: float, par_t: float, workers: int):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 600
        max_t = max(seq_t, par_t) or 1.0

        bar_max_w = w - 240
        w_seq = int((seq_t / max_t) * bar_max_w)
        w_par = int((par_t / max_t) * bar_max_w)

        # Bar 1: Sequential
        self.canvas.create_text(20, 35, anchor=tk.W, text="1 Core (Sequential):", fill=COLOR_TEXT_PRIMARY, font=("Segoe UI", 8, "bold"))
        self.canvas.create_rectangle(170, 22, 170 + max(20, w_seq), 48, fill="#EF4444", outline="")
        self.canvas.create_text(180 + max(20, w_seq), 35, anchor=tk.W, text=f"{seq_t:.3f}s", fill=COLOR_TEXT_PRIMARY, font=("Segoe UI", 8, "bold"))

        # Bar 2: Parallel
        self.canvas.create_text(20, 85, anchor=tk.W, text=f"{workers} Cores (Parallel):", fill=COLOR_TEXT_PRIMARY, font=("Segoe UI", 8, "bold"))
        self.canvas.create_rectangle(170, 72, 170 + max(20, w_par), 98, fill=COLOR_SUCCESS, outline="")
        self.canvas.create_text(180 + max(20, w_par), 85, anchor=tk.W, text=f"{par_t:.3f}s ({seq_t / max(1e-4, par_t):.1f}x faster)", fill=COLOR_SUCCESS, font=("Segoe UI", 8, "bold"))
