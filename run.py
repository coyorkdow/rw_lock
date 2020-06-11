from PyQt5.QtCore import QMetaObject, pyqtSlot
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QApplication, QStackedWidget)

from gui import MainWindow
from simulation import Simulation, DrawThread, mutex


class Main(QWidget):

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

        self.stack = QStackedWidget()

        self.threads = []

        self.mainWin = MainWindow()
        self.simulation = Simulation()

        self.stack.addWidget(self.mainWin)
        self.stack.addWidget(self.simulation)

        main_layout = QVBoxLayout()
        button_box = QHBoxLayout()

        self.mainWinBtn = QPushButton()
        self.mainWinBtn.setText('implementation')
        self.mainWinBtn.setObjectName('implementation')
        self.simulationBtn = QPushButton()
        self.simulationBtn.setText('simulation')
        self.simulationBtn.setObjectName('simulation')
        self.simulationBtn.setFixedWidth(130)
        self.mainWinBtn.setFixedWidth(130)

        button_box.addWidget(self.mainWinBtn)
        button_box.addStretch(6)
        button_box.addWidget(self.simulationBtn)

        main_layout.addLayout(button_box)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)
        QMetaObject.connectSlotsByName(self)
        self.show()

    @pyqtSlot()
    def on_implementation_clicked(self):
        self.stack.setCurrentIndex(0)

    @pyqtSlot()
    def on_simulation_clicked(self):
        self.simulation.box.itemAt(0).widget().clear()
        self.threads.append(DrawThread())
        self.threads[-1].signal.connect(self.setPlot)
        self.threads[-1].start()
        self.stack.setCurrentIndex(1)

    def setPlot(self):
        self.simulation.box.itemAt(0).widget().reDraw()
        self.simulation.update()
        mutex.unlock()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Main()
    win.setWindowTitle('read&write problem')
    win.show()
    app.exec_()
