"""
Unit Tests for Milestone 10: Symbolic Mathematical Optimization (SymPy)
SRM Institute of Science and Technology, Tiruchirappalli
"""
import unittest
import sympy as sp

from optimization.symbolic_model import SymbolicTimetableModel
from config import WEIGHT_STUDENT_CONSECUTIVE, HARD_VIOLATION_PENALTY


class TestSymbolicModel(unittest.TestCase):
    def setUp(self):
        self.model = SymbolicTimetableModel()

    def test_symbolic_expression_generation(self):
        expr = self.model.get_objective_expression()
        self.assertIsInstance(expr, sp.Expr)
        # Verify symbols are part of the expression
        free_symbols = {s.name for s in expr.free_symbols}
        self.assertIn("M_hard", free_symbols)
        self.assertIn("N_hard", free_symbols)
        self.assertIn("w_consec", free_symbols)
        self.assertIn("P_consec", free_symbols)

    def test_gradients(self):
        grads = self.model.compute_gradients()
        self.assertEqual(str(grads["dZ_dw_consec"]), "P_consec")
        self.assertEqual(str(grads["dZ_dP_consec"]), "w_consec")

    def test_evaluate_loss_substitution(self):
        # 0 hard violations, 2 consecutive students, 1 faculty overload, 20 seat waste
        loss = self.model.evaluate_loss(n_hard=0, p_consec=2, p_fac=1, p_waste=20)
        # Expected: 2 * 10 + 1 * 15 + 20 * 0.5 = 20 + 15 + 10 = 45
        self.assertAlmostEqual(loss, 45.0, places=1)

    def test_hard_violation_penalty(self):
        # 1 hard violation should heavily inflate penalty
        loss = self.model.evaluate_loss(n_hard=1, p_consec=0, p_fac=0, p_waste=0)
        self.assertGreaterEqual(loss, HARD_VIOLATION_PENALTY)

    def test_sensitivity_analysis(self):
        penalties = {"consecutive": 5, "faculty": 2, "waste": 30}
        sens = self.model.perform_sensitivity_analysis(penalties, delta_pct=0.25)
        self.assertIn("base_loss", sens)
        self.assertIn("sensitivities", sens)
        self.assertIn("w_consec_sensitivity", sens["sensitivities"])


if __name__ == "__main__":
    unittest.main()
