from google.cloud import storage
from flask import current_app, _app_ctx_stack
import datetime


class GCS:
    def __init__(self, app=None):
        self.client = storage.Client.from_service_account_json('/app/keys/service-account.json')
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()
    
    def upload_file(self, filepath, bucket_name):
      bucket = self.client.bucket(bucket_name)
      blob = bucket.blob(filepath.split('/')[-1])
      blob.upload_from_filename(filepath)
      
      bucket_url = blob.generate_signed_url(
      version="v4",
      # This URL is valid for 15 minutes
      expiration=datetime.timedelta(minutes=15),
      # Allow GET requests using this URL.
      method="GET",
      )

      return bucket_url
