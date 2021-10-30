from flask import render_template, request, redirect, url_for

from app import app, q

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        from app.jobs import FilteringJob
        url = request.form['url']
        # make call to service to get the video
        q.enqueue_call(func=FilteringJob, args=(url,))
    else:
        return render_template("upload.html")