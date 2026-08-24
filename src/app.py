from datetime import date

from expense_manager import ExpenseManager
from storage import JSONStorage


def print_header(title: str) -> None:
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def print_expenses(expenses) -> None:
    if not expenses:
        print("No expenses found.")
        return

    print(f"\n{'ID':<5}{'Date':<13}{'Category':<16}{'Amount':>10}  Description")
    print("-" * 75)

    for expense in expenses:
        print(
            f"{expense.id:<5}"
            f"{expense.expense_date:<13}"
            f"{expense.category:<16}"
            f"{expense.amount:>10.2f}  "
            f"{expense.description}"
        )


def add_expense(manager: ExpenseManager) -> None:
    print_header("Add Expense")

    try:
        amount = float(input("Amount: ").strip())
        category = input("Category: ").strip()
        description = input("Description: ").strip()
        expense_date = input(
            f"Date [YYYY-MM-DD, default {date.today().isoformat()}]: "
        ).strip() or None

        expense = manager.add_expense(
            amount,
            category,
            description,
            expense_date,
        )
        print(f"\nExpense #{expense.id} added successfully.")

    except ValueError as error:
        print(f"\nError: {error}")


def view_expenses(manager: ExpenseManager) -> None:
    print_header("All Expenses")
    print_expenses(manager.get_all())


def delete_expense(manager: ExpenseManager) -> None:
    print_header("Delete Expense")

    try:
        expense_id = int(input("Expense ID: ").strip())
        if manager.delete_expense(expense_id):
            print("Expense deleted successfully.")
        else:
            print("Expense not found.")
    except ValueError:
        print("Please enter a valid numeric ID.")


def search_expenses(manager: ExpenseManager) -> None:
    print_header("Search Expenses")
    keyword = input("Search keyword: ").strip()
    print_expenses(manager.search(keyword))


def monthly_summary(manager: ExpenseManager) -> None:
    print_header("Monthly Summary")

    try:
        year = int(input("Year: ").strip())
        month = int(input("Month (1-12): ").strip())

        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12.")

        total, by_category = manager.monthly_summary(year, month)

        print(f"\nTotal spending: {total:.2f}")

        if by_category:
            print("\nBy category:")
            for category, amount in sorted(by_category.items()):
                print(f"- {category}: {amount:.2f}")
        else:
            print("No expenses found for this month.")

    except ValueError as error:
        print(f"Error: {error}")


def main() -> None:
    manager = ExpenseManager(JSONStorage())

    while True:
        print_header("Personal Expense Tracker")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Search expenses")
        print("4. Monthly summary")
        print("5. Delete expense")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        actions = {
            "1": add_expense,
            "2": view_expenses,
            "3": search_expenses,
            "4": monthly_summary,
            "5": delete_expense,
        }

        if choice == "0":
            print("\nGoodbye!")
            break

        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("\nInvalid option. Please choose from the menu.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
