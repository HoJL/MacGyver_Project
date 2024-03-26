from customWidget import Download_Panel
from type import DownloadInfo, State

class Downloader:
    type = None
    dp = None
    
    def __init__(self, info: DownloadInfo , parent = None, type = None) -> None:
        self.type = type
        self.parent = parent
        self.info = info
        self.dp = Download_Panel(self.parent, info)

    def download(self) -> DownloadInfo:
        pass

    def _download_done(self, file_dir, forder_dir):
        self.dp.progress.IsPostprocessing(False)
        self.dp.progress.done()
        self.info.file_path = file_dir
        self.info.dir = forder_dir
        self.info.state = State.Done

class Video:

    def __init__(self, info: DownloadInfo) -> None:
        self.info = info