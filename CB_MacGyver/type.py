from dataclasses import dataclass
from paths import MyIcon
from enum import Enum

type_list = {'www.youtube.com': 'youtube','youtu.be': 'youtube'}
ext_list = {'.m3u8': 'm3u8'}


icon_list = {'youtube': MyIcon.YOUTUBE_ICON, 'm3u8': MyIcon.M3U8_ICON}

class State(Enum):
    Normal = 0
    Loading = 1
    Done = 2
    Error = -1

@dataclass
class DownloadInfo:
    url: str = None
    name: str = None
    type: str = None
    state: State = State.Normal
    error_code :str = None
    size: int = 0
    file_path:str = None
    dir:str = None

@dataclass
class MetaData:
    size: int = 0
    length: str = None
    codec:str = None