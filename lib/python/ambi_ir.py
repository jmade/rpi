import subprocess
from time import sleep
from lib.python.ambi_background import light_reading, start_blackout, start_process, stop_process

BASE_DIR = '/home/pi/Ambilight/lib/shell/ir/hdmi_switcher.sh'

def runHDMISwitch(button_name):
	subprocess.Popen(['bash', BASE_DIR, button_name])

#  read status via light_reading 
#  perform switching
#  restore state, blackout if nothing running.

def read_state():
	info = light_reading()
	status = info['status']
	process = info['process']
	state = (status,process)
	return state

def prepare_state(state):
	status = state[0]
	if status == "N":
		print("Not Running.")
		return
	else:
		process = state[-1]
		print("Terminating Process: "+process)
		stop_process(process)

def restore_state(state):
	status = state[0]
	if status == "N":
		print("Performing Blackout Function.")
		start_blackout()
		return
	else:
		process = state[-1]
		print("Restoring Process: "+process)
		start_process(process)

# Commands
def press_button_1():
	runHDMISwitch('button_1')

def press_button_2():
	runHDMISwitch('button_2')

def press_button_3():
	runHDMISwitch('button_3')

def press_button_4():
	runHDMISwitch('button_4')

def press_button_sel():
	runHDMISwitch('button_sel')

def press_button_pip():
	runHDMISwitch('button_pip')

def press_button_enter():
	runHDMISwitch('button_enter')

# New Input
def hdmi_switch(input):
	print("Reading State.")
	state = read_state()
	prepare_state(state)
	print("--\nIR")
	runHDMISwitch('b_'+str(input)+'_i_1')
	sleep(1.0)
	runHDMISwitch('b_'+str(input)+'_i_2')
	sleep(1.0)
	print("IR\n--")
	print("Restore State")
	restore_state(state)