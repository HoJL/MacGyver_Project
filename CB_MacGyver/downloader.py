from customWidget import Download_Panel
from type import DownloadInfo

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