# Expense Tracker Project

## Project Overview
This is a Python web application built with **Flask** that allows users to track their expenses. It uses **SQLAlchemy** as an ORM to interact with a **SQLite** database. Users can add, view, edit, and delete expenses.

## Technology Stack
- **Language:** Python
- **Web Framework:** Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Testing:** pytest

## Project Structure
```text
D:\edu\Training\2026\gemini_code_assist\expense_tracker_project\
├── app.py              # Main Flask application entry point and routes
├── models.py           # Database models (SQLAlchemy)
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates (Jinja2)
│   ├── base.html       # Base template with common layout
│   ├── index.html      # Dashboard/List view
│   └── form.html       # Add/Edit expense form
├── static/             # Static files (CSS, JS, images)
└── tests/              # Unit tests
    └── test_app.py     # Tests for application routes and logic
```

## Setup and Installation

1.  **Install Dependencies:**
    Ensure you have Python installed. It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the Server:**
    Run the application using Python. This will start the Flask development server (debug mode is enabled by default).
    ```bash
    python app.py
    ```
    
2.  **Access the App:**
    Open your browser and navigate to: `http://127.0.0.1:5000`

    *Note: The database (`instance/expenses.db`) is automatically initialized on the first run.*

## Running Tests

The project uses `pytest` for testing.

1.  **Run All Tests:**
    ```bash
    pytest
    ```

## Development Conventions

-   **Code Style:** Follow standard Python PEP 8 guidelines.
-   **Database:** The `Expense` model is defined in `models.py`. Changes to models may require database migrations or recreating the database (currently `db.create_all()` is used in `app.py`, which creates tables if they don't exist).
-   **Testing:** New features should include corresponding tests in the `tests/` directory. Tests use an in-memory SQLite database to ensure isolation.
