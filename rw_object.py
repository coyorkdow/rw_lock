from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QLabel, QSizePolicy)


class ReaderObject(QLabel):
    def __init__(self, id):
        super(ReaderObject, self).__init__()
        self.id = id
        self.setStyleSheet("QLabel { font:20pt; background-color: #00f260; color: white; border: 2px}")
        self.setAlignment(Qt.AlignCenter)
        self.setText(str(id))
        self.setFixedWidth(40)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))


class WriterObject(QLabel):
    signal = pyqtSignal(str, str)

    def __init__(self, id, text=None):
        super(WriterObject, self).__init__()
        self.id = id
        self.setStyleSheet("QLabel { font:20pt; background-color: #00f260; color: white; border: 2px}")
        self.setAlignment(Qt.AlignCenter)
        self.setText(str(id))
        self.setFixedWidth(40)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))
        self.push = False
        self.setMouseTracking(True)
        self._text = text

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.push = True

    def mouseReleaseEvent(self, event):
        if self.push:
            self.push = False
            self.signal.emit(self._text, self.id)
