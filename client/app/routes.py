from flask import Blueprint, request, redirect, render_template, url_for
from .events import socketio
# from .tasks import *


site = Blueprint('site', __name__)

@site.route('/test')
def test():

    return render_template('test.html', scriptName='test.js')

@site.route('/home', methods=['GET', 'POST'])
def home():

    update_week_free_slots.delay()

    return render_template('home.html', scriptName='home.js')

@site.route('/booking-summary', methods=['GET', 'POST'])
def summary():

    return render_template('summary.html')