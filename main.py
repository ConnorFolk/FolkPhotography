# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:00:07 2022

@author: C onnor
"""

from flask import Flask, render_template, request, redirect, url_for
#from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from os.path import isfile, join, isdir
from werkzeug.utils import secure_filename
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'
gcs = storage.Client()
bucket = gcs.get_bucket("imagesforsublimecoverbandits")

def get_foldernames(bucket_name, prefix, delimiter=None):

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    print("Blobs:")
    for blob in blobs:
       print(blob.name)

    if delimiter:   
         words = [prefix for prefix in blobs.prefixes]
         splitwords = [word.split('/')[3] for word in words]
         return splitwords
     
def get_file(bucket_name, prefix, var):
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix + str(var))
    return [blob.public_url for blob in blobs]

get_file('imagesforsublimecoverbandits', 'static/images/folk/', 20220816)

@app.route('/')
def home():
    app.config['UPLOAD_FOLDER'] = 'static/images'
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/folk') if isdir(join(app.config['UPLOAD_FOLDER'] + '/folk', f))]
    return render_template('home.html', folders=folders)

@app.route('/folk')
def folk():
    folders = get_foldernames('imagesforsublimecoverbandits', 'static/images/folk/', '/')
    return render_template('folk.html', folders=folders)

@app.route('/folk/<var>')
def folkrepo(var):
    app.config['UPLOAD_FOLDER'] = 'static/images'
    folders = get_foldernames('imagesforsublimecoverbandits', 'static/images/folk/', '/')
    if str(var) in folders:
        filename= get_file('imagesforsublimecoverbandits', 'static/images/folk/', var)
        return  render_template('blash.html', userimage=filename, name=var)
    else:
        return f'nope'
@app.route('/coop')
def coop():
    app.config['UPLOAD_FOLDER'] = 'static/images'
    folders = get_foldernames('imagesforsublimecoverbandits', 'static/images/coop/', '/')
    return render_template('coop.html', folders=folders)    

@app.route('/coop/<var>')
def cooprepo(var):
    app.config['UPLOAD_FOLDER'] = 'static/images'
    folders = get_foldernames('imagesforsublimecoverbandits', 'static/images/coop/', '/')
    if str(var) in folders:
        filename= get_file('imagesforsublimecoverbandits', 'static/images/coop/', var)
        return  render_template('blash.html', userimage=filename, name=var)
    else:
        return f'nope'
    
@app.route('/lots')
def lots():
    app.config['UPLOAD_FOLDER'] = 'static/images'
    folders = folders = get_foldernames('imagesforsublimecoverbandits', 'static/images/lots/', '/')
    return render_template('lots.html', folders=folders)

@app.route('/lots/<var>')
def lotsrepo(var):
    app.config['UPLOAD_FOLDER'] = 'static/images'
    folders = get_foldernames('imagesforsublimecoverbandits', 'static/images/lots/', '/')
    if str(var) in folders:
        filename= get_file('imagesforsublimecoverbandits', 'static/images/lots/', var)
        return  render_template('blash.html', userimage=filename, name=var)
    else:
        return f'nope'



#@app.route('/repo/<var>') # within html you can get a webpage (display), post is uploading something to
#    #so we need to support both get and post bc we are uploading an image

#def repo(var):
#    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/connor') if isdir(join(app.config['UPLOAD_FOLDER'] + '/connor', f))]
#    if str(var) in folders:
#        folderpath= app.config['UPLOAD_FOLDER'] + "/connor/" + str(var)
#        filename = ['/'+ folderpath + '/' +  f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
#        return  render_template('blash.html', userimage=filename)
#   else:
#        return f'nope'
    
    # Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if  request.form['username'] == 'Cooper' and request.form['password'] == 'admin':
            return redirect(url_for('cooperuploads'))
        elif request.form['username'] == 'Matthew' and  request.form['password'] == 'admin':
            return redirect(url_for('lotsuploads'))
        elif request.form['username'] == 'Connor' and  request.form['password'] == 'admin':
            return redirect(url_for('folkuploads'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/cooperuploads', methods=['GET', 'POST'])
def cooperuploads():
    UPLOAD_FOLDER = 'static/images/coop'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method =='POST':
        uploaded_file = request.files.getlist('file[]')
    
        if not uploaded_file:
            return 'No file uploaded.', 400
    
        # Create a Cloud Storage client.
        gcs = storage.Client()
    
        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket("imagesforsublimecoverbandits")
        for file in uploaded_file:
        # Create a new blob and upload the file's content.
            blob = bucket.blob('static/images/coop/' + file.filename)
        
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
        return f'nice'
    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action='' method="POST" enctype="multipart/form-data">
    <p><input type="file" name="file[]" webkitdirectory="" directory="">
    <input type='submit' value='upload'>
    </p>

</form>
'''

@app.route('/lotsuploads', methods=['GET', 'POST'])
def lotsuploads():
    UPLOAD_FOLDER = 'static/images/lots'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method =='POST':
        uploaded_file = request.files.getlist('file[]')
    
        if not uploaded_file:
            return 'No file uploaded.', 400
    
        # Create a Cloud Storage client.
        gcs = storage.Client()
    
        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket("imagesforsublimecoverbandits")
        for file in uploaded_file:
        # Create a new blob and upload the file's content.
            blob = bucket.blob('static/images/lots/' + file.filename)
        
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
        #files = request.files.getlist("file[]")
        #print(request.files)
        #for file in files:
        #    path = os.path.dirname(file.filename)
        #    path2 = os.path.join(app.config['UPLOAD_FOLDER'], path)
        #    if not os.path.exists(path2):
        #        os.mkdir(path2)
        #    filename = os.path.join(path, secure_filename(os.path.basename(file.filename)))
        #   file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'nice'
    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action='' method="POST" enctype="multipart/form-data">
    <p><input type="file" name="file[]" webkitdirectory="" directory="">
    <input type='submit' value='upload'>
    </p>

</form>
'''

@app.route('/folkuploads', methods=['GET', 'POST'])
def folkuploads():
    UPLOAD_FOLDER = 'static/images/folk'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method =='POST':
        uploaded_file = request.files.getlist('file[]')
    
        if not uploaded_file:
            return 'No file uploaded.', 400
    
        # Create a Cloud Storage client.
        gcs = storage.Client()
    
        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket("imagesforsublimecoverbandits")
        for file in uploaded_file:
        # Create a new blob and upload the file's content.
            blob = bucket.blob('static/images/folk/' + file.filename)
        
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
        return f'nice'
    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action='' method="POST" enctype="multipart/form-data">
    <p><input type="file" name="file[]" webkitdirectory="" directory="">
    <input type='submit' value='upload'>
    </p>

</form>
'''       
    #for folder in folders:
    #    var=folder
    #    folderpath= app.config['UPLOAD_FOLDER'] + "/" + str(folder)
    #    filename = [folderpath + '/' +  f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
    #return render_template('index.html', userimage=filename)



if __name__=="__main__":
    app.run(port=1001)
    
mypath='static/images'

