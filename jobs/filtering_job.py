from jobs import rq

@rq.job
def FilteringJob(video_url):
  print(f"\n\n\n {video_url} \n\n\n")
  return