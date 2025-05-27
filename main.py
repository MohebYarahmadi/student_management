#!/usr/bin/env python3
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction

import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")
        self.setFixedWidth(600)
        self.setFixedHeight(400)

        # Create Menubar
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add submenu for each menubar
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_for_record = QAction("Find Student", self)
        search_for_record.triggered.connect(self.search)
        edit_menu_item.addAction(search_for_record)

        about_action = QAction("About Manager", self)
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

    def load_data(self):
        connection = sqlite3.connect("database.db")
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
        connection = sqlite3.connect('database.db')
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
        print("find the record")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = MainWindow()
    manager.show()
    manager.load_data()
    sys.exit(app.exec())
