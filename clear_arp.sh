#!/bin/sh


ERROR() {
	echo "fail"
	exit 1
}

#find adapter	
wifi_if=`sudo iw dev | grep Interface | awk '{print $2}'` || ERROR 

sudo ip link set $wifi_if arp off || ERROR

sudo ip link set $wifi_if arp on || ERROR

