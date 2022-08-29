# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:00:07 2022

@author: C onnor
"""

from flask import Flask, render_template, request, redirect, url_for
#from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from os.path import isfile, join, isdir

app= Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/')
def home():
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/connor') if isdir(join(app.config['UPLOAD_FOLDER'] + '/connor', f))]
    return render_template('home.html', folders=folders)

@app.route('/folk')
def folk():
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/connor') if isdir(join(app.config['UPLOAD_FOLDER'] + '/connor', f))]
    return render_template('folk.html', folders=folders)

@app.route('/folk/<var>')
def folkrepo(var):
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/connor') if isdir(join(app.config['UPLOAD_FOLDER'] + '/connor', f))]
    if str(var) in folders:
        folderpath= app.config['UPLOAD_FOLDER'] + "/connor/" + str(var)
        filename = ['/'+ folderpath + '/' +  f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
        return  render_template('blash.html', userimage=filename)
    else:
        return f'nope'
    
@app.route('/lots')
def lots():
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/lots') if isdir(join(app.config['UPLOAD_FOLDER'] + '/lots', f))]
    return render_template('home.html', folders=folders)

@app.route('/coop')
def coop():
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/coop') if isdir(join(app.config['UPLOAD_FOLDER'] + '/coop', f))]
    return render_template('home.html', folders=folders)

@app.route('/repo/<var>') # within html you can get a webpage (display), post is uploading something to
    #so we need to support both get and post bc we are uploading an image

def repo(var):
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER'] + '/connor') if isdir(join(app.config['UPLOAD_FOLDER'] + '/connor', f))]
    if str(var) in folders:
        folderpath= app.config['UPLOAD_FOLDER'] + "/connor/" + str(var)
        filename = ['/'+ folderpath + '/' +  f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
        return  render_template('blash.html', userimage=filename)
    else:
        return f'nope'
    
    
    
    #for folder in folders:
    #    var=folder
    #    folderpath= app.config['UPLOAD_FOLDER'] + "/" + str(folder)
    #    filename = [folderpath + '/' +  f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
    #return render_template('index.html', userimage=filename)



if __name__=="__main__":
    app.run(port=1001)
    
mypath='static/images'

