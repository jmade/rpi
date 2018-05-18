#!/bin/sh

# COLORS
_reset=$(tput sgr0)
_green=$(tput setaf 76)
_purple=$(tput setaf 171)
_red=$(tput setaf 1)
_tan=$(tput setaf 3)
_blue=$(tput setaf 38)
_bold=$(tput bold)
_underline=$(tput sgr 0 1)




function _success()
{
    printf "${_green}✔ %s${_reset}\n" "$@"
}

function _bold()
{
	printf "${_bold}%s${_reset}\n" "$@"
}

function _error()
{
	printf "${_red}%s${_reset}\n" "$@"
}



function setupForSSH()
{
	echo "Setting up SSH..."
	cd $HOME 
	mkdir .shh
	cd .ssh/
	touch authorized_keys
	_success "SSH Setup Complete"
}

function systemUpgrades()
{
	echo "System Upgrades"
	sudo apt-get -y update
	sudo apt-get -y upgrade
	_success "System Upgrade Success!"
}

function installPythonHeaders()
{
	echo "Python Header Files."
	sudo apt-get -y install python2.7-dev python3-dev
	
}

function installPIP()
{
	echo "Install pip Python package manager"
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python get-pip.py
}


function install_tmux()
{
	echo "Installing tmux"
	sudo apt-get -y update
	sudo apt-get -y install tmux
	_success "tmux Installed!"
}


function installLEDLib()
{
	printf "Installing ${_blue}RPI_WS281X${_reset} LED Library\n"
	sudo apt-get install build-essential python-dev git scons swig

	cd ~
	git clone https://github.com/jgarff/rpi_ws281x.git
	cd rpi_ws281x
	scons

	cd python
	sudo python setup.py install -y
}


function installh264()
{
	cd ~
	git clone git://git.videolan.org/x264
	cd x264
	./configure --host=arm-unknown-linux-gnueabi --enable-static --disable-opencl
	make -j4
	sudo make install
	_success "h.264 Installed!"
}

function install_ffmpeg()
{
	cd ~
	git clone git://source.ffmpeg.org/ffmpeg.git
	cd ffmpeg
	./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree
	make -j4
	sudo make install
	_success "ffmpeg Installed!"
}


function install_psutil()
{
	pip install psutil
	_success "psutil Installed!"
}


function install_lirc()
{
	sudo apt-get install lirc liblircclient-dev -y
	_success "lirc Installed!"
}


function install_rabbitmq()
{
	sudo apt-get install rabbitmq-server -y
	_success "rabbitmq-server Installed!"
}



function _main()
{
	_bold "-~- Starting Setup Script -~-"
	install_rabbitmq
	_success "-~- Finished Install Script -~-"
}


_main

