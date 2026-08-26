# 💰 Personal Expense Tracker

A simple and modular **command-line expense tracker** built with Python.

This project was developed as a learning project to practice **Object-Oriented Programming, data persistence, input validation, unit testing, and Git/GitHub workflow**.

---

## ✨ Features

- ➕ Add new expenses
- 👀 View all expenses
- 🔎 Search expenses by category, description, or date
- ✏️ Edit existing expenses
- 🗑️ Delete expenses
- 🏷️ Categorize expenses
- 📅 Store expense dates
- 📊 Generate monthly spending summaries
- 📂 Generate category-wise monthly summaries
- 💾 Store data locally using JSON
- 🧪 Automated unit tests
- ✅ Input validation for amount, category, description, and date

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Application development |
| OOP | Application architecture |
| JSON | Local data persistence |
| unittest | Automated testing |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📁 Project Structure

```text
personal-expense-tracker/
│
├── src/
│   ├── app.py                  # Command-line interface
│   ├── expense_manager.py      # Business logic
│   ├── models.py               # Expense data model
│   └── storage.py              # JSON storage layer
│
├── data/
│   └── .gitkeep                # Keeps data directory in Git
│
├── tests/
│   └── test_expense_manager.py # Unit tests
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt