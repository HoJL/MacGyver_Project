from dataclasses import dataclass
import paths
from enum import Enum

type_list = {'www.youtube.com': 'youtube','youtu.be': 'youtube'}
ext_list = {'.m3u8': 'm3u8'}


icon_list = {'youtube': paths.IMAGE_DIR + '/yt_icon.png', 'm3u8': paths.IMAGE_DIR + '/m3u8_Icon.png'}

class State(Enum):
    Normal = 0
    Loading = 1
    Done = 2
    Error = -1

@dataclass
class DownloadInfo:
    url: str = None
    type: str = None
    state: State = State.Normal
    error_code :str = None
    size: int = 0
    file_path:str = None
    dir:str = None