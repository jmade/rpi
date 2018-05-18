sudo bash /home/pi/Ambilight/Controls/S300/power.sh
echo 'on 0' | cec-client RPI -s
echo 'tx 1F:82:10:00' | cec-client RPI -s