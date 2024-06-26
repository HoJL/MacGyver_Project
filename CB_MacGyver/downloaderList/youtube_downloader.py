import logging
import yt_dlp
from yt_dlp import YoutubeDL
from downloader import Downloader, Video
from type import State

class Download_Youtube(Downloader):

    ydl_opts =''
    isStart = False
    isOnce = False
    class MyLogger(object):
        def __init__(self, info) -> None:
            self._info = info
        def debug(self, msg):
            if self._info.state == State.Done:
                raise InterruptedError("Canceled")
        def info(self, msg):
            if self._info.state == State.Done:
                raise InterruptedError("Canceled")
        def warning(self, msg):
            if self._info.state == State.Done:
                raise InterruptedError("Canceled")
        def error(self, msg):
            raise ValueError(msg)

    def init_opts(self):
        self.ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'progress_hooks': [self._progress_hooks],
            'postprocessor_hooks': [self._postprocessor_hooks],
            'outtmpl': 'Youtube_Download/%(title)s.%(ext)s',
            'extract_flat': True,
            'quiet': True,
            'verbose': False,
            'noplaylist': True,
            'noprogress': True,
            'postprocessors':[
            {
                'key': 'MetadataParser',
                'actions':[(yt_dlp.postprocessor.metadataparser.MetadataParserPP.replacer, 'webpage_url', '.*', '')],
                'when': 'post_process'
            },
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegMetadata',
            }
            ]
        }
        self.ydl_opts['writethumbnail'] = True
        self.ydl_opts['postprocessors'].append({'key': 'EmbedThumbnail'})
        self.ydl_opts['logger'] = self.MyLogger(self.info)

    def _progress_hooks(self, d):
        if self.info.state == State.Done:
            raise

        if self.isStart is False:
            self.isStart = True
            self.dp.setTitle(d['info_dict']['title'])
            self.info.name = d['info_dict']['title']
            self.dp.progress.setTotal(d['total_bytes'])
            self.dp.progress.setValue(0)

        if d['status'] == 'downloading':
            self.dp.progress.setValue(d['downloaded_bytes'])
        elif d['status'] == 'finished':
            self.dp.progress.setValue(d['downloaded_bytes'])
            self.dp.progress.download_done()

    def _postprocessor_hooks(self, d):
        if d['status'] == 'started':
            self.dp.progress.IsPostprocessing(True)
            if d['postprocessor'] == 'EmbedThumbnail':
                if self.isOnce is False:
                    self.isOnce = True
                    dic = d['info_dict']['__files_to_move']
                    for v in dic.values():
                        self.dp.thumbnail.setLoading(False)
                        self.dp.thumbnail.set_thumb_pixmap(v)
                        break
        elif d['status'] == 'finished':
            self.dp.progress.IsPostprocessing(False)
            #postprocessor = 'EmbedThumbnail'

    # info['id']
    # info['title']
    # info['channel_url']
    # info['webpage_url']
    # info['requested_downloads'][0]['__finaldir']
    # info['requested_downloads'][0]['filepath']
    # info['requested_downloads'][0]['ext']
    def download(self):
        super().download()
        self.init_opts()
        with YoutubeDL(self.ydl_opts) as self.ydl:
            self.dp.progress.time_start_signal.emit()
            try:
                #ydl.download(self.info.url)
                info = self.ydl.extract_info(self.info.url)
            except Exception as e:
                self.dp.progress.time_stop_signal()
                self.info.state = State.Error
                self.info.error_code = e.__str__()
                return Video(self.info)
            
            self._download_done(info['requested_downloads'][-1]['filepath'], info['requested_downloads'][-1]['__finaldir'])

        return Video(self.info)