import threading as thread
import random


class RWLocker:
    def __init__(self):
        self.__read_num_lock = thread.Lock()
        self.__write_lock = thread.Lock()
        self.resource = 0
        self.__read_cnt = 0

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

    def reader(self, no):
        try:
            self.__read_acquire()
            print('reader {} is reading resource... resource={}'.format(no, self.resource))
        finally:
            self.__read_release()

    def writer(self, no):
        try:
            self.__write_acquire()
            self.resource += 1
            print('writer {} is writing resource... resource={}'.format(no, self.resource))
        finally:
            self.__write_release()

    def run(self):
        for i in range(100):
            rand = random.randint(0, 100)
            if rand > 50:
                _thread = thread.Thread(target=self.reader, args=(i,))
                _thread.start()
            else:
                _thread = thread.Thread(target=self.writer, args=(i,))
                _thread.start()


if __name__ == '__main__':
    rw_locker = RWLocker()
    rw_locker.run()