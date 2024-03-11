import importlib
import threading
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from customWidget import Download_Panel
from type import DownloadInfo, State
import downloader

#test m3u8 https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8
class MyThread(threading.Thread):
    def __init__(self, group: None = None, target = None, name: str | None = None, args = (), kwargs = None, *, daemon: bool | None = None) -> None:
        threading.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

    def run(self) -> None:
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    
    def join(self, timeout: float | None = None):
        threading.Thread.join(self, timeout)
        return self._return

class Downloading(threading.Thread):

    def __init__(self, di: DownloadInfo, listview: QListWidget) -> None:
        threading.Thread.__init__(self)
        if di.type is None:
            self.cls = downloader.Downloader(di, listview)
        else:
            type_str = di.type
            fix = 'download'
            pkg = 'downloaderList.'

            mod_str = pkg + type_str + '_' + fix +'er'
            cls_str = fix.capitalize() + '_' + type_str.capitalize()

            #module = __import__(mod_str, fromlist=['test_downloader'])
            module = importlib.import_module(mod_str)
            self.cls = getattr(module, cls_str)(info=di, parent=listview) 
                
            
        item = QListWidgetItem(listview)
        item.setSizeHint(self.cls.dp.base.sizeHint())
        listview.setItemWidget(item, self.cls.dp.base)
        listview.addItem(item)
        self.cls.dp.update_state()
        #self.listView.addItem(dp.base)
        
        # type_str = di.type
        # fix = 'download'
        # pkg = 'downloaderList.'

        # mod_str = pkg + type_str + '_' + fix +'er'
        # cls_str = fix.capitalize() + '_' + type_str.capitalize()

        # #module = __import__(mod_str, fromlist=['test_downloader'])
        # module = importlib.import_module(mod_str)
        # self.cls = getattr(module, cls_str)(info=di, parent=listview)
        # item = QListWidgetItem(listview)
        # item.setSizeHint(self.cls.dp.base.sizeHint())
        # listview.setItemWidget(item, self.cls.dp.base)
        # listview.addItem(item)
        #self.ly.addWidget(cls.dp.base)
        #cls.download(info=di)
        # thread1 = threading.Thread(target = self.cls.download)
        # thread1.start()
    
    def run(self) -> None:
        dp: Download_Panel = self.cls.dp
        thread1 = MyThread(target = self.cls.download)
        thread1.start()
        thread1.join()
        dp.update_state_color()
        dp.update_state()

    def join(self, timeout: float | None = None) -> None:
        threading.Thread.join(self, timeout)