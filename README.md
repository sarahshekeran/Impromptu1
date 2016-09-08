Ad-Hoc Assignment

-----Pre-Requisite-----
Linux
python2
tkinter
	sudo apt-get install python-tk

----How to RUN-----
1)Give execute permission to init.sh
	chmod +x init.sh
2)Run init.sh
	./init.sh
3)Run Main.py
	python Main.py <ssid>

--------What Works ?----------------

- Creates network and connects to it
- Scan the network for neighbour nodes
- Identify neighbours when a node joins the network or leave the network
- keep dynamic list of neighnours
- service username and directory on query
- set up public and private keys for ssh on each host for key based authentication and copy public keys to all neighbours
- set up scp file transfer to multiple neighbours
- collect statistics of tiem taken to connect and to transfer files

--------What Could Not be Implemented -----------

- interactive interface 
- parallel-ssh and parallel-scp implementation
- reduce network traffic due to pings
- dynamically specifying the dorectory
- handling multiple usernames for a host
- usage of rhosts
- achieve fast speed scp transfer comparable to pendrive transfer
- a way that eleminates password prompt completely for file transfer
- Check if essid corresponds to ad-hoc in the script.
- Change Unencrypted to WPA/PSK.	
- Handle external WiFi Adapters - change iw dev to iwconfig.

----------Files----------------

init.sh			- Script to give permissions to following files.
Main.py 		- Main code
connect.sh 		- Script to scan for an ad-hoc.
create.sh		- Create an ad-hoc.
TimerThread.py  - Thread Class which calls function at particular intervals.
monitor.sh		- Script to fetch IPs from arp table.
clear_arp.sh	- Clear arp table.
clear.sh		- Script to restore previous settings and delete log files.
Server.py 		- Python code that services the hosts username and directory
Client.py 		- Python code that queries a host for its username and password
send_ssh.sh 	- Script that checks whether remote login without password authentication is possible

OUTPUT FILES
log.txt 		- All stderr contents.
mon_result.txt	- IPs returned from monitor.sh
Statistics.txt	- File containing timestamped values of tiem taken to connect and to transfer files

	
-------To-Do--------------
#Todo
	#Check if essid corresponds to ad-hoc in the script.
	#Change Unencrypted to WPA/PSK -------------> IMPORTANT	
	#Handle external WiFi Adapters - change iw dev to iwconfig.
	
