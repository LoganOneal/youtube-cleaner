import os
import time
import requests
from pytube import YouTube
from google.cloud import storage
import datetime

BUCKET_NAME = "youtube-cleaner"
ASSEMBLY_API_KEY = "4951dd81c6854670a21a59696359e7ac"

def run(video_url):
  video_id = str(int(time.time()))
  mp4_name = video_id + ".mp4"
  #download video from youtube
  yt=YouTube(video_url)
  stream = yt.streams.get_by_itag(22)
  stream.download(filename=mp4_name)
  print(mp4_name)

  print(os.system("dir"))
  #convert video to mp3
  mp3_file = video_id + ".mp3"
  os.system("ffmpeg -i {} {}".format(mp4_name, mp3_file))

  #upload mp3 to google bucket
  storage_client = storage.Client()
  bucket = storage_client.bucket(BUCKET_NAME)
  blob = bucket.blob(mp3_file)
  blob.upload_from_filename(mp3_file)

  print(
      "File {} uploaded to {}.".format(
          source_file_name, destination_blob_name
      )
  )
    
  bucket_url = blob.generate_signed_url(
  version="v4",
  # This URL is valid for 15 minutes
  expiration=datetime.timedelta(minutes=15),
      # Allow PUT requests using this URL.
      method="GET",
  )
  
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
  return response.json()

if __name__ == "__main__":
    run("https://www.youtube.com/watch?v=0MAKheuCgTo")