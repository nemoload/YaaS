from __future__ import unicode_literals
from multiprocessing import Process
import youtube_dl
from encode import merge,fib
from redis import Redis
from rq import Queue
import json
import sys
from flask import (Flask, send_from_directory, jsonify,request, Blueprint)

YT_URL = 'https://www.youtube.com/watch?v=cwQgjq0mCdE'
VIDEO_FORMAT = '248'
AUDIO_FORMAT = '251'

YDL_PARAMS = {'quiet': False}

app = Flask(__name__)


class VideoFormat:
    def __init__(self,vformat):

        self.id = vformat['id']
        self.format = vformat['format_id']

        if vformat['acodec'] != "none" and vformat['vcodec'] != "none":
            self.type = 'av'
            self.url = vformat['url']

        elif vformat['acodec'] is not None:
            self.type = 'a'
        elif vformat['vcodec'] is not None:
            self.type = 'v'
        
        self.acodec = vformat['acodec'] 
        self.vcodec = vformat['vcodec']

        self.ext = vformat['ext']
        self.size = vformat['filesize']

        if vformat['resolution'] is not None:
            self.resolution = vformat['resolution'].split("x")[1] + "p"
        else:
            self.resolution = vformat['format']


class YoutubeVideo:
    def __init__(self,yt_url):
        self.yt_url = yt_url
        self._formats = []
        with youtube_dl.YoutubeDL(YDL_PARAMS) as ydl:
            self.info_dict = ydl.extract_info(yt_url,download=False)
            # TODO save it to the disk
    
    def download(self,video_format):
        if video_format.type == 'av':
            return video_format.url
        else:
            with youtube_dl.YoutubeDL(YDL_PARAMS) as ydl:
                ydl.params.update({'format':video_format.format,
                'outtmpl':'%(id)s_{}.%(ext)s'.format(video_format.format)})
                ydl.download([self.yt_url])
    
    def get_format(self,vformat):
        for vf in self.formats:
            if vf.format == vformat:
                return vf
    
    @property
    def formats(self):
        if not self._formats:
            self._formats = self._get_formats()
        return self._formats

    def _get_formats(self):
        formats = []
        v_id = self.info_dict['id']
        for vformat in self.info_dict['formats']:
            formats.append(VideoFormat({
                'format_id': vformat['format_id'],
                'id':v_id,
                'ext': vformat['ext'],
                'url' : vformat['url'],
                'filesize' : vformat['filesize'] if 'filesize' in vformat.keys() else None,
                'acodec': vformat['acodec'] ,              
                'vcodec': vformat['vcodec'] ,
                'resolution': vformat['resolution'] if 'resolution' in vformat.keys() else None ,
                'format': vformat['format']}))
        return formats

@app.route('/ytv/<yt_id>')
def process_ytv(yt_id):
    yt_url = "https://youtube.com/watch?v=" + yt_id
    ytv = YoutubeVideo(yt_url)
    
    return jsonify([ vf.__dict__ for vf in ytv.formats ])
    
@app.route('/ytv/<yt_id>/download')
def download(yt_id):
    
    ytv = YoutubeVideo(yt_id)

    video_format = request.args.get('video_format')
    audio_format = request.args.get('audio_format')
   

    if video_format is not None:
        video_format = ytv.get_format(video_format)
        v_process = Process(target=ytv.download,args=(video_format,))
        v_process.start()
    
    if audio_format is not None:
        audio_format = ytv.get_format(audio_format)
        a_process = Process(target=ytv.download,args=(audio_format,))
        a_process.start()
    
    try:
        v_process.join()
    except NameError:
        print("No video to process",sys.stderr)

    try:
        a_process.join()
    except NameError:
        print("No audio to process",sys.stderr)

    if audio_format and video_format:
        # TODO Merge 
        pass
    else:
        vformat = video_format or audio_format
        filename = '{id}_{format}.{ext}'.format(id=vformat.id,
        format=vformat.format,ext=vformat.ext)
        
        return send_from_directory(".", filename)
    

# if __name__ == '__main__':
    # ytv = YoutubeVideo(yt_url)
    # print(ytv.get_formats())
    # download_video()
    # q = Queue(connection=Redis())
    # q.enqueue(fib,30)
    # video_process = Process(target=download_video)
    # video_process.start()
    # res = q.enqueue(fib,40)
    # audio_process = Process(target=download_audio)
    # audio_process.start()

    # video_process.join()
    # audio_process.join()

    
    # q.enqueue(merge)
    # print(res)
