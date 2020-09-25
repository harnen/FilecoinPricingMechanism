#!/bin/bash

ACC='0x5AB16852FB28d800994cD3a7F69359AD062f497b'
ADDR=$1

cd ../auction/
for item in 5,7,1 10,7,1 15,7,1
do 
	IFS=",";
	set -- $item;
	./client.py item --account $ACC --addr $ADDR --size $1 --duration $2 --price $3 &
done

for bid in 3,3,10 6,3,15 11,3,20 
do 
	IFS=",";
	set -- $bid;
	./client.py bid --account $ACC --addr $ADDR --size $1 --duration $2 --price $3 &
done

wait
