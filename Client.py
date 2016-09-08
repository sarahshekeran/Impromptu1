import socket
from time import sleep
import sys

IP = sys.argv[1]

mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocket.connect(( IP, 50006))
mySocket.send("dummydata")
#sleep(2)
username = mySocket.recv(1024)
print (username)
mySocket.close()
