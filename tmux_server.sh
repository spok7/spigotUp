#!/bin/bash
tmux new -d -s mcserver 
tmux send-keys -t mcserver "bash $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/run_server.sh" C-m
