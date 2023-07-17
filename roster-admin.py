import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QVBoxLayout, QWidget, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtGui import QBrush, QColor, QFont

names = ['NSW-1', 'NSW-2', 'NSW-3', 'NSW-4', 'NSW-5', 'NSW-6', 
         'QLD-1', 'QLD-2',
         'REM-1', 'REM-2', 'REM-3', 'REM-4', 'REM-5', 'REM-6']

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.months_dropdown = QComboBox()
        self.months_dropdown.addItems(months)
        self.update_roster_button = QPushButton('Update Roster')
        
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.months_dropdown)
        toolbar_layout.addWidget(self.update_roster_button)

        self.table = QTableWidget()
        self.table.setRowCount(len(names))
        self.table.setColumnCount(31)
        self.table.horizontalHeader().setDefaultSectionSize(30)
        self.table.verticalHeader().setDefaultSectionSize(30)

        headers = [str(i) for i in range(1, 32)]
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setVerticalHeaderLabels(names)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet("QTableWidget::item { padding: 0px; }")

        self.setup_table()

        layout = QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Interactive Grid')
        self.setFixedSize(1100, 550)

        self.load_month_files()
        self.months_dropdown.currentIndexChanged.connect(self.load_table)
        self.load_table(0)  
        self.update_roster_button.clicked.connect(self.update_roster_file)
    
    def load_json_file(self, index):
        filepath = f'roster/{index}.json'
        with open(filepath, 'r') as f:
            self.month_data[index] = json.load(f)

    def load_month_files(self):
        self.month_data = {}
        for i in range(1, 13):
            filepath = f'roster/{i}.json'
            if not os.path.exists(filepath):
                month_data = {"month": months[i-1]}
                month_data.update({str(day): {name: 0 for name in names} for day in range(1, 32)})
                with open(filepath, 'w') as f:
                    json.dump(month_data, f)
            self.load_json_file(i)

    def load_table(self, month_index):
        month_index += 1 
        shift_colors = [QColor('white'), QColor('green'), QColor('orange'), QColor('purple')]
        month_data = self.month_data[month_index]
        for day, staff in month_data.items():
            if day == "month":
                continue
            for i, name in enumerate(names):
                shift = staff[name]
                cell = self.table.item(i, int(day)-1)
                cell.setBackground(shift_colors[shift])

    def setup_table(self):
        for i in range(len(names)):
            for j in range(31):
                cell = QTableWidgetItem()
                cell.setFlags(cell.flags() ^ 32)  
                cell.setBackground(QBrush(QColor('white')))
                cell.setFont(QFont("Arial", 10, QFont.Bold))
                self.table.setItem(i, j, cell)
        self.table.cellClicked.connect(self.change_color)

    def change_color(self, row, column):
        cell = self.table.item(row, column)
        current_state = cell.background().color()
        next_state = self.get_next_state(current_state)
        cell.setBackground(next_state)

    def get_next_state(self, current_state):
        colours = [QColor('white'), QColor('green'), QColor('orange'), QColor('purple')]
        current_index = colours.index(current_state)
        next_index = (current_index + 1) % 4
        next_state = colours[next_index]
        return next_state

    def update_roster_file(self):
        month_index = self.months_dropdown.currentIndex() + 1
        filepath = f'roster/{month_index}.json'
        shift_colors = [QColor('white'), QColor('green'), QColor('orange'), QColor('purple')]
        month_data = {'month': months[month_index-1]}
        for j in range(1, 32):
            day_data = {}
            for i, name in enumerate(names):
                cell = self.table.item(i, j-1)
                if cell is not None:
                    color = shift_colors.index(cell.background().color())
                    day_data[name] = color
            month_data[str(j)] = day_data
        with open(filepath, 'w') as f:
            json.dump(month_data, f)
        self.load_json_file(month_index)


def main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
