#!/bin/sh


ERROR() {
	echo "fail"
	exit 1
}

ip=$1

#find adapter	
wifi_if=`sudo iw dev | grep Interface | awk '{print $2}'` || ERROR 

#IP addr to be replaced with the computed value.
`sudo ip addr del $ip/8 broadcast 10.255.255.255 dev $wifi_if` || ERROR
`sudo service network-manager start` || ERROR
`sudo rm log.txt` || ERROR
`sudo rm mon_result.txt` || ERROR

sudo fuser -k 50006/tcp || ERROR

echo 'done'
