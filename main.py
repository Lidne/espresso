import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.search.clicked.connect(self.diplay_info)

    def diplay_info(self):
        try:
            search_result = self.get_from_db(self.category.currentText(), self.inp.text())
            if search_result is None:
                raise ValueError
            self.id.setText(str(search_result[0]))
            self.sort.setText(str(search_result[1]))
            self.roast.setText(str(search_result[2]))
            if search_result[3]:
                self.kind.setText('в зёрнах')
            else:
                self.kind.setText('молотый')
            self.taste.setText(str(search_result[4]))
            self.value.setText(str(search_result[5]))
            self.volume.setText(str(search_result[6]))
        except Exception:
            self.log.setText('Нет данных по этому запросу')

    def get_from_db(self, category, item):
        cur = self.con.cursor()
        if category == 'Название сорта':
            category = 'sort'
        elif category == 'Степень обжарки':
            category = 'roast'
        elif category == 'Вид(молотый/взёрнах)':
            category = 'kind'
        elif category == 'Описание вкуса':
            category = 'taste'
        elif category == 'Цена':
            category = 'value'
        elif category == 'Объём упаковки':
            category = 'volume'
        res = cur.execute("""SELECT id, sort, roast, kind, taste, value, volume FROM coffee
        WHERE {}='{}'""".format(category, item)).fetchone()
        return res


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    es = Espresso()
    es.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
