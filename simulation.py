import random
import threading as thread
import time

import matplotlib.pyplot as plt
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QApplication)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np

start_time = [i for i in range(30)]
end_time = [i for i in range(30)]
thread_time = [i for i in range(30)]
thread_flag = [i for i in range(30)]  # 0是读者 1是写者

mutex = QMutex()


class Simulation(QWidget):
    def __init__(self):
        super(Simulation, self).__init__()
        self.box = QHBoxLayout()
        self.box.addWidget(Canvas())
        self.setLayout(self.box)
        self.show()


class Canvas(FigureCanvasQTAgg):

    def __init__(self):
        self.fig = plt.figure(num=2, figsize=(16, 12), dpi=80, facecolor="white", edgecolor='green', frameon=True)
        self.axes = self.fig.add_subplot(111)
        self.setUI()
        super(Canvas, self).__init__(self.fig)

    def setUI(self):
        self.axes.set_title("r&w problem threads simulation (red means reader, black means writer)", loc='center',
                            pad=20,
                            fontsize='xx-large', color='black')  # 设置标题
        self.axes.set_xlabel('time')  # 确定坐标轴标题
        self.axes.set_ylabel("thread id")
        self.axes.set_yticks([i for i in range(30)])  # 设置坐标轴刻度

    def clear(self):
        for ax in self.fig.axes:
            ax.clear()
        self.setUI()
        self.draw()

    def reDraw(self):
        self.createMat()
        self.draw()

    def createMat(self):
        for i in range(30):
            if thread_flag[i] == 0:  # 如果是读者
                print(i, ' ', start_time[i], ' ', end_time[i])
                x1 = np.arange(int((start_time[i] - start_time[0]) * 100), int((end_time[i] - start_time[0]) * 100), 1)
                y1 = i * x1 - i * x1 + i
                self.axes.plot(x1, y1, color='red', linewidth=3, linestyle='-')

            elif thread_flag[i] == 1:  # 如果是写者
                print(i, ' ', start_time[i], ' ', end_time[i])
                x1 = np.arange(int((start_time[i] - start_time[0]) * 100), int((end_time[i] - start_time[0]) * 100), 1)
                y1 = i * x1 - i * x1 + i
                self.axes.plot(x1, y1, color='black', linewidth=3, linestyle='-')
        self.setUI()


class DrawThread(QThread):
    signal = pyqtSignal()

    def __init__(self):
        super(DrawThread, self).__init__()

    def run(self):
        mutex.lock()
        RWLocker().run()
        time.sleep(3)
        self.signal.emit()


class RWLocker:
    def __init__(self):
        self.__read_num_lock = thread.Lock()
        self.__write_lock = thread.Lock()
        self.resource = 0
        self.__read_cnt = 0
        self.all_num = 0

    @staticmethod
    def thread_work():
        time.sleep(0.1)

    def __read_acquire(self):
        self.__read_num_lock.acquire()
        self.__read_cnt += 1
        if self.__read_cnt == 1:
            self.__write_lock.acquire()
        self.__read_num_lock.release()

    def __read_release(self):
        self.__read_num_lock.acquire()
        self.__read_cnt -= 1
        if self.__read_cnt == 0:
            self.__write_lock.release()
        self.__read_num_lock.release()

    def __write_acquire(self):
        self.__write_lock.acquire()

    def __write_release(self):
        self.__write_lock.release()

    def reader(self, id):
        try:
            self.__read_acquire()
            start_time[id] = time.time()
            self.thread_work()
        finally:
            self.__read_release()
            end_time[id] = time.time()
            self.all_num += 1
            if self.all_num == 30:
                for i in range(30):
                    thread_time[i] = end_time[i] - start_time[i]

    def writer(self, id):
        try:
            self.__write_acquire()
            self.resource += 1
            start_time[id] = time.time()
            self.thread_work()
        finally:
            self.__write_release()
            end_time[id] = time.time()
            self.all_num += 1
            if self.all_num == 30:
                for i in range(30):
                    thread_time[i] = end_time[i] - start_time[i]

    def run(self):
        for i in range(30):
            time.sleep(0.01)
            rand = random.randint(0, 100)
            if rand > 50:
                thread_flag[i] = 0
                _thread = thread.Thread(target=self.reader, args=(i,))
                # start_time[i] = time.time()
                _thread.start()
            else:
                thread_flag[i] = 1
                _thread = thread.Thread(target=self.writer, args=(i,))
                # start_time[i] = time.time()
                _thread.start()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Simulation()
    win.show()
    app.exec_()
