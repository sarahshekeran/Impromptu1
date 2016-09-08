#!/bin/sh


ERROR() {
	echo "fail"
	exit 1
}

#find adapter	
wifi_if=`sudo iw dev | grep Interface | awk '{print $2}'` || ERROR 

`arp -n | grep $wifi_if | awk '{ print $1 }' > mon_result.txt` || ERROR

