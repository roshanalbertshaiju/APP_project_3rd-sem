"""
ExamOpt — Symbolic Mathematical Optimization Model (SymPy)
Milestone 10: Symbolic Modeling and Objective Function Formulation
SRM Institute of Science and Technology, Tiruchirappalli

Formal mathematical formulation of the Examination Timetabling Problem (ETP)
using SymPy symbolic calculus, matrix algebra, and analytical sensitivity analysis.
"""
from typing import Dict, Any, Tuple
import sympy as sp

from config import (
    WEIGHT_STUDENT_CONSECUTIVE,
    WEIGHT_FACULTY_OVERLOAD,
    WEIGHT_ROOM_SEAT_WASTE,
    HARD_VIOLATION_PENALTY,
)


class SymbolicTimetableModel:
    """
    Symbolic mathematical formulation of the examination timetabling objective function.
    Leverages SymPy for symbolic algebra, partial differentiation, and matrix calculations.
    """

    def __init__(self):
        # 1. Define Symbolic Weights
        self.w_consec = sp.Symbol("w_consec", positive=True, real=True)
        self.w_fac = sp.Symbol("w_fac", positive=True, real=True)
        self.w_waste = sp.Symbol("w_waste", positive=True, real=True)
        self.M_hard = sp.Symbol("M_hard", positive=True, real=True)

        # 2. Define Symbolic Penalty Metric Variables
        self.N_hard = sp.Symbol("N_hard", integer=True, nonnegative=True)
        self.P_consec = sp.Symbol("P_consec", integer=True, nonnegative=True)
        self.P_fac = sp.Symbol("P_fac", integer=True, nonnegative=True)
        self.P_waste = sp.Symbol("P_waste", integer=True, nonnegative=True)

        # 3. Formulate Symbolic Vectors and Matrices
        self.W_vector = sp.Matrix([self.w_consec, self.w_fac, self.w_waste])
        self.P_vector = sp.Matrix([self.P_consec, self.P_fac, self.P_waste])

        # 4. Symbolic Soft Objective (Dot Product: W^T * P)
        self.Z_soft = (self.W_vector.T * self.P_vector)[0]

        # 5. Symbolic Total Objective (Z_total = M_hard * N_hard + Z_soft)
        self.Z_total = self.M_hard * self.N_hard + self.Z_soft

        # 6. Symbolic Bounded Fitness Function: F = 1000 / (1 + Z_total)
        self.Fitness = 1000 / (1 + self.Z_total)

    def get_objective_expression(self) -> sp.Expr:
        """Returns the analytical expression for Z_total."""
        return self.Z_total

    def get_latex_formulation(self) -> Dict[str, str]:
        """Exports LaTeX representations of the mathematical models for documentation."""
        return {
            "objective_latex": sp.latex(self.Z_total),
            "soft_penalty_latex": sp.latex(self.Z_soft),
            "fitness_latex": sp.latex(self.Fitness),
            "weight_vector": sp.latex(self.W_vector),
            "penalty_vector": sp.latex(self.P_vector),
        }

    def compute_gradients(self) -> Dict[str, sp.Expr]:
        """
        Computes symbolic partial derivatives (gradients) with respect to each weight.
        Demonstrates analytical sensitivity analysis.
        """
        return {
            "dZ_dw_consec": sp.diff(self.Z_total, self.w_consec),
            "dZ_dw_fac": sp.diff(self.Z_total, self.w_fac),
            "dZ_dw_waste": sp.diff(self.Z_total, self.w_waste),
            "dZ_dP_consec": sp.diff(self.Z_total, self.P_consec),
            "dZ_dP_fac": sp.diff(self.Z_total, self.P_fac),
            "dZ_dP_waste": sp.diff(self.Z_total, self.P_waste),
        }

    def evaluate_loss(
        self,
        n_hard: int,
        p_consec: int,
        p_fac: int,
        p_waste: int,
        weights: Dict[str, float] = None,
    ) -> float:
        """
        Substitutes concrete numerical values into the symbolic objective function
        and computes the scalar cost.
        """
        w_c = (weights or {}).get("w_consec", WEIGHT_STUDENT_CONSECUTIVE)
        w_f = (weights or {}).get("w_fac", WEIGHT_FACULTY_OVERLOAD)
        w_w = (weights or {}).get("w_waste", WEIGHT_ROOM_SEAT_WASTE)
        m_h = (weights or {}).get("M_hard", HARD_VIOLATION_PENALTY)

        subs_map = {
            self.N_hard: n_hard,
            self.P_consec: p_consec,
            self.P_fac: p_fac,
            self.P_waste: p_waste,
            self.w_consec: w_c,
            self.w_fac: w_f,
            self.w_waste: w_w,
            self.M_hard: m_h,
        }

        eval_result = float(self.Z_total.evalf(subs=subs_map))
        return eval_result

    def perform_sensitivity_analysis(
        self,
        baseline_penalties: Dict[str, int],
        delta_pct: float = 0.20,
    ) -> Dict[str, Any]:
        """
        Calculates how perturbing each constraint weight by delta_pct (e.g. ±20%)
        shifts the total objective penalty.
        """
        p_consec = baseline_penalties.get("consecutive", 0)
        p_fac = baseline_penalties.get("faculty", 0)
        p_waste = baseline_penalties.get("waste", 0)

        base_loss = self.evaluate_loss(0, p_consec, p_fac, p_waste)

        variations = {}
        # Perturb w_consec
        loss_high_c = self.evaluate_loss(0, p_consec, p_fac, p_waste, {"w_consec": WEIGHT_STUDENT_CONSECUTIVE * (1 + delta_pct)})
        variations["w_consec_sensitivity"] = {
            "delta_loss": round(loss_high_c - base_loss, 2),
            "percentage_change": round(((loss_high_c - base_loss) / (base_loss + 1e-6)) * 100, 2),
        }

        # Perturb w_fac
        loss_high_f = self.evaluate_loss(0, p_consec, p_fac, p_waste, {"w_fac": WEIGHT_FACULTY_OVERLOAD * (1 + delta_pct)})
        variations["w_fac_sensitivity"] = {
            "delta_loss": round(loss_high_f - base_loss, 2),
            "percentage_change": round(((loss_high_f - base_loss) / (base_loss + 1e-6)) * 100, 2),
        }

        # Perturb w_waste
        loss_high_w = self.evaluate_loss(0, p_consec, p_fac, p_waste, {"w_waste": WEIGHT_ROOM_SEAT_WASTE * (1 + delta_pct)})
        variations["w_waste_sensitivity"] = {
            "delta_loss": round(loss_high_w - base_loss, 2),
            "percentage_change": round(((loss_high_w - base_loss) / (base_loss + 1e-6)) * 100, 2),
        }

        return {
            "base_loss": round(base_loss, 2),
            "delta_percentage": int(delta_pct * 100),
            "sensitivities": variations,
        }
