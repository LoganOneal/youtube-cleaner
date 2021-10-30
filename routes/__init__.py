from os import getenv
from flask import render_template, request, redirect, url_for, Blueprint
from jobs.filtering_job import FilteringJob
from jobs import rq

http = Blueprint("http", __name__)
ws   = Blueprint("ws", __name__)

default_q = rq.get_queue()

@http.route('/')
def index():
    return render_template("index.html")

@http.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        url = request.form['url']
        # make call to service to get the video
        job = FilteringJob.queue(url, meta={ "upload_url": url })
        return redirect(url_for("http.show_uploads", job_id=job.id))
    else:
        return render_template("upload/new.html")

@http.route('/uploads/<job_id>')
def show_uploads(job_id):
    job = default_q.fetch_job(job_id)
    return render_template("upload/show.html", job_id=job_id, job_status=job.get_status(), job_upload_url=job.meta['upload_url'], base_url=getenv("BASE_URL"))

@ws.route('jobs/<job_id>')
def job_socket(socket, job_id):
    job = default_q.fetch_job(job_id)
    filter_job = job.FilteringJob
    while not socket.closed:
        if job.is_finished():
            socket.send(f"200: {filter_job.download_url}")
        elif job.is_failed() or job.is_cancelled():
            socket.send("500: Failed to process")