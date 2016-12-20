import select 
import socket 
import sys 
import subprocess
import os

host = sys.argv[1]
port = 50006 
backlog = 3 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host,port)) 
server.listen(backlog) 
input = [server, sys.stdin]
running = 1

dir_name  = "Files"
username = ""
path_name = ""


p = subprocess.Popen(["whoami"], stdout=subprocess.PIPE)
username, err = p.communicate();
username=username.strip("\n")
p.wait()

if not os.path.exists(dir_name):
	os.makedirs(dir_name)


path_name = os.getcwd()
path_name+="/"+dir_name+"\n"

while running: 
    inputready,outputready,exceptready = select.select(input,[],[]) 
    
    for s in inputready: 
	
        if s == server: 
            # handle the client socket 
            client, address = server.accept()
            input.append(client)

        elif s == sys.stdin: 
		pass

        else: 
		# handle all other sockets
		#data = client.recv(100)			
			
		if username and path_name: 
			s.send(username+";"+path_name)

		s.close()
		input.remove(s)

server.close()
