from flask import render_template, request

from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        url = request.form['url']
    else:
        return render_template("upload.html")


