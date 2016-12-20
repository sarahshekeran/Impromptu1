#!/bin/sh

ERROR() {
	echo "fail"
	exit 1
}

mesh_if=$1

#Commands

#Delete mesh_if
sudo iw dev $mesh_if del

#Enable network-manager
sudo service network-manager start || ERROR


