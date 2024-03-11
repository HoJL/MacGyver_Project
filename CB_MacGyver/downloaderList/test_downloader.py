
class Download_Test():

    num = None
    def __init__(self, t=None) -> None:
        self.num = t

    def download(self):
        print('download start {}'.format(self.num))