from datetime import datetime

from models import Expense
from storage import JSONStorage


class ExpenseManager:
    """Business logic for creating and managing expenses."""

    def __init__(self, storage: JSONStorage):
        self.storage = storage
        self.expenses = self.storage.load()

    def _next_id(self) -> int:
        return max((expense.id for expense in self.expenses), default=0) + 1

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        expense_date: str | None = None,
    ) -> Expense:

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if not category.strip():
            raise ValueError("Category cannot be empty.")

        if not description.strip():
            raise ValueError("Description cannot be empty.")

        if expense_date:
            self._validate_date(expense_date)

        expense = Expense.create(
            self._next_id(),
            amount,
            category,
            description,
            expense_date,
        )

        self.expenses.append(expense)
        self.storage.save(self.expenses)

        return expense

    def get_all(self) -> list[Expense]:
        return sorted(
            self.expenses,
            key=lambda expense: (expense.expense_date, expense.id),
            reverse=True,
        )

    def get_by_id(self, expense_id: int) -> Expense | None:
        return next(
            (expense for expense in self.expenses if expense.id == expense_id),
            None,
        )

    def update_expense(
        self,
        expense_id: int,
        amount: float | None = None,
        category: str | None = None,
        description: str | None = None,
        expense_date: str | None = None,
    ) -> Expense | None:
        """Update an existing expense safely and save the changes."""

        expense = self.get_by_id(expense_id)

        if expense is None:
            return None

        # Validate everything BEFORE changing the expense
        if amount is not None:
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

        if category is not None:
            if not category.strip():
                raise ValueError("Category cannot be empty.")

        if description is not None:
            if not description.strip():
                raise ValueError("Description cannot be empty.")

        if expense_date is not None:
            self._validate_date(expense_date)

        # Apply changes only after ALL validation passes
        if amount is not None:
            expense.amount = round(amount, 2)

        if category is not None:
            expense.category = category.strip().title()

        if description is not None:
            expense.description = description.strip()

        if expense_date is not None:
            expense.expense_date = expense_date

        self.storage.save(self.expenses)

        return expense

    def delete_expense(self, expense_id: int) -> bool:
        expense = self.get_by_id(expense_id)

        if expense is None:
            return False

        self.expenses.remove(expense)
        self.storage.save(self.expenses)

        return True

    def search(self, keyword: str) -> list[Expense]:
        keyword = keyword.lower().strip()

        return [
            expense
            for expense in self.get_all()
            if keyword in expense.category.lower()
            or keyword in expense.description.lower()
            or keyword in expense.expense_date.lower()
        ]

    def monthly_summary(
        self,
        year: int,
        month: int,
    ) -> tuple[float, dict[str, float]]:

        prefix = f"{year:04d}-{month:02d}"

        matching = [
            expense
            for expense in self.expenses
            if expense.expense_date.startswith(prefix)
        ]

        total = round(
            sum(expense.amount for expense in matching),
            2,
        )

        by_category: dict[str, float] = {}

        for expense in matching:
            by_category[expense.category] = round(
                by_category.get(expense.category, 0) + expense.amount,
                2,
            )

        return total, by_category

    def export_to_csv(self, file_path: str) -> int:
        """Export all expenses to a CSV file."""

        import csv

        expenses = self.get_all()

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date",
            ])

            for expense in expenses:
                writer.writerow([
                    expense.id,
                    expense.amount,
                    expense.category,
                    expense.description,
                    expense.expense_date,
                ])

        return len(expenses)
        
    def category_monthly_summary(
        self,
        year: int,
        month: int,
    ) -> dict[str, float]:
        """Return total expenses grouped by category for a month."""

        prefix = f"{year:04d}-{month:02d}"

        summary: dict[str, float] = {}

        for expense in self.expenses:
            if expense.expense_date.startswith(prefix):
                category = expense.category
                summary[category] = round(
                    summary.get(category, 0) + expense.amount,
                    2,
                )

        return dict(sorted(summary.items()))

    @staticmethod
    def _validate_date(value: str) -> None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(
                "Date must use YYYY-MM-DD format."
            ) from exc