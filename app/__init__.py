from flask import Flask
import os

def create_app():
  app = Flask(__name__)
  app.config['RQ_REDIS_URL'] = os.getenv('REDIS_URL')


  from jobs import rq
  rq.init_app(app)

  from routes import blueprint
  app.register_blueprint(blueprint)

  return app