from flask import Flask
from flask_sse import sse
import os

def create_app():
  app = Flask(__name__)
  app.config['RQ_REDIS_URL'] = os.getenv('REDIS_URL')

  from extensions import gcs
  gcs.init_app(app)

  from jobs import rq
  rq.init_app(app)

  from routes import http
  app.register_blueprint(http)
  app.register_blueprint(sse, url_prefix="/stream")

  return app