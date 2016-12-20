#!/bin/sh


ERROR() {
	echo "fail"
	exit 1
}

chmod +x Main.py TimerThread.py monitor.sh connect.sh create.sh clear.sh Client.py key_gen.sh Server.py ssh_send.sh clear_arp.sh

#find adapter	
wifi_if=`sudo iw dev | grep Interface | awk '{print $2}'` || ERROR 

sudo su -c "echo 1 > /proc/sys/net/ipv4/conf/$wifi_if/arp_accept"

ssh-keygen -t rsa || ERROR

ssh-add -D|| ERROR
ssh-add || ERROR

sudo fuser -k 50006/tcp



