from customWidget import Download_Panel
from type import DownloadInfo, State
import threading
class Downloader:
    type = None

    def __init__(self, info: DownloadInfo , parent = None, type = None) -> None:
        self.type = type
        self.parent = parent
        self.info = info
        self.dp = Download_Panel(self.parent, info)

    def download(self) -> DownloadInfo:
        pass

    def _download_done(self, file_dir, forder_dir):
        self.dp.progress.IsPostprocessing(False)
        #self.dp.progress.done()
        self.dp.progress.time_stop_signal.emit()
        self.info.file_path = file_dir
        self.info.dir = forder_dir
        self.info.state = State.Done

class Video:

    def __init__(self, info: DownloadInfo) -> None:
        self.info = info