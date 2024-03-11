import importlib

#모듈이름은 다운로드타입_downloader
#Module naming rule: 'Download type_downloader'

#클래스이름은 Download_다운로드타입
#Class naming rule: 'Download_download type'

#ex) 유튜브의 경우 모듈 : youtube_downloader 클래스 : Download_Youtube
#ex) if you download Youtube, 
#Module name is 'youtube_downloader' and Class name is 'Download_Youtube'


# type = 'm3u8'
# fix = 'download'
# pkg = 'downloaderList.'

# mod_str = pkg + type + '_' + fix +'er'
# cls_str = fix.capitalize() + '_' + type.capitalize()

# #module = __import__(mod_str, fromlist=['test_downloader'])
# module = importlib.import_module(mod_str)
# cls = getattr(module, cls_str)('args')

# cls.download('https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8')


# import base64

# with open('./CB_MacGyver/images/말랑곰.png', 'rb') as f:
#     imdata = base64.b64encode(f.read())

# with open('./imdate.txt', 'wb') as f:
#     f.write(imdata)

from pyqt_toast import Toast


import os
import re
#dir = 'C:/Users/HoJ/Downloads/output/'
files = os.listdir(dir)
p = re.compile(r'\d+')
#a = p.findall(txt)[-1]
files = sorted(files, key=lambda s: int(p.findall(s)[-1]))
#files.sort(key=lambda s: p.findall(s)[-1])
with open('merged.txt', 'w', encoding='utf-8') as fout:
    for file in files:
        if '.txt' not in file:
            continue
        with open(dir + file, 'rt', encoding='utf-8') as fin:
            fout.write(fin.read())