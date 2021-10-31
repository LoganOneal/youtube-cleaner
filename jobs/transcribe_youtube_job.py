from jobs import rq
import time
from extensions import aai
from pytube import YouTube

@rq.job
def TranscribeYoutubeJob(video_url, blocked_words, video_path, on_success=None):
  #download video from youtube
  yt=YouTube(video_url)
  audio_url = yt.streams.get_by_itag(140).url

  aai.transcribe(audio_url, video_path, blocked_words)

