#!/usr/bin/env python2.7

from flask import Flask, jsonify, request, redirect, url_for
import subprocess
import psutil
from time import sleep
import multiprocessing as mp
from multiprocessing import Process, Value
from server_lib import pages
from lib.python.led import *
from lib.python.ambilight import start_ambilight_system, stop_ambilight_system
from lib.python.AmbilightObject import *
from lib.python.ambi_ir import *
from lib.python.S300 import power, volume_up, volume_down
from lib.python.cec import hdmi_1, hdmi_2, hdmi_3, tv_power_on, tv_power_off
from lib.python.vol import volumeUp, volumeDown, volumeUpTriple, volumeDownTriple, volumeDownMax

STRIP = None
POOL = None
PROCESS = None
LOOP_PID = 0
AMBI_PID = 0
AMBILIGHT_RUNNING = False

app = Flask(__name__, static_folder='script')
app.config['SECRET_KEY'] = 'top-secret!'

# Response Dict
def request_ok(response_dict, success=True):
    response_dict.update({
        'success': success
    })
    resp = jsonify(**response_dict)
    resp.status_code = 200
    return resp


# HTML Responses
@app.route('/action',methods=['POST', 'GET'])
def action():
  if request.method == 'POST':
    action_value = request.form['action']
    if action_value is None:
        return request_ok({'message':'okay'})
    elif action_value == 'Color':
        color_string = request.form['color']
        # handle_html_color(color_string)
        return redirect(url_for('success_action',value=action_value))
    else:
        return redirect(url_for('success_action',value=action_value))
  else:
    return request_ok({'message':'okay'})


# Test Loop
@app.route('/test_loop',methods = ['POST', 'GET'])
def test_loop():
  if request.method == 'POST':
    user = request.form['nm']
    return redirect(url_for('success',name = user))
  else:
    user = request.args.get('nm')
    return redirect(url_for('success',name = user))


def makeIndexOptions():
    start_ambilight = False
    start_loop = False
    show_test = True
    if LOOP_PID == 0:
        start_loop = True
    if AMBI_PID == 0:
        start_ambilight = True
    return (start_ambilight,start_loop,show_test)

# Index
@app.route('/')
def index():
    return pages.index(makeIndexOptions())




# App Responses

# options response
def make_option_entry(title,catagory='ambilight',description='None.'):
    option = {
        'title' : title,
        'catagory' : catagory,
        'description' : description,
        'option_id' : len(title)+23284,
    }

    return option

def new_options():
    catA = 'ambilight'
    catB = 'tv'
    catC = 'test'
    catD = 'lights'
    catE = 'automation'

    return [

        make_option_entry(title='Watch Apple TV w/Ambilgiht',catagory=catE,description=''),

        make_option_entry(title='Start Ambilight',catagory=catA,description='This action will start the Ambilight System to display the given input.'),
        make_option_entry(title='Stop Ambilight',catagory=catA,description=''),

        make_option_entry(title='Wheel',catagory=catD,description='Animate the Color-Wheel on lights.'),
        make_option_entry(title='Change Color',catagory=catD,description='Change Lights to Green.'),
        make_option_entry(title='Blackout',catagory=catD,description='Turn lights to Black color.'),

        make_option_entry(title='Test',catagory=catC,description='Endpoint Test.'),
        make_option_entry(title='Solenoid Test',catagory=catC,description='Solenoid Test.'),

        make_option_entry(title='TV Off',catagory=catB,description='TV Power OFF.'),
        make_option_entry(title='TV On',catagory=catB,description='TV Power ON.'),
        make_option_entry(title='HDMI Input 1',catagory=catB,description='HDMI Input 1.'),
        make_option_entry(title='HDMI Input 2',catagory=catB,description='HDMI Input 2.'),
        make_option_entry(title='HDMI Input 3',catagory=catB,description='HDMI Input 3.'),

        make_option_entry(title='Volume Up',catagory=catB,description='Raise (+) the System Volume by 10 percent.'),
        make_option_entry(title='Volume Down',catagory=catB,description='Lower (-) the System Volume by 10 percent.'),
        make_option_entry(title='Volume Up (3)',catagory=catB,description='Raise (+) the System Volume by 30 percent.'),
        make_option_entry(title='Volume Down (3)',catagory=catB,description='Lower (-) the System Volume by 30 percent.'),
        make_option_entry(title='Volume Down Max',catagory=catB,description='Lower (-) the System Volume to 0.'),

    ]

def availible_options():
    return [
        'Start Ambilight',
        'Stop Ambilight',
        'Wheel',
        'Change Color',
        'Test',
        'Blackout',
        'Test Button',
        'TV Off',
        'TV On',
        'HDMI Input 1',
        'HDMI Input 2',
        'HDMI Input 3',
        'Volume Up',
        'Volume Down',
        'Volume Up (3)',
        'Volume Down (3)',
        'Volume Down Max',
    ]


def inquireAmbilightStatus():
    global AMBILIGHT_RUNNING
    if AMBILIGHT_RUNNING == True:
        return 1
    else :
        return 0

#  for the app 
def createOptionsResponse():
    response_dict = {}

    options = {
        'options' : availible_options(),
        'amibilight_status' : inquireAmbilightStatus(),
        'something' : 'Awesome.',
        'new_options' : new_options(),
    }

    response_dict.update({
        'options': options
    })

    return request_ok(response_dict)

# ColorStrip Commands
def changeColor():
    global STRIP
    if STRIP is None: STRIP = ambilightStripInit()
    colorWipe(STRIP,Color(0,255,0))

def blackoutStrip():
    global STRIP
    if STRIP is None: STRIP = ambilightStripInit()
    colorWipe(STRIP,Color(0,0,0))

def performWheel():
    global STRIP
    if STRIP is None: STRIP = ambilightStripInit()
    # this will block currently...
    rainbowCycle(STRIP, wait_ms=20, iterations=1)


#  Amiblight Funcs
def startBackgroundAmbilight():
    global PROCESS
    global STRIP
    global AMBILIGHT_RUNNING
    if AMBILIGHT_RUNNING == False:
        print("AMBILIGHT NOT Running, Starting it up.")
        STRIP = ambilightStripInit()
        PROCESS = Process(target=startup_amilight_obj, args=())
        PROCESS.start()
        AMBILIGHT_RUNNING = True

def stopBackgroundAmbilight():
    global PROCESS
    global AMBILIGHT_RUNNING
    print('Quitting Background Ambilight Process.')
    print(PROCESS)
    PROCESS.terminate()
    PROCESS.join()
    blackoutStrip()
    AMBILIGHT_RUNNING = False
    return

def startup_amilight_obj():
    ambiObj = AmbilightObject()
    ambiObj.describe()
    ambiObj.startAmbilight()


#################
# Server Routes #
#################

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return request_ok({
        'message': 'PONG'
    })

def emptyOption():
    print("Nothing Chosen.")

def availibleActions():
    return {
        'Start Ambilight' : startBackgroundAmbilight,
        'Stop Ambilight' : stopBackgroundAmbilight,
        'Wheel' : performWheel, 
        'Change Color' : changeColor,
        'Test' : emptyOption,
        'Blackout' : blackoutStrip,
        'Test Button' : power,
        'TV Off' : tv_power_off,
        'TV On' : tv_power_on,
        'HDMI Input 1' : hdmi_1,
        'HDMI Input 2' : hdmi_2,
        'HDMI Input 3' : hdmi_3,
        'Volume Up' : volumeUp,
        'Volume Down' : volumeDown,
        'Volume Up (3)' : volumeUpTriple,
        'Volume Down (3)' : volumeDownTriple,
        'Volume Down Max' : volumeDownMax,
    }

@app.route('/chosen_action',  methods=['GET', 'POST'])
def chosen_action():

    chosen_action = request.form['action']
    print("Chosen Action: "+chosen_action)
    availibleActions()[chosen_action]()

    return request_ok({
        'result': chosen_action
    })


@app.route('/ambi_app',  methods=['GET', 'POST'])
def ambi_app():
    sleep(1.0)
    return createOptionsResponse()


@app.route('/test', methods=['GET', 'POST'])
def test():
    print('Test')
    return request_ok({ 'message': 'Welcome to Amiblight\'s moblie API.'})


def run_app():
    app.run(debug=1.0,use_reloader=True, host='0.0.0.0', port=8080)
    
if __name__ == '__main__':
    run_app()