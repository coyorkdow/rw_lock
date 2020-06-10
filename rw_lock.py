from PyQt5.QtCore import QThread, pyqtSignal, QMutex

_read_num_lock = QMutex()
_write_lock = QMutex()
reader_cnt = 0


class Reader(QThread):
    readStartSignal = pyqtSignal(int)
    readEndSignal = pyqtSignal(int)

    def __init__(self, main_window, id):
        super(Reader, self).__init__()
        super().__init__()
        self.mainWindow = main_window
        self.id = id

    def run(self):
        try:
            self.__read_acquire()
            self.mainWindow.readLocks[self.id].lock()
            self.readStartSignal.emit(self.id)

            self.mainWindow.readLocks[self.id].lock()
            self.readEndSignal.emit(self.id)
        finally:
            self.__read_release()

    def __read_acquire(self):
        global reader_cnt
        _read_num_lock.lock()
        reader_cnt += 1
        if reader_cnt == 1:
            _write_lock.lock()
        _read_num_lock.unlock()

    def __read_release(self):
        global reader_cnt
        _read_num_lock.lock()
        reader_cnt -= 1
        if reader_cnt == 0:
            _write_lock.unlock()
        _read_num_lock.unlock()


class Writer(QThread):
    writeStartSignal = pyqtSignal(str, str)
    writeEndSignal = pyqtSignal(str)

    def __init__(self, main_window, text, id):
        super(Writer, self).__init__()
        super().__init__()
        self.mainWindow = main_window
        self.text = text
        self.id = id

    def run(self):
        try:
            _write_lock.lock()
            self.mainWindow.writeLock.lock()
            self.writeStartSignal.emit(self.text, self.id)

            self.mainWindow.writeLock.lock()
            self.writeEndSignal.emit(self.id)
            self.mainWindow.writeLock.unlock()
        finally:
            _write_lock.unlock()
