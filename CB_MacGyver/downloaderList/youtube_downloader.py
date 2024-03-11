import yt_dlp
from yt_dlp import YoutubeDL
from downloader import Downloader

class Download_Youtube(Downloader):

    ydl_opts =''
    isStart = False
    class MyLogger(object):
        def __init__(self) -> None:
            pass
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    def init_opts(self):
        self.ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'progress_hooks': [self._progress_hooks],
            'postprocessor_hooks': [self._postprocessor_hooks],
            'outtmpl': 'downloadY/%(title)s.%(ext)s',
            'quiet': True,
            'verbose': False,
            'postprocessors':[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegMetadata',
            },
            {
                'key': 'MetadataParser',
                'actions':[(yt_dlp.postprocessor.metadataparser.MetadataParserPP.replacer, 'webpage_url', '.*', '')],
                'when': 'pre_process'
            }
            ]
        }
        self.ydl_opts['writethumbnail'] = True
        self.ydl_opts['postprocessors'].append({'key': 'EmbedThumbnail'})
        self.ydl_opts['logger'] = self.MyLogger()

    def _progress_hooks(self, d):
        
        if d['status'] == 'downloading':
            if self.isStart is False:
                self.isStart = True
                self.dp.progress.setTotal(d['total_bytes'])
                self.dp.progress.setValue(0)

            self.dp.progress.setValue(d['downloaded_bytes'])
        elif d['status'] == 'finished':
            self.dp.progress.setValue(d['downloaded_bytes'])
            self.dp.progress.download_done()

    def _postprocessor_hooks(self, d):
        if d['status'] == 'started':
            self.dp.progress.IsPostprocessing(True)
        elif d['status'] == 'finished':
            self.dp.progress.IsPostprocessing(False)

    def download(self):
        super().download()
        self.init_opts()
        with YoutubeDL(self.ydl_opts) as ydl:
            self.dp.progress.start()
            ydl.download(self.info.url)
            self.dp.progress.done()