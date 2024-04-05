from pathlib import Path
from enum import Enum

BASE_DIR = Path(__file__).resolve().parent.__str__()

IMAGE_DIR = BASE_DIR + '/images'

def a(url):
    return IMAGE_DIR + url
class MyIcon():
    WIN_ICON = a('/말랑곰.png')
    LOADING_ICON = a('/loading_spin.gif')
    EXIT_ICON = a('/Exit_Icon.png')
    YOUTUBE_ICON = a('/yt_icon.png')
    M3U8_ICON = a('/m3u8_Icon.png')
    LINK_ICON = a('/Link_Icon.png')
    FORDER_ICON = a('/folder_icon.png')
    DELETE_ICON = a('/del_icon.png')
    REMOVE_ICON = a('/remove_icon.png')
    DOWNLOAD_ICON = a('/Download_Icon.png')
    MENU_ARROW_ICON = a('/down_arrow.png')
    TIME_ICON = a('/time_icon.png')
    DISK_ICON = a('/disk_icon.png')
