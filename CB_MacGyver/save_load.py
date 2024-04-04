import pickle
from PyQt5.QtCore import QObject, QSettings, QMetaType
from PyQt5.QtWidgets import QListWidget, QWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap
from customWidget.download_panel import Download_Panel
import downloader

def save(listwidget: QListWidget):
    items = [listwidget.item(idx) for idx in range(listwidget.count())]
    setting = QSettings('MacGyver.ini', QSettings.Format.IniFormat)
    setting.clear()
    cnt = 0
    setting.setValue('Downloaded/count', len(items))
    for item in reversed(items):
        #save infomation
            #title text
            #thumbnail image
            #DownloadInfo class

        dp = return_download_panel_obj(listwidget.itemWidget(item))
        pix = dp.thumbnail.splash.pixmap()
        setting.setValue('Downloaded/%d.pixmap'% cnt, pix)
        di = dp.info
        setting.setValue('Downloaded/%d.info'% cnt, di)
        cnt += 1

def return_download_panel_obj(obj) -> Download_Panel:
    return obj

def load(listwidget: QListWidget):
    setting = QSettings('MacGyver.ini', QSettings.Format.IniFormat)
    cnt = setting.value('Downloaded/count')
    if cnt is None or cnt == 0:
        return

    for idx in range(int(cnt)):
        di = setting.value('Downloaded/%d.info'% idx)
        dw = downloader.Downloader(di, listwidget)
        item = QListWidgetItem()
        item.setSizeHint(dw.dp.size())
        listwidget.insertItem(0, item)
        listwidget.setItemWidget(item, dw.dp)
        dw.dp.set_item(item)
        dw.dp.update_state()
        pixmap = setting.value('Downloaded/%d.pixmap'% idx)
        dw.dp.thumbnail.set_thumb_pixmap_by_load(pixmap)
        dw.dp.progress.setTotal(100)
        dw.dp.progress.setValue(100)