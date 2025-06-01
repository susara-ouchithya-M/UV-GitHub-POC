import unittest
# from cashflow_models.cashflow_model import calculate_cashflow

class TestCashflowModel(unittest.TestCase):
    def test_calculate_cashflow(self):
        initial_investment = 1000
        cashflows = [200, 300, 400, 500]
        discount_rate = 0.05
        expected_npv = 292.58  # Example expected value

        npv = calculate_cashflow(initial_investment, cashflows, discount_rate)
        self.assertAlmostEqual(npv, expected_npv, places=2)

if __name__ == '__main__':
    unittest.main()

