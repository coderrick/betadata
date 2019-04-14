import os
from flask import Flask, render_template, request,redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from app.upload import upload_blob
from app.label import analyze_labels
import json 
from app.models import Detected
from config import Config
from app.forms import SearchForm

UPLOAD_FOLDER = '/home/lewd/gdprojects/betadata/backend/app/static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4', 'mkv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# basedir = os.path.abspath(os.path.dirname(__file__))
# SECRET_KEY = os.environ.get('SECRET_KEY') or 'seeker'
# GOOGLE_APPLICATION_CREDENTIALS=os.environ.get("SECRET_KEY")
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#     'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_TRACK_MODIFICATIONS = False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            gcs_upload = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            to_gcs = upload_blob('ziscography_bucket', gcs_upload, filename)
            results = analyze_labels(to_gcs)
            for result in results:
                try: 
                    d = Detected(label_description=result['label_description'], label_category=result['label_category'], start_time=result['start_time'], end_time=result['stop_time'], confidence=result['confidence'])
                    db.session.add(d)
                    db.session.commit()
                except: 
                    pass
            return render_template('search_results.html', results=results)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if 'search_term' not in request.form:
            flash('No search term entered')
            return redirect(request.url)
        search_term = request.form['search_term']
        s = search_term.split()
        if ('play') in s:
            if ('from') in s:
                return render_template('player.html')
            if ('clip') in s:
                return 'playing clip'
        elif ('find') in s:
            if ('first') in s:
                return 'playing first'
            if ('last') in s:
                return 'playing last'
            else:
                return 'x clips found'
        else:
            return 'search term not understood'
    return render_template("search.html")

# @app.route('/search_results', methods=['GET', 'POST'])
# def search_results():
#     return render_template("search_results.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
