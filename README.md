#Impromptu

This project implements a way to provide file transfer between two or more remote hosts without the use of pendrives i.e. via an Adhoc network

##How to Run the Program
Give execute permission to init.sh
	#chmod +x init.sh
Run init.sh
	#./init.sh
Run Main.py
	#python Main.py <ssid>

##Pre-Requisites
The program depends on the following libraries which must be installed prior to running the code:
-Linux
-python2
-tkinter
	#sudo apt-get install python-tk

##Features

- Creates network and connects to it
- Scan the network for neighbour nodes
- Identify neighbours when a node joins the network or leave the network
- keep dynamic list of neighnours
- service username and directory on query
- set up public and private keys for ssh on each host for key based authentication and copy public keys to all neighbours
- set up scp file transfer to multiple neighbours
- collect statistics of item taken to connect and to transfer files

##Files

-init.sh: Script to give permissions to following files.
-Main.py: Main code
-connect.sh: Script to scan for an ad-hoc.
-create.sh: Create an ad-hoc.
-TimerThread.py: Thread Class which calls function at particular intervals.
-monitor.sh: Script to fetch IPs from arp table.
-clear_arp.sh: Clear arp table.
-clear.sh: Script to restore previous settings and delete log files.
-Server.py: Python code that services the hosts username and directory
-Client.py: Python code that queries a host for its username and password
-send_ssh.sh: Script that checks whether remote login without password authentication is possible

OUTPUT FILES
-log.txt: All stderr contents.
-mon_result.txt: IPs returned from monitor.sh
-Statistics.txt: File containing timestamped values of tiem taken to connect and to transfer files

	
	
