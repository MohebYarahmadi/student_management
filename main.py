#!/usr/bin/env python3
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem
from PyQt6.QtGui import QAction
import sqlite3

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")\

        # Create Menubar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add submenu for each menubar
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About Manager", self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole) # Fix Some Mac Issue

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


def main():
    app = QApplication(sys.argv)
    manager = MainWindow()
    manager.show()
    manager.load_data()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
