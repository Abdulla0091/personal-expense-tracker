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

    # -------------------------
    # Add Expense Tests
    # -------------------------

    def test_add_expense(self):
        expense = self.manager.add_expense(
            250,
            "Food",
            "Lunch",
            "2026-08-24",
        )

        self.assertEqual(expense.id, 1)
        self.assertEqual(expense.amount, 250)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Lunch")
        self.assertEqual(expense.expense_date, "2026-08-24")

    def test_add_expense_generates_incremental_id(self):
        first = self.manager.add_expense(
            100,
            "Food",
            "Breakfast",
            "2026-08-24",
        )

        second = self.manager.add_expense(
            200,
            "Transport",
            "Bus",
            "2026-08-24",
        )

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_add_expense_rejects_zero_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(
                0,
                "Food",
                "Lunch",
                "2026-08-24",
            )

    def test_add_expense_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(
                -100,
                "Food",
                "Lunch",
                "2026-08-24",
            )

    def test_add_expense_rejects_empty_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(
                100,
                "",
                "Lunch",
                "2026-08-24",
            )

    def test_add_expense_rejects_empty_description(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(
                100,
                "Food",
                "",
                "2026-08-24",
            )

    def test_add_expense_rejects_invalid_date(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense(
                100,
                "Food",
                "Lunch",
                "2026/08/24",
            )

    # -------------------------
    # Get Expense Tests
    # -------------------------

    def test_get_by_id(self):
        expense = self.manager.add_expense(
            150,
            "Shopping",
            "T-shirt",
            "2026-08-24",
        )

        result = self.manager.get_by_id(expense.id)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, expense.id)

    def test_get_by_id_returns_none_for_missing_expense(self):
        result = self.manager.get_by_id(999)

        self.assertIsNone(result)

    # -------------------------
    # Delete Expense Tests
    # -------------------------

    def test_delete_expense(self):
        expense = self.manager.add_expense(
            100,
            "Transport",
            "Bus fare",
            "2026-08-24",
        )

        self.assertTrue(self.manager.delete_expense(expense.id))
        self.assertIsNone(self.manager.get_by_id(expense.id))

    def test_delete_non_existing_expense(self):
        self.assertFalse(self.manager.delete_expense(999))

    # -------------------------
    # Search Tests
    # -------------------------

    def test_search_by_category(self):
        self.manager.add_expense(
            100,
            "Food",
            "Breakfast",
            "2026-08-24",
        )

        self.manager.add_expense(
            200,
            "Transport",
            "Bus",
            "2026-08-24",
        )

        results = self.manager.search("food")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, "Food")

    def test_search_by_description(self):
        self.manager.add_expense(
            100,
            "Food",
            "Chicken lunch",
            "2026-08-24",
        )

        results = self.manager.search("chicken")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].description, "Chicken lunch")

    def test_search_by_date(self):
        self.manager.add_expense(
            100,
            "Food",
            "Breakfast",
            "2026-08-24",
        )

        results = self.manager.search("2026-08-24")

        self.assertEqual(len(results), 1)

    def test_search_is_case_insensitive(self):
        self.manager.add_expense(
            100,
            "Food",
            "Lunch",
            "2026-08-24",
        )

        results = self.manager.search("FOOD")

        self.assertEqual(len(results), 1)

    # -------------------------
    # Monthly Summary Tests
    # -------------------------

    def test_monthly_summary(self):
        self.manager.add_expense(
            100,
            "Food",
            "Breakfast",
            "2026-08-10",
        )

        self.manager.add_expense(
            200,
            "Food",
            "Lunch",
            "2026-08-15",
        )

        self.manager.add_expense(
            300,
            "Transport",
            "Bus",
            "2026-09-01",
        )

        total, categories = self.manager.monthly_summary(2026, 8)

        self.assertEqual(total, 300)
        self.assertEqual(categories["Food"], 300)

    def test_monthly_summary_returns_zero_for_empty_month(self):
        total, categories = self.manager.monthly_summary(2026, 12)

        self.assertEqual(total, 0)
        self.assertEqual(categories, {})
        
    def test_category_monthly_summary(self):
        self.manager.add_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-10",
        )
        self.manager.add_expense(
            300,
            "Transport",
            "Bus",
            "2026-08-15",
        )
        self.manager.add_expense(
            250,
            "Food",
            "Dinner",
            "2026-08-20",
        )
        self.manager.add_expense(
            1000,
            "Shopping",
            "Clothes",
            "2026-07-20",
        )

        result = self.manager.category_monthly_summary(2026, 8)

        self.assertEqual(
            result,
            {
                "Food": 750,
                "Transport": 300,
            },
        )    

    # -------------------------
    # Update Expense Tests
    # -------------------------

    def test_update_expense(self):
        expense = self.manager.add_expense(
            250,
            "Food",
            "Lunch",
            "2026-08-24",
        )

        updated = self.manager.update_expense(
            expense.id,
            300,
            "Food",
            "Dinner",
            "2026-08-25",
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated.id, expense.id)
        self.assertEqual(updated.amount, 300)
        self.assertEqual(updated.category, "Food")
        self.assertEqual(updated.description, "Dinner")
        self.assertEqual(updated.expense_date, "2026-08-25")

    def test_update_non_existing_expense(self):
        result = self.manager.update_expense(
            999,
            300,
            "Food",
            "Dinner",
            "2026-08-25",
        )

        self.assertIsNone(result)

    def test_update_expense_rejects_invalid_amount(self):
        expense = self.manager.add_expense(
            250,
            "Food",
            "Lunch",
            "2026-08-24",
        )

        with self.assertRaises(ValueError):
            self.manager.update_expense(
                expense.id,
                -100,
                "Food",
                "Dinner",
                "2026-08-25",
            )

    # -------------------------
    # CSV Export Tests
    # -------------------------

    def test_export_to_csv(self):
        self.manager.add_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-30",
        )

        self.manager.add_expense(
            700,
            "Transport",
            "Bus",
            "2026-08-30",
        )

        csv_path = Path(self.temp_dir.name) / "expenses.csv"

        count = self.manager.export_to_csv(str(csv_path))

        self.assertEqual(count, 2)
        self.assertTrue(csv_path.exists())

        content = csv_path.read_text(encoding="utf-8")

        self.assertIn("ID,Amount,Category,Description,Date", content)
        self.assertIn("Food", content)
        self.assertIn("Transport", content)
        self.assertIn("Lunch", content)
        self.assertIn("Bus", content)


if __name__ == "__main__":
    unittest.main()