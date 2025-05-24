#!/usr/bin/env python3
from PyQt6.QtWidgets import QApplication, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton

import sys
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        # Create widgets
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_label = QLabel("Date of Birth MM/DD/YYY:")
        self.date_line_edit = QLineEdit()

        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.calculate_age)
        self.output_lbl = QLabel("")

        # Add widgets to grid
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)
        grid.addWidget(calc_btn, 2, 0, 1, 2)
        grid.addWidget(self.output_lbl, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        cur_year = datetime.now().year
        date_of_birth = self.date_line_edit.text()
        year_of_birth = datetime.strptime(
            date_of_birth, "%m/%d/%Y").date().year
        age = cur_year - year_of_birth
        self.output_lbl.setText(
            f"{self.name_line_edit.text()} is {age} years old."
        )


def main():
    app = QApplication(sys.argv)
    age_cal = AgeCalculator()
    age_cal.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
