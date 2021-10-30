from flask import Flask
import os

def create_app():
  app = Flask(__name__)
  app.config['RQ_REDIS_URL'] = os.getenv('REDIS_URL')

  from websockets import socketio
  socketio.init_app(app)

  from jobs import rq
  rq.init_app(app)

  from routes import http
  app.register_http(http)

  return app