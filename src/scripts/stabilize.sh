#!/bin/bash

# Stabilization for nodes running on different machines, with M = 20

./taco stabilize
./taco stabilize
./taco stabilize
./taco stabilize
./taco stabilize
./taco stabilize

for i in `seq 1 22`;
do
  ./taco fix_finger
done  
