#Impromptu

This project implements a way set up a mesh network and exchange messages over multiple hops.

##How to Run the Program
- Give execute permission to both files, create.sh and delete,sh
```
chmod +x init.sh
```
- Run ./create.sh
```
./create.sh <mesh interface> <mesh id> <mesh IP> <subnet mask> <mesh broadcast IP>
```
- Run ./delete.sh ti bring bag the previous system configuration
```
./delete.sh <mesh interface>
```

##Files

- create.sh: Creates a logcal mesh interface and assignes the IP and broadcast addresses to it.
- delete.sh: Returns configuration to the previous state by undoing the changes made by create.sh
- connect.sh: Script to scan for an ad-hoc.


	
	
