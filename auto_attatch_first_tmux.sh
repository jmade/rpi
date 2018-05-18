#!/bin/bash

function get_session_name()
{
	echo * | tmux ls | awk '{print $1;}' | sed 's/.$//'
}

function performCommand()
{
	cmd="a -t $@"
	echo "tmux $cmd"
	tmux $cmd
}


performCommand $(get_session_name)