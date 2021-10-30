from flask_socketio import SocketIO, emit
from jobs import rq

default_q = rq.get_queue()

socketio = SocketIO()

@socketio.on("est_conn")
def establish_connection(job_id): 
  job = default_q.fetch_job(job_id)
  if not job:
    emit("status", { 404: "Job not found"})
