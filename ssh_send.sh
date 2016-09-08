#!/bin/sh
ERROR() {
	echo "fail"
	exit 1
}

SUCCESS(){
	echo "success"
	exit 0 
}


USER=$1
IP=$2

#copy key to remote-host
if ssh $USER@$IP -o BatchMode=yes exit; [ $? -eq 255 ]
then
	ERROR
else
	SUCCESS
fi
