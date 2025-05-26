#!/usr/bin/env python3
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, \
    QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QAction

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

        

def main():
    app = QApplication(sys.argv)
    manager = MainWindow()
    manager.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
