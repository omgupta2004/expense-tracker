# Advanced Expense Tracker (PyQt6)

## Project Overview

The **Advanced Expense Tracker** is a standalone desktop application developed using **Python 3** and **PyQt6**. It provides comprehensive expense management with dynamic categories, date selection, filtering, sorting, and detailed analytics visualizations. The app integrates a **PostgreSQL** backend to securely persist user financial data.

Designed to help individuals or small businesses monitor and analyze their spending habits efficiently, this application boasts a modern multi-tab interface, live search and filtering capabilities, and an intuitive calendar widget for date inputs. Users can visualize spending distributions and trends via interactive charts, enabling smarter budgeting decisions.

***

## Key Features

### Expense Management
- Easily add new expenses specifying amount, category (selectable from managed lists), date (via calendar picker), and optional notes.  
- View expenses in a sortable and filterable table enabling quick access and editing capabilities.  
- Efficiently delete one or multiple selected expense records from the list.

### Category Management
- Dynamically add and delete expense categories, allowing personalized grouping of expenses.  
- Categories are stored and retrieved from PostgreSQL to maintain consistency.

### Filtering and Searching
- Filter expense records by category, date range, and keywords in notes with instant updates.  
- Clear all filters via a single click for full expense data retrieval.

### Data Visualization Analytics
- Pie chart showing percentage distribution of expenses across categories.  
- Bar chart illustrating expense trends over the past 30 days with daily aggregation.  
- Charts update dynamically as expense data changes.

### User Interface and Experience
- Multi-tab layout using Qt’s tab widget for clear separation of expenses, categories, and analytics.  
- Calendar popup widget for effortless date entry minimizing manual input errors.  
- Light and Dark mode toggling for comfortable usage in various ambient lighting.  
- Keyboard shortcuts (`Ctrl + N` for clearing form, `Ctrl + D` for deleting selected entries) speed up common operations.

***

## Technology Stack

- **Programming Language:** Python 3.9+  
- **GUI Framework:** PyQt6  
- **Database:** PostgreSQL  
- **ORM / DB Driver:** psycopg2  
- **Visualization:** Matplotlib  
- **Environment:** Cross-platform (Windows, macOS, Linux)

***

## Installation & Setup Guide

### Prerequisites

1. **Python 3 installation**  
   Ensure Python 3.9 or later is installed. Download from [python.org](https://www.python.org/downloads/) if needed.

2. **PostgreSQL Installation**  
   Install PostgreSQL server and create a user with password and a database (e.g., `expense_db`).  
   Refer to [PostgreSQL’s official site](https://www.postgresql.org/download/) for installation.

3. **Python Dependencies**  
   Open a terminal or command prompt and run:

   ```bash
   pip install PyQt6 psycopg2 matplotlib
   ```

### Database Setup

Launch `psql` or pgAdmin and execute the following commands:

```sql
CREATE DATABASE expense_db;

-- Connect to the database
\c expense_db

-- Create categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Create expenses table
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    amount NUMERIC(10,2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    date DATE NOT NULL,
    note TEXT
);

-- Insert default categories
INSERT INTO categories (name) VALUES ('Food'), ('Transport'), ('Entertainment'), ('Utilities'), ('Others');
```

### Configure the Application

In `pyqt_expense_tracker.py`, update your database connection settings:

```python
DB_HOST = "localhost"
DB_NAME = "expense_db"
DB_USER = "postgres"
DB_PASS = "********"
```

***

## Running the Application

To start the application, run the main Python script:

```bash
python pyqt_expense_tracker.py
```

The main window will open with separate tabs for managing expenses, categories, and viewing analytics.

***

## Usage Instructions

### Adding an Expense
1. Switch to the **Expenses** tab.  
2. Enter amount, select category from dropdown, choose the date from the calendar popup, and add an optional note.  
3. Click **Add Expense** or press **Enter**. The expense will be added and visible in the table below.

### Managing Categories
1. Switch to the **Categories** tab.  
2. Use the text input and **Add Category** button to insert custom categories.  
3. Select a category in the table to delete it using the **Delete Selected Category** button.

### Filtering Data
- Filter expenses by category, date range, or note keywords with the filter controls above the expenses table.  
- Click **Clear Filters** to reset all filters.

### Analytics
- View dynamic pie and bar charts in the **Analytics** tab reflecting your current expense data.

### UI Enhancements
- Toggle between Light and Dark mode with the checkbox below the tabs.  
- Use keyboard shortcuts for quick actions:  
  - Ctrl + N: Clear expense entry form  
  - Ctrl + D: Delete selected expenses

***

## Troubleshooting

- **Database Connection Issues:** Ensure PostgreSQL server is running, and credentials in the Python file are correct.  
- **Missing Dependencies:** Run `pip install` commands again to ensure all packages are installed.  
- **Permission Errors:** On some OS, you may need to run terminal or IDE with administrator rights to access DB.

***

## Future Improvements

- User login with multi-user expense separation  
- Budget management and alerts  
- Export to CSV/PDF reports  
- AI-powered spending categorization suggestions  
- Responsive web-based frontend for cloud hosting

***

## License

This project is licensed under the MIT License.

***

## Contact & Contribution

For bugs, feature requests, or contributions, please contact:  
**Om Gupta** — omgupta200304@gmail.com
