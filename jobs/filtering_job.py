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
    
  
  # upload to assemblyAI
  endpoint = "https://api.assemblyai.com/v2/transcript"
  json = {
  "audio_url": bucket_url
  }
  headers = {
      "authorization": ASSEMBLY_API_KEY,
      "content-type": "application/json"
  }
  response = requests.post(endpoint, json=json, headers=headers)
  assembly_id = response.json()['id']
  
  #transribe audio on AssmeblyAI
  endpoint = "https://api.assemblyai.com/v2/transcript/" + assembly_id
  headers = {
    "authorization": ASSEMBLY_API_KEY,
  }
  response = requests.get(endpoint, headers=headers)
  while(response.json()["status"] != "completed" and response.json()["status"] != "error"):
    time.sleep(1)
    response = requests.get(endpoint, headers=headers)

  if callable(on_success):
    on_success("test url")

  return response.json()
