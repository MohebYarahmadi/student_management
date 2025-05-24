#!/usr/bin/env python3
from PyQt6.QtWidgets import QApplication, QComboBox, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton

import sys


class CalculateSpeed(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speed Calculator")
        grid = QGridLayout()

        # Create widgets
        dis_lbl = QLabel("Distance:")
        self.dis_line_edit = QLineEdit()
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(['Metric (km)', 'Imperial (miles)'])
        time_lbl = QLabel("Time (h):")
        self.time_line_edit = QLineEdit()
        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.calculate)
        self.output_lbl = QLabel("")

        # Add widgets to grid
        grid.addWidget(dis_lbl, 0, 0)
        grid.addWidget(self.dis_line_edit, 0, 1)
        grid.addWidget(self.unit_combo, 0, 2)
        grid.addWidget(time_lbl, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calc_btn, 2, 0, 1, 3)
        grid.addWidget(self.output_lbl, 3, 0, 1, 3)

        self.setLayout(grid)

    def calculate(self):
        distance = float(self.dis_line_edit.text())
        time = float(self.time_line_edit.text())

        speed = distance / time
        
        if self.unit_combo.currentText() == 'Metric (km)':
            speed = round(speed, 2)
            unit = 'km/h'
        if self.unit_combo.currentText() == 'Imperial (miles)':
            speed = round(speed * 0.621371, 2)
            unit = 'mph'

        self.output_lbl.setText(
            f"Average Speed: {speed} {unit}"
        )


def main():
    app = QApplication(sys.argv)
    calc_speed = CalculateSpeed()
    calc_speed.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
