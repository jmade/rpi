import subprocess

BASE_DIR = '/home/pi/Ambilight/lib/shell/atv.sh'

def atv_remote(command_name):
	subprocess.Popen(['bash', BASE_DIR, command_name])