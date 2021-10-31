from google.cloud import storage
from flask import current_app, _app_ctx_stack
import datetime
import os, requests


class AAI:

    base_url = "https://api.assemblyai.com/v2"

    base_headers = {}

    def __init__(self, app=None):
        self.app = app
        self.base_headers["Authorization"] = os.getenv('AAI_PK')
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
    
    def transcribe(self, audio_url, video_path, words):
        headers = self.base_headers
        headers["Content-Type"] = "application/json"
        resp = requests.post(f"{self.base_url}/transcript", json={ "audio_url": audio_url, "webhook_url": os.getenv('BASE_URL') + f"/webhook?vid_path={ video_path }&words={ words }" }, headers=headers)

    
    def search(self, transcript_id, words):
        resp = requests.get(self.base_url + f"/transcript/{transcript_id}/word-search?words={words}", headers=self.base_headers)
        resp_json = resp.json()
        if resp_json['total_count'] > 0:
            return resp_json['matches']
        return None

