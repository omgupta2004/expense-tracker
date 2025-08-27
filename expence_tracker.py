import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTableView, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QDateEdit, QTextEdit, QTabWidget,
    QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QDate
from PyQt6.QtGui import QKeySequence, QShortcut
import psycopg2
from psycopg2 import sql
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from datetime import datetime

# Database connection parameters - Change according to your setup
DB_HOST = "localhost"
DB_NAME = "expense_db"
DB_USER = "postgres"
DB_PASS = "@Omgupta2004"

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cur = conn.cursor()

# Model for expenses (simplified)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Advanced Expense Tracker")
        self.resize(1000, 700)

        self._create_db_connection()
        self._create_widgets()
        self._populate_categories()
        self._connect_signals()
        self.load_expenses()
        self.plot_analytics()
        self.dark_mode_enabled = False
        
    def _create_db_connection(self):
        # Using psycopg2 connection for direct queries, 
        # for Qt model we can consider QSqlDatabase but keep using psycopg2 for control here.
        pass

    def _create_widgets(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.central_widget.setLayout(layout)

        # -- Expenses Tab --
        self.expense_tab = QWidget()
        self.tabs.addTab(self.expense_tab, "Expenses")
        self._setup_expense_tab()

        # -- Categories Tab --
        self.category_tab = QWidget()
        self.tabs.addTab(self.category_tab, "Categories")
        self._setup_category_tab()

        # -- Analytics Tab --
        self.analytics_tab = QWidget()
        self.tabs.addTab(self.analytics_tab, "Analytics")
        self._setup_analytics_tab()

        # -- Theme checkbox --
        self.theme_checkbox = QCheckBox("Dark Mode")
        layout.addWidget(self.theme_checkbox)
        self.theme_checkbox.stateChanged.connect(self.toggle_theme)

        # Keyboard Shortcuts
        QShortcut(QKeySequence("Ctrl+N"), self, activated=self.clear_expense_form)
        QShortcut(QKeySequence("Ctrl+D"), self, activated=self.delete_selected_expense)

    def _setup_expense_tab(self):
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        # Amount
        form_layout.addWidget(QLabel("Amount:"))
        self.amount_input = QLineEdit()
        form_layout.addWidget(self.amount_input)

        # Category
        form_layout.addWidget(QLabel("Category:"))
        self.category_combobox = QComboBox()
        form_layout.addWidget(self.category_combobox)

        # Date
        form_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        form_layout.addWidget(self.date_edit)

        # Note
        form_layout.addWidget(QLabel("Note:"))
        self.note_input = QLineEdit()
        form_layout.addWidget(self.note_input)

        # Add button
        self.add_expense_button = QPushButton("Add Expense")
        self.add_expense_button.setShortcut("Return")  # Enter key activates add
        form_layout.addWidget(self.add_expense_button)

        layout.addLayout(form_layout)

        # Filter Layout
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by Category:"))
        self.filter_category = QComboBox()
        filter_layout.addWidget(self.filter_category)

        filter_layout.addWidget(QLabel("Filter by Date From:"))
        self.filter_date_from = QDateEdit(calendarPopup=True)
        self.filter_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.filter_date_from.setDisplayFormat("yyyy-MM-dd")
        filter_layout.addWidget(self.filter_date_from)

        filter_layout.addWidget(QLabel("To:"))
        self.filter_date_to = QDateEdit(calendarPopup=True)
        self.filter_date_to.setDate(QDate.currentDate())
        self.filter_date_to.setDisplayFormat("yyyy-MM-dd")
        filter_layout.addWidget(self.filter_date_to)

        self.filter_text = QLineEdit()
        self.filter_text.setPlaceholderText("Search notes...")
        filter_layout.addWidget(self.filter_text)

        self.clear_filter_button = QPushButton("Clear Filters")
        filter_layout.addWidget(self.clear_filter_button)

        layout.addLayout(filter_layout)

        # Expense table
        self.expense_table = QTableView()
        layout.addWidget(self.expense_table)

        # Delete Button
        self.delete_expense_button = QPushButton("Delete Selected Expense")
        layout.addWidget(self.delete_expense_button)

        self.expense_tab.setLayout(layout)

    def _setup_category_tab(self):
        layout = QVBoxLayout()
        form = QHBoxLayout()

        self.new_category_input = QLineEdit()
        self.new_category_input.setPlaceholderText("New category name")
        form.addWidget(self.new_category_input)

        self.add_category_button = QPushButton("Add Category")
        form.addWidget(self.add_category_button)
        self.delete_category_button = QPushButton("Delete Selected Category")
        form.addWidget(self.delete_category_button)

        layout.addLayout(form)

        self.category_table = QTableView()
        layout.addWidget(self.category_table)

        self.category_tab.setLayout(layout)

    def _setup_analytics_tab(self):
        layout = QVBoxLayout()
        self.fig = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.analytics_tab.setLayout(layout)

    def _connect_signals(self):
        self.add_expense_button.clicked.connect(self.add_expense)
        self.delete_expense_button.clicked.connect(self.delete_selected_expense)
        self.add_category_button.clicked.connect(self.add_category)
        self.delete_category_button.clicked.connect(self.delete_selected_category)
        self.clear_filter_button.clicked.connect(self.clear_filters)
        self.filter_category.currentIndexChanged.connect(self.apply_filters)
        self.filter_date_from.dateChanged.connect(self.apply_filters)
        self.filter_date_to.dateChanged.connect(self.apply_filters)
        self.filter_text.textChanged.connect(self.apply_filters)

    def _execute_query(self, query, params=None):
        try:
            cur.execute(query, params or ())
            conn.commit()
            return cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            return []

    def _populate_categories(self):
        categories = ["All"] + [row[0] for row in self._execute_query("SELECT name FROM categories ORDER BY name")]
        self.category_combobox.clear()
        self.category_combobox.addItems(categories[1:])
        
        self.filter_category.clear()
        self.filter_category.addItems(categories)

    def load_expenses(self):
        expenses = self._execute_query("""
            SELECT e.id, e.amount, c.name, e.date, e.note
            FROM expenses e JOIN categories c ON e.category_id = c.id
            ORDER BY e.date DESC
        """)

        self.expense_model = ExpenseTableModel(expenses)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.expense_model)
        self.expense_table.setModel(self.proxy_model)
        self.expense_table.resizeColumnsToContents()
        
    def add_expense(self):
        try:
            amount = float(self.amount_input.text())
            category = self.category_combobox.currentText()
            date = self.date_edit.date().toPyDate()
            note = self.note_input.text()

            # Get category_id
            res = self._execute_query("SELECT id FROM categories WHERE name = %s", (category,))
            if not res:
                QMessageBox.warning(self, "Input error", "Invalid category.")
                return
            category_id = res[0][0]

            cur.execute("INSERT INTO expenses (amount, category_id, date, note) VALUES (%s, %s, %s, %s)", (amount, category_id, date, note))
            conn.commit()
            QMessageBox.information(self, "Success", "Expense added.")
            self.load_expenses()
            self.plot_analytics()
            self.clear_expense_form()
        except ValueError:
            QMessageBox.warning(self, "Input error", "Please enter a valid amount.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_expense_form(self):
        self.amount_input.clear()
        self.note_input.clear()
        self.date_edit.setDate(QDate.currentDate())
        if self.category_combobox.count() > 0:
            self.category_combobox.setCurrentIndex(0)

    def delete_selected_expense(self):
        selection = self.expense_table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(self, "Selection error", "Select at least one expense to delete.")
            return
        for idx in selection:
            expense_id = self.proxy_model.data(self.proxy_model.index(idx.row(), 0))
            cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        conn.commit()
        self.load_expenses()
        self.plot_analytics()
        QMessageBox.information(self, "Deleted", "Selected expenses deleted.")

    def add_category(self):
        new_cat = self.new_category_input.text().strip()
        if not new_cat:
            QMessageBox.warning(self, "Input Error", "Enter a category name.")
            return
        try:
            cur.execute("INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING", (new_cat,))
            conn.commit()
            self.new_category_input.clear()
            self._populate_categories()
            self.load_expenses()
            self.load_categories_table()
        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))

    def delete_selected_category(self):
        selection = self.category_table.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(self, "Selection error", "Select a category to delete.")
            return
        for idx in selection:
            cat_id = self.category_model.data(self.category_model.index(idx.row(), 0))
            try:
                cur.execute("DELETE FROM categories WHERE id = %s", (cat_id,))
                conn.commit()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        self._populate_categories()
        self.load_expenses()
        self.load_categories_table()

    def load_categories_table(self):
        categories = self._execute_query("SELECT id, name FROM categories ORDER BY name")
        self.category_model = CategoryTableModel(categories)
        self.category_table.setModel(self.category_model)
        self.category_table.resizeColumnsToContents()

    def apply_filters(self):
        cat_filter = self.filter_category.currentText()
        date_from = self.filter_date_from.date().toPyDate()
        date_to = self.filter_date_to.date().toPyDate()
        note_filter = self.filter_text.text().lower()

        def filter_accepts(row):
            _, amount, category, date, note = row
            if cat_filter != "All" and category != cat_filter:
                return False
            if not (date_from <= date <= date_to):
                return False
            if note_filter and note_filter not in note.lower():
                return False
            return True

        filtered = filter(filter_accepts, self.expense_model.expenses)
        self.proxy_model = ExpenseTableModel(list(filtered))
        self.expense_table.setModel(self.proxy_model)
        self.expense_table.resizeColumnsToContents()

    def clear_filters(self):
        self.filter_category.setCurrentIndex(0)
        self.filter_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.filter_date_to.setDate(QDate.currentDate())
        self.filter_text.clear()
        self.load_expenses()

    def plot_analytics(self):
        self.fig.clear()

        ax1 = self.fig.add_subplot(121)
        cur.execute("""
            SELECT c.name, SUM(e.amount) FROM expenses e
            JOIN categories c ON e.category_id = c.id
            GROUP BY c.name
        """)
        data = cur.fetchall()
        if data:
            cats, amounts = zip(*data)
            ax1.pie(amounts, labels=cats, autopct='%1.1f%%', startangle=140)
            ax1.set_title("Expense by Category")
        else:
            ax1.text(0.5, 0.5, "No data", ha='center', va='center')

        ax2 = self.fig.add_subplot(122)
        cur.execute("""
            SELECT date, SUM(amount) FROM expenses
            WHERE date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY date ORDER BY date
        """)
        data = cur.fetchall()
        if data:
            dates, amounts = zip(*data)
            dates = [d.strftime("%m-%d") for d in dates]
            ax2.bar(dates, amounts)
            ax2.set_title("Last 30 Days Expenses")
            ax2.tick_params(axis='x', rotation=45)
        else:
            ax2.text(0.5, 0.5, "No data", ha='center', va='center')

        self.canvas.draw()

    def toggle_theme(self, state):
        if state == Qt.CheckState.Checked:
            self.setStyleSheet("QWidget { background-color: #2b2b2b; color: #f0f0f0; }")
            self.dark_mode_enabled = True
        else:
            self.setStyleSheet("")
            self.dark_mode_enabled = False

# Table Models
from PyQt6.QtCore import QAbstractTableModel, QVariant

class ExpenseTableModel(QAbstractTableModel):
    def __init__(self, expenses=None):
        super().__init__()
        self.headers = ["ID", "Amount", "Category", "Date", "Note"]
        self.expenses = expenses or []

    def rowCount(self, parent=None):
        return len(self.expenses)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.expenses[index.row()][index.column()])
        return QVariant()

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return QVariant()

class CategoryTableModel(QAbstractTableModel):
    def __init__(self, categories=None):
        super().__init__()
        self.headers = ["ID", "Category Name"]
        self.categories = categories or []

    def rowCount(self, parent=None):
        return len(self.categories)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self.categories[index.row()][index.column()])
        return QVariant()

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return QVariant()

# Main
def main():
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
