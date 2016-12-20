#!/bin/sh

ERROR() {
	echo "fail"
	exit 1
}

mesh_if=$1
mesh_id=$2
mesh_ip=$3
netmask=$4
broadcast_ip=$5

#Commands

#Disable network-manager
sudo service network-manager stop || ERROR

#Find adapter	
wifi_if=`sudo iw dev | grep Interface | awk '{print $2}'` || ERROR 

#Create mesh interace on wifi dev
sudo iw dev $wifi_if interface add $mesh_if type mesh || ERROR

#Set IP.
sudo ip addr add $mesh_ip/$netmask broadcast $broadcast_ip dev $mesh_if

#Set down wifi_if and turn on mesh_if.
sudo ip link set $wifi_if down || ERROR
sudo ip link set $mesh_if up || ERROR

#Todo - change channel

sudo iw dev $mesh_if mesh join $mesh_id || ERROR

sudo iw dev $mesh_if get mesh_param || ERROR

sudo iw dev $mesh_if station dump || ERROR

#Todo - WPA_supplicant
