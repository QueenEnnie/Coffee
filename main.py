import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.roasting = dict()
        self.get_roasting()
        self.ground_or_grains = dict()
        self.get_ground_grains()
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Coffee information")
        self.setMinimumSize(2100, 600)

        self.table_widget.setMinimumSize(2100, 600)

        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки",
                                                     "Молотый/в зёрнах", "Описание вкуса", "Цена",
                                                     "Объем упаковки"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.fill_table()

    def fill_table(self):
        result = self.get_coffee_varities()
        for row, one_film in enumerate(result):
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            for column, elem in enumerate(one_film):
                if column == 2:
                    elem = self.roasting[elem]
                elif column == 3:
                    elem = self.ground_or_grains[elem]
                self.table_widget.setItem(row, column, QTableWidgetItem(str(elem)))

    def get_coffee_varities(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        result = cursor.execute(f"SELECT * from coffee_info").fetchall()
        connection.close()
        return result

    def get_roasting(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        result = cursor.execute(f"SELECT id, degree from roasting_degree").fetchall()
        connection.close()
        for elem in result:
            self.roasting[elem[0]] = elem[1]

    def get_ground_grains(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        result = cursor.execute(f"SELECT id, type from ground_or_grains").fetchall()
        connection.close()
        for elem in result:
            self.ground_or_grains[elem[0]] = elem[1]


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
