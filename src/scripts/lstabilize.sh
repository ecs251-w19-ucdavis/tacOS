#!/bin/bash

# Stabilization for nodes running on the same machine on port 8000 and 5000, with M = 20

PORT=5000 python3 ./taco create_ring
PORT=8000 python3 ./taco join 127.0.1.1 5000

PORT=8000 python3 ./taco stabilize
PORT=5000 python3 ./taco stabilize

for i in `seq 1 22`;
do
  PORT=8000 python3 ./taco fix_finger
  PORT=5000 python3 ./taco fix_finger
done  

#PORT=8000 python3 taco.py disperse ./cache/IMG_20190101_123952_e.jpg 4
