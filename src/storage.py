import json
from pathlib import Path

from models import Expense


class JSONStorage:
    """Persists expenses in a JSON file."""

    def __init__(self, file_path: str = "data/expenses.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[Expense]:
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                raw_data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

        return [Expense.from_dict(item) for item in raw_data]

    def save(self, expenses: list[Expense]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                [expense.to_dict() for expense in expenses],
                file,
                indent=4,
                ensure_ascii=False,
            )


class BudgetStorage:
    """Persists monthly budgets in a JSON file."""

    def __init__(self, file_path: str = "data/budgets.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, float]:
        if not self.file_path.exists():
            return {}

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                raw_data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

        if not isinstance(raw_data, dict):
            return {}

        return {
            str(key): float(value)
            for key, value in raw_data.items()
        }

    def save(self, budgets: dict[str, float]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                budgets,
                file,
                indent=4,
                ensure_ascii=False,
            )