from google.cloud import storage
from flask import current_app, _app_ctx_stack
import datetime
import os, requests


class AAI:

    base_url = "https://api.assemblyai.com/v2/transcript"

    base_headers = {
        "Authorization": os.getenv('AAI_PK')
    }

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()
    
    def transcribe(self, audio_url):
        headers = self.base_headers
        headers["Content-Type"] = "application/json"
        requests.post(f"{self.base_url}/transcript", json={ "audio_url": audio_url, "webhook_url": os.getenv('BASE_URL') }, headers=headers)
