from jobs import rq
from extensions import aai, gcs
import subprocess
import math

@rq.job
def CleanVideoJob(fpath, curse_matches, on_success=None):
  for match in curse_matches:
      clean_path = f"{fpath.split('.')[-2]}-clean.{fpath.split('.')[-1]}"
      mutes =  ", ".join([f"volume=enable='between(t, {math.floor(t[0] / 1000)}, {math.floor(t[1])})':volume=0" for t in match['timestamps']]) 
      subprocess.call(['ffmpeg', '-i', fpath, '-af', mutes, clean_path])
      url = gcs.upload_file(f"{clean_path}", "youtube-cleaner")
      on_success(url)