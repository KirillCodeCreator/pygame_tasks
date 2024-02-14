import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [650, 450]
scale = 10


class Map(QWidget):

    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def keyPressEvent(self, event):
        global scale
        if event.key() == Qt.Key_PageDown:
            if scale < 21:
                scale += 1
            self.update()
        if event.key() == Qt.Key_PageUp:
            if scale > 0:
                scale -= 1
            self.update()

    def update(self):
        self.getImage()
        self.image.clear()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&z={scale}&size={SCREEN_SIZE[0]},{SCREEN_SIZE[1]}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Большая задача по Maps API. Часть №2')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(SCREEN_SIZE[0], SCREEN_SIZE[1])
        self.image.setPixmap(self.pixmap)
        self.setFixedSize(SCREEN_SIZE[0], SCREEN_SIZE[1])

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    map = Map()
    map.show()
    sys.exit(app.exec())
