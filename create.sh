#!/bin/sh


ERROR() {
	echo "fail"
	exit 1
}

SSID=$1
mac=$2

#commands
#disable network-manager
`sudo service network-manager stop` || ERROR

#find adapter	
wifi_if=`sudo iw dev | grep Interface | awk '{print $2}'` || ERROR 

`sudo ip link set $wifi_if down` || ERROR

#Todo - change channel

`sudo iwconfig  $wifi_if mode ad-hoc` || ERROR

`sudo iwconfig  $wifi_if essid $SSID` || ERROR

#Todo - WEP key

#mac=`ip link show $wifi_if | grep link/ether | awk '{ print $2 }'`

#Todo convert MAC to hex

`sudo ip addr add $mac/8 broadcast 10.255.255.255 dev $wifi_if` || ERROR

`sudo ip link set $wifi_if up` || ERROR
