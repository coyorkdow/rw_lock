from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QMetaObject, QMutex)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout,
                             QLineEdit, QPushButton, QApplication, QLabel, QPlainTextEdit, QSizePolicy, QDialog)

from rw_lock import Writer, Reader
from rw_object import WriterObject, ReaderObject


class MainWindow(QWidget):
    class Dummy(QLabel):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("QLabel {background-color: #ffffff; color: white; border: 2px}")
            self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainLayout = QVBoxLayout()
        self.setWindowTitle('read&write problem implementation')

        self.readTot = 0
        self.__writerWaitingLock = QMutex()
        self.writeLock = QMutex()
        self.__readerWaitingOrReadingLock = QMutex()
        self.readLocks = {}

        self.writerThreads = []
        self.readerThreads = []

        self.rwStatus = 0  # 0 means none, 1 means read, 2 means write

        resource_box = QVBoxLayout()
        resource_info_box = QHBoxLayout()
        self.rwTips = QLabel('there are neither readers nor writers')
        self.operateRWButton = QPushButton()
        self.operateRWButton.setObjectName('operateRW')
        self.operateRWButton.setText('remove reader')
        resource_info_box.addWidget(self.rwTips)
        resource_info_box.addStretch(6)
        resource_info_box.addWidget(self.operateRWButton)

        self.resource = QPlainTextEdit()
        self.resource.setReadOnly(True)
        self.resource.setPlainText('default texts')

        self.readerResourceTips = QLabel('readers who are reading will shown below')

        view_widgets = []
        for i in range(4):
            view_widgets.append(QWidget())
            view_widgets[-1].setFixedHeight(50)
            view_widgets[-1].setProperty('name', 'widget')
        self.readersReadingPane = QGridLayout(view_widgets[0])
        self.readersReadingPane.setContentsMargins(5, 5, 5, 5)
        self.readersReadingPane.setAlignment(Qt.AlignLeft)
        self.readersReadingPane.setSpacing(5)

        self.readersReadingPane.setObjectName('readers_reading_pane')

        resource_box.addLayout(resource_info_box)
        resource_box.addWidget(self.resource)
        resource_box.addWidget(self.readerResourceTips)
        resource_box.addWidget(view_widgets[0])

        rw_box = QHBoxLayout()
        button_box = QVBoxLayout()
        self.addReaderButton = QPushButton()
        self.addReaderButton.setText('add reader')
        self.addReaderButton.setObjectName('addReader')
        self.addReaderButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.addReaderButton.setFixedWidth(100)
        button_box.addWidget(self.addReaderButton)
        self.addWriterButton = QPushButton()
        self.addWriterButton.setText('add writer')
        self.addWriterButton.setObjectName('addWriter')
        self.addWriterButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.addWriterButton.setFixedWidth(100)
        button_box.addWidget(self.addWriterButton)

        r_box, w_box = QHBoxLayout(), QGridLayout()
        self.readersWaitingPane = QGridLayout(view_widgets[1])
        self.readersWaitingPane.setContentsMargins(5, 5, 5, 5)
        self.readersWaitingPane.setAlignment(Qt.AlignLeft)
        self.readersWaitingPane.setSpacing(5)
        self.writersWaitingPane = QGridLayout(view_widgets[3])
        self.writersWaitingPane.setContentsMargins(5, 5, 5, 5)
        self.writersWaitingPane.setAlignment(Qt.AlignLeft)
        self.writersWaitingPane.setSpacing(5)

        view_widgets[2].setFixedWidth(50)
        self.writersWritingPane = QHBoxLayout(view_widgets[2])
        self.writersWritingPane.setContentsMargins(5, 5, 5, 5)

        r_box.addWidget(view_widgets[1])

        w_box.addWidget(QLabel(), 0, 0)
        w_box.addWidget(view_widgets[2], 1, 0)
        w_box.addWidget(QLabel('writers\' buffer'), 0, 1)
        w_box.addWidget(view_widgets[3], 1, 1)

        view_widgets[1].setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        view_widgets[2].setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))

        rw_waiting_box = QVBoxLayout()
        rw_waiting_box.addWidget(QLabel('readers\' buffer'))
        rw_waiting_box.addLayout(r_box)
        rw_waiting_box.addLayout(w_box)

        rw_box.addLayout(button_box)
        rw_box.addLayout(rw_waiting_box)

        self.mainLayout.addLayout(resource_box)
        self.mainLayout.addLayout(rw_box)
        self.setLayout(self.mainLayout)

        self.setStyleSheet(
            '''
           QWidget[name = "widget"] {
				background: #ffffff; 
				border: 1px solid #eaeaea;
				font-weight: light;
			}
            '''
        )
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_operateRW_clicked(self):
        if self.rwStatus == 0:
            pass
        elif self.rwStatus == 1:
            for k, v in self.readLocks.items():
                v.unlock()
                break
        elif self.rwStatus == 2:
            self.writeLock.unlock()

    @pyqtSlot()
    def on_addReader_clicked(self):
        self.readLocks[self.readTot] = QMutex()
        self.addReader('buffer', self.readTot)
        self.readerThreads.append(Reader(self, self.readTot))
        self.readTot += 1
        self.readerThreads[-1].readStartSignal.connect(self.__readStart)
        self.readerThreads[-1].readEndSignal.connect(self.__readEnd)
        self.readerThreads[-1].start()

    @pyqtSlot()
    def on_addWriter_clicked(self):
        self.writerWindow = WriterWindow(self)
        self.writerWindow.setWindowModality(Qt.ApplicationModal)
        self.writerWindow.signal.connect(self.writerWindowCallback)
        self.writerWindow.show()

        screen_resolution = QApplication.desktop().screenGeometry()
        user_screen_width, user_screen_height = screen_resolution.width(), screen_resolution.height()

        self.writerWindow.move((user_screen_width - self.writerWindow.width()) // 2,
                               (user_screen_height - self.writerWindow.height()) // 2)

    def writerWindowCallback(self, text, id):
        self.addWriter(text, id)
        self.writerThreads.append(Writer(self, text, id))
        self.writerThreads[-1].writeStartSignal.connect(self.__writeStart)
        self.writerThreads[-1].writeEndSignal.connect(self.__writeEnd)
        self.writerThreads[-1].start()

    def addWriter(self, text, id):
        self.__writerWaitingLock.lock()
        writer_object = WriterObject(id, text)
        writer_object.signal.connect(self.showWriter)
        self.writersWaitingPane.addWidget(writer_object, 0, self.writersWaitingPane.count(), 1, 1)
        self.__writerWaitingLock.unlock()

    def showWriter(self, text, id):
        self.writerWindow = WriterWindow(self)
        self.writerWindow.setWindowModality(Qt.ApplicationModal)
        self.writerWindow.writerIDEdit.setText(id)
        self.writerWindow.resource.setPlainText(text)
        self.writerWindow.setReadOnly(True)
        self.writerWindow.show()

        screen_resolution = QApplication.desktop().screenGeometry()
        user_screen_width, user_screen_height = screen_resolution.width(), screen_resolution.height()

        self.writerWindow.move((user_screen_width - self.writerWindow.width()) // 2,
                               (user_screen_height - self.writerWindow.height()) // 2)

    def removeWriter(self, id):
        self.__writerWaitingLock.lock()
        num = self.writersWaitingPane.count()
        for idx in range(num):
            widget = self.writersWaitingPane.itemAt(idx)
            assert type(widget.widget()) is WriterObject
            if widget.widget().id == id:
                self.writersWaitingPane.removeWidget(widget.widget())
                break
        if self.writersWaitingPane.count() == 0:  # force refresh
            self.writersWaitingPane.addWidget(MainWindow.Dummy(), 0, 0, 1, 1)
            self.writersWaitingPane.removeWidget(self.writersWaitingPane.itemAt(0).widget())
        self.writersWaitingPane.update()
        self.__writerWaitingLock.unlock()

    def addReader(self, opt, id):
        pane = None
        if opt == 'buffer':
            pane = self.readersWaitingPane
        elif opt == 'reading':
            pane = self.readersReadingPane
        self.__readerWaitingOrReadingLock.lock()
        pane.addWidget(ReaderObject(id), 0, pane.count(), 1, 1)
        self.__readerWaitingOrReadingLock.unlock()

    def removeReader(self, opt, id):
        pane = None
        if opt == 'buffer':
            pane = self.readersWaitingPane
        elif opt == 'reading':
            pane = self.readersReadingPane
        num = pane.count()
        for idx in range(num):
            widget = pane.itemAt(idx)
            assert type(widget.widget()) is ReaderObject
            if widget.widget().id == id:
                pane.removeWidget(widget.widget())
                break
        if pane.count() == 0:  # force refresh
            pane.addWidget(MainWindow.Dummy(), 0, 0, 1, 1)
            pane.removeWidget(pane.itemAt(0).widget())
        pane.update()

    def __writeStart(self, text, id):
        self.rwStatus = 2
        self.operateRWButton.setText('remove writer')
        self.rwTips.setText('there is a writer who is writing')
        self.resource.setPlainText(text)

        self.removeWriter(id)
        writer_object = WriterObject(id, text)
        writer_object.signal.connect(self.showWriter)
        self.writersWritingPane.addWidget(writer_object)

    def __writeEnd(self, id):
        self.rwStatus = 0
        self.operateRWButton.setText('remove reader')
        self.writersWritingPane.removeWidget(self.writersWritingPane.itemAt(0).widget())
        self.writersWritingPane.addWidget(MainWindow.Dummy())
        self.writersWritingPane.removeWidget(self.writersWritingPane.itemAt(0).widget())
        self.rwTips.setText('there are neither readers nor writers')

    def __readStart(self, id):
        self.rwStatus = 1
        self.removeReader('buffer', id)
        self.addReader('reading', id)
        self.operateRWButton.setText('remove reader')
        if self.readersReadingPane.count() == 1:
            self.rwTips.setText('there is a reader who is reading')
        else:
            self.rwTips.setText('there are {} readers who are reading'.format(self.readersReadingPane.count()))

    def __readEnd(self, id):
        self.removeReader('reading', id)
        self.readLocks[id].unlock()
        self.readLocks.pop(id)

        if self.readersReadingPane.count() == 1:
            self.rwTips.setText('there is a reader who is reading')
        elif self.readersReadingPane.count() == 0:
            self.rwStatus = 0
            self.rwTips.setText('there are neither readers nor writers')
        else:
            self.rwTips.setText('there are {} readers who are reading'.format(self.readersReadingPane.count()))


class WriterWindow(QDialog):
    signal = pyqtSignal(str, str)

    def __init__(self, parent: MainWindow):
        super(WriterWindow, self).__init__()
        self.mainLayout = QVBoxLayout()
        self.parentWindow = parent

        self.writerIDEdit = QLineEdit()
        id_box = QHBoxLayout()
        id_box.addWidget(QLabel('writer ID:'))
        id_box.addWidget(self.writerIDEdit)

        self.resource = QPlainTextEdit()
        self.resource.setPlainText(parent.resource.toPlainText())

        self.mainLayout.addLayout(id_box)
        self.mainLayout.addWidget(QLabel('edit resource:'))
        self.mainLayout.addWidget(self.resource)
        self.OKButton = QPushButton()
        self.OKButton.setText('OK')
        self.OKButton.setObjectName('OK')
        self.mainLayout.addWidget(self.OKButton)

        self.setLayout(self.mainLayout)
        QMetaObject.connectSlotsByName(self)

        self.readOnly = False

    def setReadOnly(self, ok):
        self.writerIDEdit.setReadOnly(ok)
        self.resource.setReadOnly(ok)

    @pyqtSlot()
    def on_OK_clicked(self):
        if not self.readOnly:
            self.signal.emit(self.resource.toPlainText(), self.writerIDEdit.text())
            self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()
