import subprocess
from time import sleep

BASE_DIR = '/home/pi/Ambilight/lib/shell/ir/hdmi_switcher.sh'

def runHDMISwitch(button_name):
	subprocess.Popen(['bash', BASE_DIR, button_name])


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
	runHDMISwitch('b_'+str(input)+'_i_1')
	sleep(1.0)
	runHDMISwitch('b_'+str(input)+'_i_2')