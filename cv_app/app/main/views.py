from . import main
from datetime import datetime , timezone 
from flask import render_template, session, redirect, url_for, make_response, request, flash, current_app

@main.route('/',methods=['GET','POST'])
def index():
    current_time = datetime.now(timezone.utc)
    return render_template('base.html', current_time=current_time)

@main.route('/projects',methods=['GET'])
def projects():
    return render_template('projects.html')

@main.route('/aiprev',methods=['GET'])
def aiprev():
    return render_template('ai_prev.html')