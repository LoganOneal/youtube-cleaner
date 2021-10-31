from jobs import rq
import time
from pytube import YouTube

q = rq.get_queue()

@rq.job
def YT_DownloadJob(video_url, fname, audio_only=False):
  path = "/data/"
  #download video from youtube
  yt=YouTube(video_url)
  if not audio_only:
    stream = yt.streams.get_by_itag(22 if not audio_only else 140)
    stream.download(output_path=path, filename=fname + ".mp4")