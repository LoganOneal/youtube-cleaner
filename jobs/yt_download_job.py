from jobs import rq
import time
from pytube import YouTube

q = rq.get_queue()

@rq.job
def YT_DownloadJob(video_url, fname):
  path = "/data/"
  #download video from youtube
  yt=YouTube(video_url)

  stream = yt.streams.filter(file_extension='mp4')[1]
  stream.download(output_path=path, filename=fname)