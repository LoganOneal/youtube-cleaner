from jobs import rq
import time
from pytube import YouTube
from google.cloud import storage
import datetime
import requests
import os

BUCKET_NAME = "youtube-cleaner"
ASSEMBLY_API_KEY = "4951dd81c6854670a21a59696359e7ac"

@rq.job
def FilteringJob(fpath, on_success=None):
  

  #convert video to mp3
  # os.system("ffmpeg -i {} {}".format(mp4_file, mp3_file))

  # #upload mp3 to google bucket
  # storage_client = storage.Client.from_service_account_json('/app/keys/service-account.json')
  
  # bucket = storage_client.bucket(BUCKET_NAME)
  # blob = bucket.blob(mp3_file)
  # blob.upload_from_filename(fpath + mp3_file)

  # print(
  #     "File {} uploaded to {}.".format(
  #         source_file_name, destination_blob_name
  #     )
  # )
    
  
  return response.json()
