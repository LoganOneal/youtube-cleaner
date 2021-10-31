from jobs import rq
from extensions import aai, gcs

@rq.job
def TranscribeUploadJob(fpath, blocked_words, on_success=None):
  file_url = gcs.upload_file(fpath, "youtube-cleaner")
 
  aai.transcribe(file_url, fpath, blocked_words)