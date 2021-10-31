from flask_sse import sse

def processing_success(download_url):
  sse.publish({ "url": download_url }, type="job_update")
