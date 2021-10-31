from jobs import rq
import time
from pytube import YouTube

@rq.job
def CleanYoutubeJob(video_url, on_success=None):
  #download video from youtube
  yt=YouTube(video_url)
  audio_url = yt.streams.get_by_itag(140).url

