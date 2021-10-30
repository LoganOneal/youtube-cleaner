from jobs import rq
import time
from pytube import YouTube
from google.cloud import storage
import os

BUCKET_NAME = "youtube-cleaner"
ASSEMBLY_API_KEY = "4951dd81c6854670a21a59696359e7ac"

@rq.job
def FilteringJob(video_url):
  path = "/data/"
  fname = str(int(time.time()))
  #download video from youtube
  yt=YouTube(video_url)
  stream = yt.streams.get_by_itag(22)
  stream.download(output_path=path, filename=fname + ".mp4")

  #convert video to mp3
  mp4_file = fname + ".mp4"
  mp3_file = fname + ".mp3"
  os.system("ffmpeg -i {} {}".format(mp4_file, mp3_file))

  #upload mp3 to google bucket
  storage_client = storage.Client.from_service_account_json('/app/keys/service-account.json')
  
  bucket = storage_client.bucket(BUCKET_NAME)
  blob = bucket.blob(mp3_file)
  blob.upload_from_filename(path + mp3_file)

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
