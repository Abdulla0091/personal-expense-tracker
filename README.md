# 💰 Personal Expense Tracker

[![Python Tests](https://github.com/Abdulla0091/personal-expense-tracker/actions/workflows/tests.yml/badge.svg)](https://github.com/Abdulla0091/personal-expense-tracker/actions/workflows/tests.yml)

A simple and modular **command-line expense tracker** built with Python.

This project was developed as a learning project to practice **Object-Oriented Programming, data persistence, input validation, unit testing, and Git/GitHub workflow**.

---

## 📸 Application Preview

![Personal Expense Tracker](screenshots/app-preview.png)
![alt text](<3Screenshot 2026-08-28 021711.png>) ![alt text](<1Screenshot 2026-08-28 021612.png>) ![alt text](<2Screenshot 2026-08-28 021647.png>)

---

## ✨ Features

* ➕ Add new expenses
* 👀 View all expenses
* 🔎 Search expenses by category, description, or date
* ✏️ Edit existing expenses
* 🗑️ Delete expenses
* 🏷️ Categorize expenses
* 📅 Store expense dates
* 📊 Generate monthly spending summaries
* 📂 Generate category-wise monthly summaries
* 💾 Store data locally using JSON
* 🧪 Automated unit tests
* ✅ Input validation for amount, category, description, and date
* 🔄 Continuous Integration with GitHub Actions

---

## 🛠️ Tech Stack

| Technology                  | Purpose                  |
| --------------------------- | ------------------------ |
| Python 3.10+                | Application development  |
| Object-Oriented Programming | Application architecture |
| JSON                        | Local data persistence   |
| unittest                    | Automated testing        |
| Git                         | Version control          |
| GitHub                      | Source code hosting      |
| GitHub Actions              | Continuous Integration   |

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
├── tests/
│   └── test_expense_manager.py # Unit tests
│
├── data/
│   └── .gitkeep                # Keeps data directory in Git
│
├── screenshots/
│   └── app-preview.png         # Application screenshot
│
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions workflow
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Abdulla0091/personal-expense-tracker.git
```

### 2. Navigate to the Project

```bash
cd personal-expense-tracker
```

### 3. Run the Application

```bash
python src/app.py
```

---

## 🧪 Running Tests

Run the automated unit tests with:

```bash
python -m unittest discover -s tests -v
```

### Test Coverage

The project currently includes **20 automated unit tests** covering:

* Adding expenses
* Incremental expense ID generation
* Updating expenses
* Deleting expenses
* Searching by category
* Searching by description
* Searching by date
* Case-insensitive search
* Monthly summaries
* Empty-month summaries
* Expense lookup
* Invalid amounts
* Empty categories
* Empty descriptions
* Invalid dates
* Non-existing expenses

### Test Result

```text
Ran 20 tests in 0.044s

OK
```

---

## 💾 Data Storage

Expense data is stored locally using **JSON**.

This allows the application to persist expense information between program runs without requiring an external database.

---

## 🔄 Continuous Integration

This project uses **GitHub Actions** to automatically run the Python unit tests whenever changes are pushed or a pull request is opened.

The workflow helps ensure that new changes do not break existing functionality.

**Current status:**

* ✅ 20/20 unit tests passing
* ✅ GitHub Actions passing
* ✅ Pull Request checks enabled

---

## 🎯 Project Goals

This project was created to strengthen practical programming and software engineering skills, including:

* Object-Oriented Programming
* File handling
* JSON data persistence
* Input validation
* Unit testing
* Modular project architecture
* Git & GitHub workflow
* Continuous Integration

---

## 📌 Future Improvements

* 📈 Expense visualization and charts
* 💰 Budget management
* 📊 Advanced financial reports
* 📤 CSV export
* 🗄️ Database support
* 🖥️ Graphical User Interface (GUI)
* 🌐 Web-based version

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Abdulla Al Noman**

Built as a learning project to practice Python development and software engineering fundamentals.
