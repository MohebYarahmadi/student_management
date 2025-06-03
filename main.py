#!/usr/bin/env python3
# Moheb Yarahmadi
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, \
    QGridLayout, QMainWindow, QLabel, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox, QToolBar, \
    QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon

import sys
import sqlite3


class Database:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")
        self.setMinimumSize(400, 400)
        # self.setFixedWidth(600)
        # self.setFixedHeight(400)

        # Create Menubar
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add submenu for each menubar
        add_student_action = QAction(
            QIcon('icons/add.png'),
            "Add Student",
            self
        )
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_action = QAction(
            QIcon('icons/search.png'),
            "Find Student",
            self
        )
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        about_action = QAction("About Manager", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)
        # Fix Some Mac Issue
        # about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Table area
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("Id", "Name", "Course", "Mobile")
        )
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add elements to toolbar
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Add elements to status bar
        # First we need to detect a cell selection
        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        connection = Database().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(
                    row_number,
                    column_number,
                    QTableWidgetItem(str(data))
                )
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def cell_clicked(self):
        edit_btn = QPushButton("Edit Record")
        edit_btn.clicked.connect(self.edit)
        delete_btn = QPushButton("Delete Record")
        delete_btn.clicked.connect(self.delete)

        # Cleanup old btns added before
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Abb btns for selecter cell
        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(delete_btn)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert New Record")
        self.setFixedWidth(200)
        self.setFixedHeight(300)

        layout = QVBoxLayout()  # Select layout, you can use Grid too

        # Create and add name_input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

        # Create and add courses combobox
        self.course_select = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_select.addItems(courses)
        layout.addWidget(self.course_select)

        # Create and add phone_input
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        layout.addWidget(self.phone_input)

        # Create and add insert_btn
        insert_btn = QPushButton("Insert")
        insert_btn.clicked.connect(self.insert_record)
        layout.addWidget(insert_btn)

        self.setLayout(layout)  # Set the layout

    def insert_record(self):
        name = self.name_input.text()
        course = self.course_select.itemText(self.course_select.currentIndex())
        mobile = self.phone_input.text()
        connection = Database().connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?,?,?)",
            (name, course, mobile)
        )
        connection.commit()
        cursor.close()
        connection.close()
        manager.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search")
        self.setFixedWidth(200)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for:")
        layout.addWidget(self.search_input)

        search_btn = QPushButton("Find")
        search_btn.clicked.connect(self.find)
        layout.addWidget(search_btn)

        self.setLayout(layout)

    def find(self):
        name = self.search_input.text()
        connection = Database().connect()
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM students WHERE name = ?",
            (name,)
        )
        rows = list(result)
        print(rows)
        items = manager.table.findItems(
            name,
            Qt.MatchFlag.MatchFixedString
        )
        for item in items:
            print(item)
            manager.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedWidth(250)
        self.setFixedHeight(100)

        layout = QVBoxLayout()

        about_text = QLabel("Designed by Moheb Yarahmadi")
        layout.addWidget(about_text)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Record")
        self.setFixedWidth(200)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get selected row information
        index = manager.table.currentRow()
        self.student_id = manager.table.item(index, 0).text()   # Id
        student_name = manager.table.item(index, 1).text()  # Name
        course_name = manager.table.item(index, 2).text()  # Course
        phone_number = manager.table.item(index, 3).text()  # Phone

        # Create and add name_input
        self.name_input = QLineEdit(student_name)
        layout.addWidget(self.name_input)

        # Create and add courses combobox
        self.course_select = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_select.addItems(courses)
        self.course_select.setCurrentText(course_name)
        layout.addWidget(self.course_select)

        # Create and add phone_input
        self.phone_input = QLineEdit(phone_number)
        layout.addWidget(self.phone_input)

        # Create and add insert_btn
        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.edit_record)
        layout.addWidget(update_btn)

        self.setLayout(layout)  # Set the layout

    def edit_record(self):
        name = self.name_input.text()
        course = self.course_select.itemText(self.course_select.currentIndex())
        mobile = self.phone_input.text()
        connection = Database().connect()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
            (name, course, mobile, self.student_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        manager.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Record")
        self.setFixedWidth(200)
        self.setFixedHeight(70)

        layout = QGridLayout()

        confirmation = QLabel("Are you sure to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        yes.clicked.connect(self.delete_record)
        no.clicked.connect(self.close)

        self.setLayout(layout)

    def delete_record(self):
        index = manager.table.currentRow()
        student_id = manager.table.item(index, 0).text()

        connection = Database().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        manager.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was deleted.")
        confirmation_widget.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = MainWindow()
    manager.show()
    manager.load_data()
    sys.exit(app.exec())
