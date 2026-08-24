from dataclasses import dataclass
from datetime import date


@dataclass
class Expense:
    """Represents a single expense."""

    id: int
    amount: float
    category: str
    description: str
    expense_date: str

    @classmethod
    def create(cls, expense_id: int, amount: float, category: str,
               description: str, expense_date: str | None = None) -> "Expense":
        return cls(
            id=expense_id,
            amount=round(amount, 2),
            category=category.strip().title(),
            description=description.strip(),
            expense_date=expense_date or date.today().isoformat(),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "expense_date": self.expense_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            id=int(data["id"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            description=str(data["description"]),
            expense_date=str(data["expense_date"]),
        )
