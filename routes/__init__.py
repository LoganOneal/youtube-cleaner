from flask import render_template, request, redirect, url_for, Blueprint
from jobs.filtering_job import FilteringJob
from jobs import rq

blueprint = Blueprint("blueprint", __name__)
default_q = rq.get_queue()

@blueprint.route('/')
def index():
    return render_template("index.html")

@blueprint.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        url = request.form['url']
        # make call to service to get the video
        job = FilteringJob.queue(url)
        return redirect(url_for("blueprint.show_uploads", job_id=job.id))
    else:
        return render_template("upload/new.html")

@blueprint.route('/uploads/<job_id>')
def show_uploads(job_id):
    job = default_q.fetch_job(job_id)
    return render_template("upload/show.html", job_id=job_id, job_status=job.get_status())