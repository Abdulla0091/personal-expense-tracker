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

    def monthly_summary(self, year: int, month: int) -> tuple[float, dict[str, float]]:
        prefix = f"{year:04d}-{month:02d}"
        matching = [
            expense for expense in self.expenses
            if expense.expense_date.startswith(prefix)
        ]

        total = round(sum(expense.amount for expense in matching), 2)
        by_category: dict[str, float] = {}

        for expense in matching:
            by_category[expense.category] = round(
                by_category.get(expense.category, 0) + expense.amount, 2
            )

        return total, by_category

    @staticmethod
    def _validate_date(value: str) -> None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Date must use YYYY-MM-DD format.") from exc
