import subprocess

BASE_DIR = '/home/pi/Ambilight/lib/shell/ir/hdmi_switcher.sh'

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

def runHDMISwitch(button_name):
	subprocess.Popen(['bash', BASE_DIR, button_name])