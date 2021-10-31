from jobs.search_transcript_job import SearchTranscriptJob
from jobs.clean_video_job import CleanVideoJob
from extensions import aai
from jobs.transcribe_youtube_job import TranscribeYoutubeJob
from jobs.transcribe_upload_job import TranscribeUploadJob
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

@http.route('/webhook', methods=["POST"])
def webhook():
    print('Webhook Received')
    request_json = request.json

    filename = request.args.get("vid_path")

    trans_id = request_json['transcript_id']
    words = request.args.get('words')

    SearchTranscriptJob.queue(trans_id, words, filename)

    return 'Webhook notification received', 200

@http.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        url = request.form['url']
        words = request.form['words']

        fname = str(int(time.time())) + '.mp4'

        if url == "":
            file = request.files['file']
            if file.filename == "":
                flash("No video given")
                return redirect(request.url)
            file.save(secure_filename('/data/' + file.filename))
            job = TranscribeUploadJob.queue('/data/' + file.filename, words)
        else:
            job = YT_DownloadJob.queue(url, fname) 
            job = TranscribeYoutubeJob.queue(url, words, "/data/" + fname)

        # make call to service to get the video
        # job = FilteringJob.queue(url, events.filter_success, meta={"upload_url": url})
        return redirect(url_for("http.show_uploads", job_id=job.id))
    else:
        return render_template("upload/new.html")

@http.route('/uploads/<job_id>')
def show_uploads(job_id):
    job = default_q.fetch_job(job_id)
    return render_template("upload/show.html", job_id=job_id, job_status=job.get_status(), base_url=getenv("BASE_URL"))

