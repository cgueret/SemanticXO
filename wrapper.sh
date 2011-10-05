#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${DIRECTORY}"
cd ${DIRECTORY}

# We want to use an hashes + bdb backend for the data
FLAGS="-s hashes -t \"hash-type='bdb',dir='/var/lib/redstore'\" "

# Start the process
${DIRECTORY}/redstore ${FLAGS} >/dev/null &



