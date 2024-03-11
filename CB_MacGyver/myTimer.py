import threading

class MyTimer():

    def __init__(self, slot = None):

        self.__interval = 1
        self.__slot = slot

    def setInterval(self, interval):
        self.__interval = interval

    def start(self):
        self.timer = threading.Timer(self.__interval, self.__timer)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def connect(self, slot):
        self.__slot = slot

    def __timer(self):
        if self.__slot is not None:
            self.__slot()
        self.timer = threading.Timer(self.__interval, self.__timer)
        self.timer.start()
