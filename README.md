# tacOS
tacOS is a completely P2P distributed file service that is built on Chord DHash. tacOS comes with automatic stabilization of the network for when nodes join and leave, and offers great load balancing and fast lookups without the need of a central master.

Chord works by placing each node on a conceptual ring where their locations are hashed values of their IP Address and Port. They files/segments are also hashed with the same function to determine which node they will be stored in.

## Table of Contents
* [Startup](#startup)
  + [On Local](#on-local)
  + [Using Docker](#using-docker)
* [Usage](#usage)
  + [1. Creating a Ring](#1-creating-a-ring)
  + [2. Joining a Ring](#2-joining-a-ring)
  + [3. Distributing Files](#3-distributing-files)
  + [4. Retrieving Files](#4-retrieving-files)
* [Other Commands](#other-commands)
* [Advanced](#advanced)

## Startup
The application requires python version 3 or later. All requests within a node will be sent using the client application `taco` to the node.py server of the same node.
### **On Local**

To start, run `python3 node.py [port]` in the [src/](src/) directory. The port argument is optional, and when omitted will cause the node to listen on the default port 8000. Note that when running on local, you have to provide a different port for each node you plan on running.

Requests will be sent to each node by prepending "PORT" environment variable with the port value of the node the command is intended for. Example for 2 nodes:
```bash
# Run first node on port 8000
python3 node.py

# Run second node on port 5000
python3 node.py 5000

# Pinging the first node
PORT=8000 python3 taco ping

# Pinging the second node
PORT=5000 python3 taco ping
```

### **Using Docker**
Run in the root directory of the tacOS application. Needs docker-compose.
```bash
docker build . -t taco:latest
docker-compose up
```

After all container are up and running, attach each terminal window to the each of the 4 node containers:
```bash
# List all running containers
docker container ls
# -> You should see 4 containers running taco:latest image

# Attach terminal window to docker container
docker container exec -it <container-id> /bin/bash

# Test if the server is running
./taco ping
# -> You should get running status with IP and Port on which server is listening
```
    
## Usage
Like mentioned earlier, all requests need to be sent via the taco file as we will see below.

The commands shown below are for inside the docker, therefore . If you're running it on a standalone machine, depending on what your python binary is called, you might have to prepend the the `python` word and `PORT` environment variable wherever required as shown in [On Local](#on-local). If each node is running on a seperate machine, you can just export the `PORT` environment variable once.

### **1. Creating a Ring**
A node creates a ring for other nodes to join and form a network. No node on the ring is superior to the other.
```bash
./taco create_ring
```

### **2. Joining a Ring**
Other nodes join a ring by requesting a node that is already on the ring. The IP and PORT of the node on the ring is needed to send a request. You can find those details by running `./taco ping` on the node that is on the ring.
```bash
./taco join <IP> <PORT>
```

### **3. Distributing Files**
Files are distributed accross different nodes on the ring. The distribution takes place by splitting the file into the number of segments specified by the second argument to the disperse command. If no argument is provided, the entire file is sent off to the appropriate node.
```bash
./taco disperse <FILE> <NUM OF SEGMENTS>
```

After the dispersion/distribution of the file, a `.td` file will be created that can be used to retrieve the distributed file as shown in the next step.

### **4. Retrieving Files**
Files are retrieved using `pull` command and the `.td` file corresponding to the file you want to retrieve.
```bash
./taco pull <.td FILE>
```

## Other Commands
Other commands you might use for various purposes can be found by typing `./taco help`. You can find a few below:
* `get_hash`: Get the hashed value/position of the node on the ring.
* `get_successor`: Get the IP and PORT of the immediate successor on the ring.
* `get_finger`: Get finger table of the node that has a list of successors at exponentially growing distances.
* `get_predecessor`: Get the IP and PORT of the immediate predecessor on the ring.

## Advanced
The [utils.py](src/utils.py) file has the value of M that decides the number of buckets on the ring, and the various hash functions that can be used for the hashing of files and the nodes. Choosing of appropriate hash functions and M is vital for ideal working of Chord, and may have to chage depending on what the application is being used for. The chosen hash function can be changed by changing the value of `main_func` variable to the name of the available function in the dictionary.
