import subprocess
from lib.python.dbutil import background_insert

def start_loop():
	cmd = 'cd ~/rpi_ws281x/python && sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python ~/Ambilight/lib/python/ambi_loop.py'
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	print("Started Ambi_Loop")
	print(process.pid)
	kill_pid = str(int(process.pid) + 1)
	print("Kill PID: "+str(kill_pid))
	background_insert(kill_pid,'ambi_loop')

def kill_loop():
	# look up pid
	out = subprocess.check_output(('ps', '-ef'))
	output = out.decode('utf-8')
	ambi_index = output.find('ambi_loop')
	print('ambi_index:\n',ambi_index)

	spread = 100
	out_str = output[ambi_index-spread:ambi_index+spread]
	words = out_str.split()
	print("Words: \n"+str(words))
	four_letter_words = [ i for i in words if len(i) == 4 ]
	print("Four Letter Words: \n"+str(four_letter_words))
	pids = [ i for i in four_letter_words if i.isdigit() ]
	if len(pids):
		kill_pid = max(pids)
		kill_out = subprocess.Popen(['bash', '/home/pi/Ambilight/lib/shell/kill.sh', kill_pid])
	else:
		print("\nERROR:\n (pids array len is "+str(len(pids))+") Unable to find `kill_pid`.\n")

