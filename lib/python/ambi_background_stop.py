# Import the module
import commands
import subprocess

def kill_loop():
	keyword = "[a]mbi_loop"
	cmd = "ps -ef | awk '/[a]mbi_loop/{print $2}' "

	ps = subprocess.Popen(('ps', '-ef'), stdout=subprocess.PIPE)
	output = subprocess.check_output(('awk', "'/[a]mbi_loop/{print $2}'"), stdin=ps.stdout)
	ps.wait()

	out.find('ambi_loop')


	import subprocess
	out = subprocess.check_output(('ps', '-ef'))
	ambi_index = out.find('ambi_loop')
	spread = 100
	out_str = out[ambi_index-spread:ambi_index+spread]
	words = out_str.split()
	four_letter_words = [ i for i in words if len(i) == 4 ]
	pids = [ i for i in four_letter_words if i.isdigit() ]
	kill_pid = max(pids)
	kill_pid
	# kill_out = subprocess.check_output(('sudo', 'kill', '-2',kill_pid))
	kill_out = subprocess.Popen(['bash', '/home/pi/Ambilight/lib/shell/kill.sh', kill_pid])


	# checked_output = 
	
	result = commands.getstatusoutput(cmd)
	pids = result[1].split()
	print("PIDS: "+str(pids))
	kill_pid = max([int(i) for i in result[1].split()])
	print("Kill PID: "+str(kill_pid))
	kill_cmd = 'sudo kill -2 '+str(kill_pid)


	# result_of_kill = commands.getstatusoutput(kill_cmd)
	# print("Kill Result: "+str(result_of_kill))
	process = subprocess.Popen(kill_cmd, shell=True, stdout=subprocess.PIPE)
	print(process.__dict__)
	# process.kill()



	# # [
	# # 	'ps','-ef',
	# # 	'|',
	# # 	'awk', "'/[a]mbi_loop/{print $2}'"

	# # ]

	# # print("---")
	# # print("Test: Check output")
	# # out = subprocess.check_output(['ps','-ef','|','awk', "'/[a]mbi_loop/{print $2}'"])
	# # print('out:\n',out)


	# print("---")
	# print("Test: Popen Command")
	# output = subprocess.Popen("ps -ef | awk '/[a]mbi_loop/{print $2}' ", shell=True, stdout=subprocess.PIPE)
	# print(output)
	# print(output.__dict__)
	# print("STDOUT")
	# print(output.stdout)

	# print("---")
	# print("Test: Run Command")
	# run_out = subprocess.run("ps -ef | awk '/[a]mbi_loop/{print $2}' ", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	# print(run_out.__dict__)
	# print(run_out.stdout)


	# # output.wait()
	# # print(output.returncode)
	# # print(output.stdout)
	# # out_arr = str(output.stdout).split()
	# # print(out_arr)

	# # if len(out_arr):
	# # 	kill_pid = kill([int(i) for i in output.stdout.split()])
	# # 	print("Found PID: ",kill_pid)
	# # 	kill_cmd = 'sudo kill -2 '+str(kill_pid)
	# # 	kill_out = subprocess.run(kill_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	# # 	print(kill_out.stdout)
	# # else: 
	# # 	print("No Ambi_Loop Process Found.")

kill_loop()