#!/bin/bash

count="$1"
counter=1

# Setup GPIO pin 16 to Output.
echo "16" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio16/direction

while [ $counter -le $count ]
do
	echo "1" > /sys/class/gpio/gpio16/value
	sleep 1
	echo "0" > /sys/class/gpio/gpio16/value
	sleep 1
	((counter++))
done

# GPIO Cleanup
echo "16" > /sys/class/gpio/unexport