"""
ExamOpt — Genetic Algorithm Studio View (Modern GUI)
Milestone 11: Meta-Heuristic Evolutionary Optimization
SRM Institute of Science and Technology, Tiruchirappalli
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable

from services.exam_service import ExamService
from scheduling.genetic_scheduler import GeneticScheduler, GeneticOptimizationResult
from config import (
    GA_DEFAULT_POPULATION_SIZE,
    GA_DEFAULT_GENERATIONS,
    GA_DEFAULT_MUTATION_RATE,
)

COLOR_BG = "#0B0F19"
COLOR_SURFACE = "#0F172A"
COLOR_BORDER = "#1E293B"
COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_ACCENT = "#6366F1"
COLOR_ACCENT_HOVER = "#4F46E5"
COLOR_SUCCESS = "#10B981"
COLOR_CARD = "#111827"


class GeneticStudioView(tk.Frame):
    """Interactive GUI for controlling and visualizing Genetic Algorithm optimization."""

    def __init__(self, parent, service: ExamService, on_data_changed: Optional[Callable] = None):
        super().__init__(parent, bg=COLOR_BG)
        self.service = service
        self.on_data_changed = on_data_changed
        self.last_result: Optional[GeneticOptimizationResult] = None

        self._build_ui()

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self, bg=COLOR_SURFACE, padx=16, pady=12, highlightthickness=1, highlightbackground=COLOR_BORDER)
        header.pack(fill=tk.X, padx=12, pady=(8, 12))

        title = tk.Label(
            header,
            text="🧬  Meta-Heuristic Genetic Algorithm Studio",
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_SURFACE,
        )
        title.pack(anchor=tk.W)

        sub = tk.Label(
            header,
            text="Evolutionary search solving NP-hard exam scheduling via chromosome crossover, mutation, and elitism.",
            font=("Segoe UI", 8),
            fg=COLOR_TEXT_MUTED,
            bg=COLOR_SURFACE,
        )
        sub.pack(anchor=tk.W, pady=(2, 0))

        # Control Panel & Metrics Grid
        controls_frame = tk.Frame(self, bg=COLOR_BG)
        controls_frame.pack(fill=tk.X, padx=12, pady=(0, 10))

        # Left: Parameter Sliders Card
        param_card = tk.Frame(controls_frame, bg=COLOR_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        param_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        tk.Label(param_card, text="ALGORITHM HYPERPARAMETERS", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        # Population
        tk.Label(param_card, text="Population Size:", font=("Segoe UI", 9), fg=COLOR_TEXT_PRIMARY, bg=COLOR_SURFACE).grid(row=1, column=0, sticky=tk.W, pady=4)
        self.pop_var = tk.IntVar(value=GA_DEFAULT_POPULATION_SIZE)
        pop_spin = tk.Spinbox(param_card, from_=10, to=200, increment=5, textvariable=self.pop_var, width=8, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        pop_spin.grid(row=1, column=1, sticky=tk.E, pady=4)

        # Generations
        tk.Label(param_card, text="Max Generations:", font=("Segoe UI", 9), fg=COLOR_TEXT_PRIMARY, bg=COLOR_SURFACE).grid(row=2, column=0, sticky=tk.W, pady=4)
        self.gen_var = tk.IntVar(value=GA_DEFAULT_GENERATIONS)
        gen_spin = tk.Spinbox(param_card, from_=5, to=200, increment=5, textvariable=self.gen_var, width=8, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        gen_spin.grid(row=2, column=1, sticky=tk.E, pady=4)

        # Mutation Rate
        tk.Label(param_card, text="Mutation Probability:", font=("Segoe UI", 9), fg=COLOR_TEXT_PRIMARY, bg=COLOR_SURFACE).grid(row=3, column=0, sticky=tk.W, pady=4)
        self.mut_var = tk.DoubleVar(value=GA_DEFAULT_MUTATION_RATE)
        mut_spin = tk.Spinbox(param_card, from_=0.01, to=0.50, increment=0.05, format="%.2f", textvariable=self.mut_var, width=8, bg=COLOR_CARD, fg=COLOR_TEXT_PRIMARY, insertbackground="white")
        mut_spin.grid(row=3, column=1, sticky=tk.E, pady=4)

        # Action Button
        run_btn = tk.Button(
            param_card,
            text="🚀  Run Genetic Evolution",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_ACCENT,
            fg="white",
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=12,
            pady=6,
            command=self._run_genetic_optimization,
        )
        run_btn.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=(8, 0))

        # Right: Fitness Metric Cards
        self.metric_card = tk.Frame(controls_frame, bg=COLOR_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        self.metric_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))

        tk.Label(self.metric_card, text="OPTIMIZATION OUTCOME", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(0, 6))

        metrics_grid = tk.Frame(self.metric_card, bg=COLOR_SURFACE)
        metrics_grid.pack(fill=tk.BOTH, expand=True)

        self.fit_lbl = self._create_metric_pill(metrics_grid, "Best Fitness", "--", 0, 0)
        self.clash_lbl = self._create_metric_pill(metrics_grid, "Hard Violations", "--", 0, 1)
        self.soft_lbl = self._create_metric_pill(metrics_grid, "Soft Penalty", "--", 1, 0)
        self.status_lbl = self._create_metric_pill(metrics_grid, "Timetable Status", "Ready", 1, 1)

        # Center: Canvas Fitness Progression Curve
        chart_frame = tk.Frame(self, bg=COLOR_SURFACE, padx=12, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDER)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        tk.Label(chart_frame, text="GENERATION FITNESS CONVERGENCE CURVE", font=("Segoe UI", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE).pack(anchor=tk.W, pady=(0, 6))

        self.canvas = tk.Canvas(chart_frame, bg=COLOR_CARD, highlightthickness=0, height=220)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self._draw_placeholder_chart()

    def _create_metric_pill(self, parent, title: str, initial_val: str, row: int, col: int) -> tk.Label:
        box = tk.Frame(parent, bg=COLOR_CARD, padx=10, pady=6, highlightthickness=1, highlightbackground=COLOR_BORDER)
        box.grid(row=row, column=col, sticky=tk.NSEW, padx=4, pady=4)
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(box, text=title, font=("Segoe UI", 7, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor=tk.W)
        val_lbl = tk.Label(box, text=initial_val, font=("Segoe UI", 12, "bold"), fg=COLOR_TEXT_PRIMARY, bg=COLOR_CARD)
        val_lbl.pack(anchor=tk.W, pady=(2, 0))
        return val_lbl

    def _draw_placeholder_chart(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            250, 110,
            text="Click 'Run Genetic Evolution' to view real-time generational convergence curve",
            fill=COLOR_TEXT_MUTED,
            font=("Segoe UI", 9, "italic"),
        )

    def _run_genetic_optimization(self):
        try:
            pop = self.pop_var.get()
            gen = self.gen_var.get()
            mut = self.mut_var.get()

            res = self.service.optimize_with_genetic_algorithm(population_size=pop, generations=gen)
            self.last_result = res

            # Update Metrics
            self.fit_lbl.config(text=f"{res.best_fitness:.2f}", fg=COLOR_SUCCESS)
            self.clash_lbl.config(text=str(res.hard_conflicts), fg=COLOR_SUCCESS if res.hard_conflicts == 0 else "#EF4444")
            self.soft_lbl.config(text=f"{res.soft_penalty:.1f}")
            self.status_lbl.config(text="100% Conflict-Free" if res.is_fully_valid else "Violations Detected")

            # Draw Canvas Curve
            self._draw_convergence_chart(res.history)

            if self.on_data_changed:
                self.on_data_changed()

            messagebox.showinfo(
                "Genetic Evolution Complete",
                f"Successfully evolved timetable over {res.generations_run} generations!\n\n"
                f"Best Fitness Score: {res.best_fitness:.4f}\n"
                f"Hard Constraints Breached: {res.hard_conflicts}\n"
                f"Total Soft Penalty: {res.soft_penalty:.2f}\n"
                f"Scheduled Exams: {len(res.best_schedule)}",
            )
        except Exception as e:
            messagebox.showerror("Genetic Algorithm Error", f"Failed to run evolution: {e}")

    def _draw_convergence_chart(self, history):
        self.canvas.delete("all")
        if not history:
            return

        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 220
        padding = 40

        # Axes
        self.canvas.create_line(padding, h - padding, w - padding, h - padding, fill=COLOR_BORDER, width=2)
        self.canvas.create_line(padding, padding, padding, h - padding, fill=COLOR_BORDER, width=2)

        # Plot best fitness points
        max_fit = max(item["best_fitness"] for item in history) or 1.0
        min_fit = min(item["best_fitness"] for item in history) or 0.0
        fit_range = max(1e-4, max_fit - min_fit)

        points = []
        n = len(history)
        for i, item in enumerate(history):
            x = padding + (i / max(1, n - 1)) * (w - 2 * padding)
            normalized_y = (item["best_fitness"] - min_fit) / fit_range
            y = (h - padding) - normalized_y * (h - 2 * padding)
            points.append((x, y))

        # Draw lines connecting points
        for i in range(len(points) - 1):
            self.canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill=COLOR_ACCENT, width=2)

        # Draw dots
        for pt in points:
            self.canvas.create_oval(pt[0] - 3, pt[1] - 3, pt[0] + 3, pt[1] + 3, fill="#38BDF8", outline=COLOR_BG)

        # Labels
        self.canvas.create_text(padding, h - padding + 15, text="Gen 1", fill=COLOR_TEXT_MUTED, font=("Segoe UI", 7))
        self.canvas.create_text(w - padding, h - padding + 15, text=f"Gen {n}", fill=COLOR_TEXT_MUTED, font=("Segoe UI", 7))
        self.canvas.create_text(padding + 25, padding - 10, text=f"Max Fit: {max_fit:.2f}", fill=COLOR_SUCCESS, font=("Segoe UI", 8, "bold"))
