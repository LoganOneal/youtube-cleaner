from jobs import rq
from extensions import gcs

@rq.job
def CleanUploadJob(fpath, on_success=None):
  gcs.upload_file(fpath, "youtube-cleaner")