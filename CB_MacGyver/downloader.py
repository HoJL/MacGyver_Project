from customWidget import Download_Panel
from type import DownloadInfo, State, MetaData
import threading
import subprocess
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
        meta_cmd = 'ffprobe -v error -show_entries stream=codec_long_name:format=duration:format=size -of default=noprint_wrappers=1 -i ' + self.info.file_path
        p = subprocess.Popen(meta_cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        out_str = p.stdout.read().decode('ascii')
        li = out_str.splitlines()
        meta_dict = {}
        key_list =[]
        for item in li:
            item_li = item.split('=')
            if item_li[0] in meta_dict:
                meta_dict[item_li[0]] = meta_dict[item_li[0]] + '\n' + item_li[1]
            else:
                meta_dict[item_li[0]] = item_li[1]
                key_list.append(item_li[0])

        self.metadata = MetaData()
        self.metadata.codec = meta_dict[key_list[0]]
        self.metadata.length = meta_dict[key_list[1]]
        self.metadata.size = meta_dict[key_list[2]]