from flask import Flask
from rq import Queue
from app.worker import conn

app = Flask(__name__, instance_relative_config=True)
q = Queue(connection=conn)

from app import routes
from app import jobs

app.config.from_object('config')
