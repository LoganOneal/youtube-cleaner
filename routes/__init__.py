from jobs.yt_download_job import YT_DownloadJob
from werkzeug.utils import secure_filename
import events
from os import getenv
from flask import render_template, request, redirect, url_for, Blueprint, flash
from jobs.filtering_job import FilteringJob
from jobs import rq
import time

http = Blueprint("http", __name__)
ws   = Blueprint("ws", __name__)

default_q = rq.get_queue()

@http.route('/')
def index():
    return render_template("index.html")

@http.route('/webhook')
def webhook():
    if request.method == 'POST':
        print('Webhook Received')
        request_json = request.json

        # print the received notification
        print('Payload: ')
        # Change from original - remove the need for function to print
        print(json.dumps(request_json,indent=4))

        # save as a file, create new file if not existing, append to existing file
        # full details of each notification to file 'all_webhooks_detailed.json'
        # Change above save_webhook_output_file to a different filename

        with open(save_webhook_output_file, 'a') as filehandle:
            # Change from original - we output to file so that the we page works better with the newlines.
            filehandle.write('%s\n' % json.dumps(request_json,indent=4))
            filehandle.write('= - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - \n')

        return 'Webhook notification received', 202
    else:
        return 'Method not supported', 405

@http.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        url = request.form['url']


        fname = str(int(time.time()))

        if url == "":
            file = request.files['file']
            if file.filename == "":
                flash("No video given")
                return redirect(request.url)
            file.save(secure_filename(file.filename))
        else:
            YT_DownloadJob.queue(url, )

        # make call to service to get the video
        job = FilteringJob.queue(url, events.filter_success, meta={"upload_url": url})
        return redirect(url_for("http.show_uploads", job_id=job.id))
    else:
        return render_template("upload/new.html")

@http.route('/uploads/<job_id>')
def show_uploads(job_id):
    job = default_q.fetch_job(job_id)
    return render_template("upload/show.html", job_id=job_id, job_status=job.get_status(), job_upload_url=job.meta['upload_url'], base_url=getenv("BASE_URL"))

