from flask import Blueprint, request, redirect, render_template, url_for
from EdgeBookingAppV1.app.TheEdgeTools import *
from EdgeBookingAppV1.app.forms import QuickBookingForm


site = Blueprint('site', __name__)

@site.route('/test')
def test():

    return render_template('test.html', scriptName='test.js')

@site.route('/home', methods=['GET'])
def home():

    weekFreeSlotDict = {}

    if sign_in(username, password):

        weekFreeSlotDict = summarise_week_free_slots()

    return render_template('home.html', scriptName='home.js', weekFreeSlotDict=weekFreeSlotDict)

@site.route('/booking-summary', methods=['POST'])
def summary():



    return render_template('summary.html')