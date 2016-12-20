#!/bin/sh


ERROR() {
	echo "fail"
	exit 1
}

SSID=$1
mac=$2

#disable network-manager
`sudo service network-manager stop` || ERROR

#find adapter	
wifi_if=`sudo iw dev | grep Interface | awk '{print $2}'` || ERROR 

`sudo ip link set $wifi_if up` || ERROR

echo `iwlist scan 2>log.txt | grep -e ESSID:\"$SSID\"`|| ERROR
