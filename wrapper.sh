#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${DIRECTORY}"
cd ${DIRECTORY}

# We want to use a sqlite backend for the data
FLAGS="-s sqlite "

# Check if the database need to be created
if [ ! -f redstore ]; then
	FLAGS="${FLAGS} -n "
fi

# Start the process
./redstored ${FLAGS} >/dev/null &



