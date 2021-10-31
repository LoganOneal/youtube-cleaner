import events
from jobs.clean_video_job import CleanVideoJob
from jobs import rq
from extensions import aai
from .clean_video_job import CleanVideoJob

q = rq.get_queue()

@rq.job
def SearchTranscriptJob(trans_id, blocked_words, fpath, on_success=None):
  matches = aai.search(trans_id, blocked_words)
  if matches != None:
    CleanVideoJob.queue(fpath, matches, on_success=events.processing_success)