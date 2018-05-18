#!/bin/sh

echo '|--> Launching Start Ambilight Server Script. |-->'
# 
cd ~/Ambilight
source env/bin/activate
# 
cd ~/rpi_ws281x/python && sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python ~/Ambilight/ambilight_server.py
# 
# cd ~
# python ~/Ambilight/ambilight_server.py
#
echo '|--> Script Complete.               |-->'
echo '|--> It was a pleasure Serving you .|-->'
