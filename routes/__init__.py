from flask import render_template, request, redirect, url_for, Blueprint
from jobs.filtering_job import FilteringJob

blueprint = Blueprint("blueprint", __name__)

@blueprint.route('/')
def index():
    return render_template("index.html")

@blueprint.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        url = request.form['url']
        # make call to service to get the video
        FilteringJob.queue(url)
        redirect(url_for("upload"))
    else:
        return render_template("upload.html")