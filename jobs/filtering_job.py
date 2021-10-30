from jobs import rq

@rq.job
class FilteringJob:
  upload_url = ""
  download_url = ""

  def __call__(self, video_url):
    return