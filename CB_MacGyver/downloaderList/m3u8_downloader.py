import collections
import subprocess
import m3u8
import os
import shutil
import datetime
import random
from Crypto.Cipher import AES
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import time
from url_request import *

from downloader import Downloader, Video
from type import DownloadInfo, State
import paths
import threading

EncryptedKey = collections.namedtuple(typename='EncryptedKey',
                                      field_names=['method', 'value', 'iv'])

BANNED_CHARACTERS = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

class Download_M3u8(Downloader):
    
    def __init__(self, info: DownloadInfo, parent = None, type=None) -> None:
        super().__init__(info=info, parent=parent, type='m3u8')

    def _get_m3u8_obj_with_best_bandwitdth(self, uri) -> m3u8.M3U8:
        
        try:
            m3u8_obj = m3u8.load(uri)
        except (ValueError, IOError) as e:
            self.info.state = State.Error
            self.info.error_code = e.__str__()
            raise

        if m3u8_obj.is_variant:
            best_bandwidth = -1
            best_bandwidth_m3u8_uri = None
            for playlist in m3u8_obj.playlists:
                if playlist.stream_info.bandwidth > best_bandwidth:
                    best_bandwidth = playlist.stream_info.bandwidth
                    best_bandwidth_m3u8_uri = playlist.absolute_uri

            if best_bandwidth_m3u8_uri is not None:
                m3u8_obj = m3u8.load(best_bandwidth_m3u8_uri)

        return m3u8_obj

    def _construct_key_segment_pairs_by_m3u8(self, m3u8_obj) -> list:
        key_segments_pairs = list()
        for key in m3u8_obj.keys:
            if key:
                if key.method.lower() == 'none':
                    continue
                response_code, encryped_value = request_for(key.absolute_uri,
                                                            max_try_times=3)
                if response_code != 200:
                    raise Exception('DOWNLOAD KEY FAILED, URI IS {}'.format(
                        key.absolute_uri))

                encryped_value = encryped_value.decode()
                _encrypted_key = EncryptedKey(method=key.method,
                                              value=encryped_value, iv=key.iv)

                key_segments = m3u8_obj.segments.by_key(key)
                segments_by_key = [(_encrypted_key, segment.absolute_uri) for segment in
                                   key_segments if
                                   not False]

                key_segments_pairs.extend(segments_by_key)

        if len(key_segments_pairs) == 0:
            _encrypted_key = None

            key_segments = m3u8_obj.segments
            segments_by_key = [(_encrypted_key, segment.absolute_uri) for segment in key_segments
                               if not False]

            #key_segments_pairs.append((_encrypted_key, segments_by_key))
            key_segments_pairs.extend(segments_by_key)
        return key_segments_pairs

    def _random_name(self) -> str:
        random_4char = [str(random.randint(0, 20)) for i in range(4)]
        return ''.join(random_4char) 

    def _resolve_file_name(self, uri :str) -> str:
        name = uri.split('/')[-1]
        if len(name.strip()) == 0:
            return self._random_name()
        
        for c in BANNED_CHARACTERS:
            name = name.replace(c, '')

        return name

    def _download_segment(self, segment_url):
        start_time = time.time()
        response_code, response_content = request_for(segment_url)
        end_time = time.time()
        
        return response_code, response_content

    def download(self) -> DownloadInfo:
        super().download()
        
        file = 'm3u8_'
        now = datetime.datetime.now()
        date_str = now.strftime('%Y%m%d_%H%M%S')
        tmpdir = paths.BASE_DIR + '/tmp_' + date_str
        file += date_str + '.mp4'
        self.dp.setTitle(file)
        forder_dir = os.getcwd()
        forder_dir += '/M3U8_Download/'
        if os.path.isdir(forder_dir) is False:
            os.mkdir(forder_dir)
        file_dir = forder_dir + file

        self.dp.progress.time_start_signal.emit()
        try:
            m3u8_obj = self._get_m3u8_obj_with_best_bandwitdth(self.info.url)
        except:
            return self.info

        key_segment_pairs = self._construct_key_segment_pairs_by_m3u8(m3u8_obj)

        key_url_content_triple = list()
        self.dp.progress.setTotal(len(key_segment_pairs))
        self.dp.progress.setValue(0)
        #self.dp.progress.start()
        
        work_start_time = time.time()
        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_key_url = {executor.submit(self._download_segment, segment_url): (key, segment_url) for key, segment_url in key_segment_pairs}

            response_code, response_content = None, None
            for future in concurrent.futures.as_completed(future_to_key_url):
                key, segment_url = future_to_key_url[future]
                try:
                    response_code, response_content = future.result()
                except (concurrent.futures.CancelledError, concurrent.futures.TimeoutError) as e:
                    self.info.state = State.Error
                    self.info.error_code = e.__str__()
                    return self.info

                if response_code == 200:
                    key_url_content_triple.append((key, segment_url, response_content))
                    #progress update
                    self.dp.progress.update_progress()
                else:
                    self.info.state = State.Error
                    self.info.error_code = 'Response error: ' + response_code.__str__()
                    return self.info

            self.dp.progress.IsPostprocessing(True)
            if os.path.isdir(tmpdir) is False:
                os.mkdir(tmpdir)
            for key, url, content in key_url_content_triple:
                file_name = self._resolve_file_name(url)
                file_path = os.path.join(tmpdir, file_name)
                if key is not None:
                    crypt_ls = {"AES-128": AES}
                    crypt_obj = crypt_ls[key.method]
                    cryptor = crypt_obj.new(key.value,
                                            crypt_obj.MODE_CBC)
                    content = cryptor.decrypt(content)
            
                with open(file_path, 'wb') as fin:
                    fin.write(content)

        self.dp.progress.download_done()
        order_segment_list_file_path = os.path.join(tmpdir, "ts_ls.txt")
        cnt = 0
        with open(order_segment_list_file_path, 'w', encoding='utf8') as fin:
            for key, urll in key_segment_pairs:
                file_name = self._resolve_file_name(urll)
                segment_file_path = os.path.join(tmpdir, file_name)
                fin.write("file '{}'\n".format(segment_file_path))
                if cnt == 0:
                    cnt += 1
                    thumbnail_path = os.path.join(tmpdir, 'tb.png')
                    thumb_cmd = "ffmpeg -y -nostats -loglevel error -ss 0 -i " + segment_file_path + " -vcodec png -vframes 1 " + thumbnail_path
                    tumb_p = subprocess.Popen(thumb_cmd, shell=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                    tumb_p.communicate()
                    self.dp.thumbnail.set_thumb_pixmap(thumbnail_path)

        merge_cmd = "ffmpeg -y -nostats -loglevel error -f concat -safe 0 -i " + order_segment_list_file_path + " -c copy " + file_dir
        p = subprocess.Popen(merge_cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        p.communicate()
        shutil.rmtree(tmpdir)
        self._download_done(file_dir, forder_dir)
        return Video(self.info)
        