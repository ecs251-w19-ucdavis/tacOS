#!/bin/bash

python3 node.py > /dev/null &
python3 node.py 3000 > /dev/null &
python3 node.py 4000 > /dev/null &
python3 node.py 5000 > /dev/null & 
python3 node.py 6000 > /dev/null & 
python3 node.py 7000 > /dev/null & 
python3 node.py 9000 > /dev/null & 
python3 node.py 10000 > /dev/null &
python3 node.py 11000 > /dev/null &
python3 node.py 12000 > /dev/null &
python3 node.py 13000 > /dev/null &
python3 node.py 14000 > /dev/null &
python3 node.py 15000 > /dev/null &
python3 node.py 16000 > /dev/null &
python3 node.py 17000 > /dev/null &
python3 node.py 18000 > /dev/null &

echo -e "\n================ For 2 Nodes ================="
PORT=8000 python3 ./taco create_ring
PORT=3000 python3 ./taco join 127.0.1.1 8000

PORT=8000 python3 ./taco stabilize > /dev/null
PORT=3000 python3 ./taco stabilize > /dev/null

echo 'fixing fingers'
for i in `seq 1 22`;
do
  PORT=8000 python3 ./taco fix_finger > /dev/null
  PORT=3000 python3 ./taco fix_finger > /dev/null
done 

time PORT=8000 python3 ./taco disperse ./test_files/supernatural-s14e15-720.mp4 10
echo -e "\n"
time PORT=8000 python3 ./taco pull supernatural-s14e15-720.mp4.td

rm -rf ./cache
rm *.mp4*


echo -e "\n================ For 4 Nodes ================="
PORT=4000 python3 ./taco join 127.0.1.1 8000
PORT=5000 python3 ./taco join 127.0.1.1 8000

PORT=8000 python3 ./taco stabilize > /dev/null
PORT=3000 python3 ./taco stabilize > /dev/null
PORT=4000 python3 ./taco stabilize > /dev/null
PORT=5000 python3 ./taco stabilize > /dev/null

for i in `seq 1 22`;
do
  PORT=8000 python3 ./taco fix_finger > /dev/null
  PORT=3000 python3 ./taco fix_finger > /dev/null
  PORT=4000 python3 ./taco fix_finger > /dev/null
  PORT=5000 python3 ./taco fix_finger > /dev/null
done 

time PORT=8000 python3 ./taco disperse ./test_files/supernatural-s14e15-720.mp4 10
echo -e "\n"
time PORT=8000 python3 ./taco pull supernatural-s14e15-720.mp4.td

rm -rf ./cache
rm *.mp4*

echo -e "\n================ For 8 Nodes ================"
PORT=6000 python3 ./taco join 127.0.1.1 8000
PORT=7000 python3 ./taco join 127.0.1.1 8000
PORT=9000 python3 ./taco join 127.0.1.1 8000
PORT=10000 python3 ./taco join 127.0.1.1 8000

PORT=10000 python3 ./taco stabilize > /dev/null
PORT=9000 python3 ./taco stabilize > /dev/null
PORT=3000 python3 ./taco stabilize > /dev/null
PORT=4000 python3 ./taco stabilize > /dev/null
PORT=5000 python3 ./taco stabilize > /dev/null
PORT=6000 python3 ./taco stabilize > /dev/null
PORT=7000 python3 ./taco stabilize > /dev/null
PORT=8000 python3 ./taco stabilize > /dev/null

for i in `seq 1 22`;
do
  PORT=10000 python3 ./taco fix_finger > /dev/null
  PORT=9000 python3 ./taco fix_finger > /dev/null
  PORT=3000 python3 ./taco fix_finger > /dev/null
  PORT=4000 python3 ./taco fix_finger > /dev/null
  PORT=5000 python3 ./taco fix_finger > /dev/null
  PORT=6000 python3 ./taco fix_finger > /dev/null
  PORT=7000 python3 ./taco fix_finger > /dev/null
  PORT=8000 python3 ./taco fix_finger > /dev/null
done 

time PORT=8000 python3 ./taco disperse ./test_files/supernatural-s14e15-720.mp4 10
echo -e "\n"
time PORT=8000 python3 ./taco pull supernatural-s14e15-720.mp4.td

rm -rf ./cache
rm *.mp4*

echo -e "\n================ For 16 Nodes ================"
PORT=11000 python3 ./taco join 127.0.1.1 8000
PORT=12000 python3 ./taco join 127.0.1.1 8000
PORT=13000 python3 ./taco join 127.0.1.1 8000
PORT=14000 python3 ./taco join 127.0.1.1 8000
PORT=15000 python3 ./taco join 127.0.1.1 8000
PORT=16000 python3 ./taco join 127.0.1.1 8000
PORT=17000 python3 ./taco join 127.0.1.1 8000
PORT=18000 python3 ./taco join 127.0.1.1 8000

PORT=3000 python3 ./taco stabilize > /dev/null
PORT=4000 python3 ./taco stabilize > /dev/null
PORT=5000 python3 ./taco stabilize > /dev/null
PORT=6000 python3 ./taco stabilize > /dev/null
PORT=7000 python3 ./taco stabilize > /dev/null
PORT=8000 python3 ./taco stabilize > /dev/null
PORT=9000 python3 ./taco stabilize > /dev/null
PORT=10000 python3 ./taco stabilize > /dev/null
PORT=11000 python3 ./taco stabilize > /dev/null
PORT=12000 python3 ./taco stabilize > /dev/null
PORT=13000 python3 ./taco stabilize > /dev/null
PORT=14000 python3 ./taco stabilize > /dev/null
PORT=15000 python3 ./taco stabilize > /dev/null
PORT=16000 python3 ./taco stabilize > /dev/null
PORT=17000 python3 ./taco stabilize > /dev/null
PORT=18000 python3 ./taco stabilize > /dev/null

for i in `seq 1 22`;
do
  PORT=3000 python3 ./taco fix_finger > /dev/null
  PORT=4000 python3 ./taco fix_finger > /dev/null
  PORT=5000 python3 ./taco fix_finger > /dev/null
  PORT=6000 python3 ./taco fix_finger > /dev/null
  PORT=7000 python3 ./taco fix_finger > /dev/null
  PORT=8000 python3 ./taco fix_finger > /dev/null
  PORT=9000 python3 ./taco fix_finger > /dev/null
  PORT=10000 python3 ./taco fix_finger > /dev/null
  PORT=11000 python3 ./taco fix_finger > /dev/null
  PORT=12000 python3 ./taco fix_finger > /dev/null
  PORT=13000 python3 ./taco fix_finger > /dev/null
  PORT=14000 python3 ./taco fix_finger > /dev/null
  PORT=15000 python3 ./taco fix_finger > /dev/null
  PORT=16000 python3 ./taco fix_finger > /dev/null
  PORT=17000 python3 ./taco fix_finger > /dev/null
  PORT=18000 python3 ./taco fix_finger > /dev/null
done 

time PORT=8000 python3 ./taco disperse ./test_files/supernatural-s14e15-720.mp4 10
echo -e "\n"
time PORT=8000 python3 ./taco pull supernatural-s14e15-720.mp4.td

rm -rf ./cache
rm *.mp4*

pkill -f node.py
