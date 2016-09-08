import subprocess, threading
import random
from TimerThread import TimerThread
import time,datetime
from Tkinter import Tk
from tkFileDialog import askopenfilename
from fcntl import ioctl
from struct import pack
import md5 , sys , socket

ERROR_FILE = open("log.txt",'ab')
ERROR_FILE.seek(0)
ERROR_FILE.truncate()

STAT_FILE = open("statistics.txt",'a')

#Todo
	#Check script file. Few are mentioned there.
	#Check if essid corresponds to ad-hoc in the script. ----> 
	#Handle external WiFi Adapters - change iw dev to iwconfig. ----> 
	#Scp process becoming zombie.
	#Clear arp table in clear.sh

#### CREATE AND CONNECT CODE ####

def create():
	p = subprocess.Popen(["./create.sh",ssid,mac],stdout=subprocess.PIPE)
	output,err = p.communicate()
	p.wait()
	if output == b'fail\n':
		print("Operation Failed")
		exit(1)
	#create thread for checking neighbour
	print("Successfully connected to "+ssid)
	monitor_thread = TimerThread(run_monitor,5)
	monitor_thread.start()
	#broadcast your IP.
	run_ping()

def connect():
	
	global time_list;	
		
	start_time = time.time()	
	
	available = False
	retrying_b = False
	no_retry = 10
	while not available:
		p = subprocess.Popen(["./connect.sh",ssid],stdout=subprocess.PIPE)	
		output,err = p.communicate()
		p.wait()
		if output == b'fail\n':
			print("Operation Failed")
			exit(1)
		else:
			result = output.decode('utf-8')
			if result[7:-2] == ssid or no_retry == 0:
				print(ssid+" Found!")
				create()
				available = True
			else:
				if not retrying_b:
					print("Network not found. Retrying (Press ctrl+C to terminate)")
					retrying_b = True
		del p
		no_retry -= 1			
	
	end_time = time.time()
	timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	STAT_FILE.write("TimeStamp: "+timestamp+": Time to Connect to the Network: "+str(end_time - start_time)+"\n")
	time_list[0] = end_time - start_time

#Keep looking for bradcast packet and append new entries to g_ip_list.
def run_monitor():
	p = subprocess.Popen(["./monitor.sh"],stdout=subprocess.PIPE)
	p.wait()
	global g_ip_list
	global lock
	global mac
	ip_l = []
	with open("mon_result.txt","r") as f:
		for line in f:
			ip_l.append(line[:-1])
	with lock:
		g_ip_list = []
		for ip in ip_l:
			g_ip_list.append(ip)	

		

#Send Broadcast Packets.
#Redirect stdout and sterr to ERROR_FILE.
def broadcast_ping():
	subprocess.call(["arping","-U",mac,"-c","20"],stdout=ERROR_FILE,stderr=subprocess.STDOUT)

def run_ping():
	thread = TimerThread(broadcast_ping,15)
	thread.start()

def run_neighbour_exist():
	thread = TimerThread(check_neighbour_exist,15)
	thread.start()

def check_neighbour_exist():
	subprocess.call(["./clear_arp.sh"],stdout=ERROR_FILE,stderr=subprocess.STDOUT)
	
#### CREATE AND CONNECT CODE END ####


#### SERVICE USERNAME ####	

def service_username_dir():

	global mac, g_proc_list;	

	g_proc_list.append(subprocess.Popen(["python","Server.py", mac],stderr=ERROR_FILE))

def get_username_dir(ip):

	p = subprocess.Popen(["python","Client.py", ip],stdout=subprocess.PIPE,stderr=ERROR_FILE)

	data, err = p.communicate()
	p.wait()
	
	if data:
		return tuple(data.strip("\n").split(";"))
	else:
		return -1
	
	
	
#### SERVICE USERNAME END ####
	
		
#### SCP CODE ####

def scp_initiator(file_path, recievers):
	
	global key_to_set, ip_user,time_list;
	serial = [] 
	parallel = [];

	for reciever in recievers:
		if reciever not in ip_user:
			data = get_username_dir(reciever)
			if data != -1:
				ip_user[reciever] = data;		
	
		if reciever in ip_user and reciever not in key_to_set:	
			key_share(reciever)
		
			
	start_time = time.time()
	
	for reciever in recievers:
		if reciever in ip_user:
			if reciever in key_to_set:		
				parallel.append(reciever)

			else:
				serial.append(reciever)
		else:
			print("Cannot obtain username of remote host: "+reciever)

	scp_send_parallel(file_path, parallel)
	scp_send_serial(file_path, serial)

	end_time = time.time()

	print("Time to Transfer files to Recipients: "+str(end_time - start_time))
	
	timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	STAT_FILE.write("TimeStamp: "+timestamp+": Time to Transfer files to Recipients: "+str(end_time - start_time)+"\n")
	time_list[1] += end_time - start_time

def scp_send_parallel(file_path, parallel):

	scp_subprocess = []
	
	for reciever in parallel:
		user = ip_user[reciever][0]
		remote_path = ip_user[reciever][1]
		p = subprocess.Popen(["scp", file_path, user+"@"+reciever+":"+remote_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		scp_subprocess.append((p, reciever))


	for subprocess_obj, reciever in scp_subprocess:
		user = ip_user[reciever][0]
		scp_send(subprocess_obj, user, reciever,file_path, reciever[1])

	

def scp_send_serial(file_path, serial):

	for reciever in serial:
		user = ip_user[reciever][0]
		remote_path = ip_user[reciever][1]
		subprocess_obj = subprocess.Popen(["scp", file_path, user+"@"+reciever+":"+remote_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		scp_send(subprocess_obj, user, reciever,file_path, reciever[1]);


def scp_send(p, user, ip,file_path, remote_path):
				
	#initiate  an scp transfer
	#p = subprocess.Popen(["./scp_send.sh",user,ip, file_path, remote_path],stdout=subprocess.PIPE)
	output,err = p.communicate()
	p.wait()
	if err.find("No such file or directory") != -1:
		
		print("The file requested to be sent cannot be found. Please recheck the path specified.")

	elif err.find("lost connection") != -1:

		print("Login Failed")

	elif err.find("Permission denied") != -1:

		print("User is not the owner of the remote directory or Path specified on remote host deos not exist. Please recheck the path specified.")

	elif err.find("lost connection") != -1:

		print("No route to remote-host.")	
	
	else:

		print(file_path+" successfully transfered to remote host: "+str(user+'@'+ip+':'+remote_path))
	


# generate the public and private key files
	
def key_share(ip):
	
	user = ip_user[ip][0]
	p = subprocess.Popen(["ssh-copy-id", user+"@"+ip],stdout=ERROR_FILE, stderr=ERROR_FILE)
	output,err = p.communicate()
	p.wait()
	ssh_send(ip)


# ssh login to detect whether a password is required i.e. to see if public keys were transfered successfully
def ssh_send(ip):

	global key_to_set, ip_user;

	user = ip_user[ip][0]

	#refresh_ip_list()
	p = subprocess.Popen(["./ssh_send.sh",user, ip],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output,err = p.communicate()
	if output == b'success\n':
		print("Public shared to "+str(user+"@"+ip))
		key_to_set.add(ip)
	p.wait()

#### SCP CODE END ####

#### TKINTER CODE ####

def file_gui():
	
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	
	if filename:
		return filename
	else:	
		return -1

#### TKINTER CODE END ####

#### GENERATE IP CODE ####

def get_interface():
	p = subprocess.Popen("sudo iw dev | grep Interface | awk \'{print $2}\'", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)	
	interface,err = p.communicate()
	p.wait()

	if interface:	
		return interface.strip("\n")
	else:
		return -1

def getHwAddr(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = ioctl(s.fileno(), 0x8927, pack('256s', ifname[:15]))
	s.close()
	return ':'.join(['%02x' % ord(char) for char in info[18:24]])


def hasher(t):
	x=0
	for i in t:
		x=x+int(i,16)
	if(x>255):
		x=x%255
	
	return x

def preHash(mac):
	m=mac.split(":")
	oc = m[3:]	
	sub = []
	m=md5.new()
	for i in oc:
		m.update(i)
		sub.append(hasher(m.hexdigest()))	
	return sub

def generate_ip():
	interface = get_interface()

	if not interface == -1:
		mac=getHwAddr(interface)
		ip=preHash(mac)
		return "10."+str('.'.join(list(map(str,ip))))

#### GENERATE IP CODE END ####
	
#### MISC ####

def menu_generate():
	
	global ssid, g_ip_list,lock;	
	
	while(1):

		print("MENU\n1. Send File across network\n2. Exit")
		choice = int(raw_input("choose an option: "))
		
		if choice == 1:
			#run to see if the given neighbours exist
			#run_neighbour_exist()

			#set a copy of g_ip_list to work on

			with lock:
				g_ip_temp = g_ip_list
			
			#g_ip_temp = ["10.42.0.227"]	
			#print(g_ip_temp)
			
			if len(g_ip_temp) != 0:
				recievers = []
				for i in range(len(g_ip_temp)):
					print(str(i)+". "+g_ip_temp[i])
				choice1 = raw_input("choose an list of nodes to send to: [-1 to return to main menu] ").strip().split()

				temp = [x for x in choice1 if int(x) >= len(g_ip_temp)]
				print(temp)
				if not temp and not choice1[0] == "-1":
					for i in choice1:
						recievers.append(g_ip_temp[int(i)]);

					print(recievers)
					#Check if file is correct.
					file_path = file_gui()
					if  file_path!= -1:
						pass
						scp_initiator(file_path,recievers)
				else:	
					print("Invalid choice of neighbours")

			else:
				print("Cannot find others in network. Try again")

		elif choice == 2:
			exit_choice = raw_input("Are you sure you want to exit? [y/n]: ")
			if exit_choice == 'y':
				break;
			else:
				print("Still connected to network: ", ssid)

		else:
			print("Invalid Option. Please Try Again.")

#### MISC END ####
	
#### MAIN ###
lock = threading.Lock()
g_ip_list = []		#Global ip list.
key_to_set = set()	#global list of remote hosts with which public keys have been shared
ip_user = {}		#global username to ip mapping
g_proc_list = [] 	#global list of open process to be cleared at end.
disconnect_thresh = 1	#Threshold after which we assume node to be dead.
ssid = sys.argv[1]
time_list = [0,0]

try:
	#mac = "10."+str(random.randint(1,255)) +"."+ str(random.randint(1,255)) +"."+ str(random.randint(1,255))
	mac = generate_ip()
	
	op_dict = {1:create,2:connect}

	#create or join network
	print("1. Create\n2. Connect")
	op = int(input("Choose an option: "))
	op_dict[op]()
	
	#run to see if the given neighbours exist
	run_neighbour_exist()

	# run Server.py in the background to listen to a port and service information
	service_username_dir()

	#menu generation for the program
	menu_generate()

	print("Main Exiting")

except KeyboardInterrupt:
	print("Keyboard Interupt Detected. Main Exiting")	

finally:
	
	for proc in g_proc_list:
		proc.kill()
	subprocess.call(["./clear.sh",mac], stdout=ERROR_FILE, stderr=ERROR_FILE)
	#exit code here
	
	ERROR_FILE.close()
	STAT_FILE.close()

	print("STATISTICS")
	print("Time to Connect to the Network: "+str(time_list[0]))
	print("Time to Transfer files to Recipients: "+str(time_list[1]))
	




