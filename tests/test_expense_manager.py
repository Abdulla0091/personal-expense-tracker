import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from expense_manager import ExpenseManager
from storage import JSONStorage


class ExpenseManagerTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        path = Path(self.temp_dir.name) / "expenses.json"
        self.manager = ExpenseManager(JSONStorage(path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_expense(self):
        expense = self.manager.add_expense(
            250,
            "Food",
            "Lunch",
            "2026-08-24",
        )

        self.assertEqual(expense.id, 1)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.amount, 250)

    def test_delete_expense(self):
        expense = self.manager.add_expense(
            100,
            "Transport",
            "Bus fare",
            "2026-08-24",
        )

        self.assertTrue(self.manager.delete_expense(expense.id))
        self.assertIsNone(self.manager.get_by_id(expense.id))

    def test_monthly_summary(self):
        self.manager.add_expense(100, "Food", "Breakfast", "2026-08-10")
        self.manager.add_expense(200, "Food", "Lunch", "2026-08-15")
        self.manager.add_expense(300, "Transport", "Bus", "2026-09-01")

        total, categories = self.manager.monthly_summary(2026, 8)

        self.assertEqual(total, 300)
        self.assertEqual(categories["Food"], 300)


if __name__ == "__main__":
    unittest.main()
