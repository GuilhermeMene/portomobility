#!/bin/bash
#
# Check if the argments are passed
if [ $# -eq 0 ]; then
    echo "No arguments are passed." >&2
    exit 1
fi

#Check if the argument is a string
if [[ $1 =~ ^[0-9]+$ ]]; then
    echo "Error: Argument '$1' is an integer, expected a text string." >&2
    exit 1
fi

# Set the env variables
set -a
. $1
set +a

#Check if it's worked
if [ $? -eq 0 ]; then
    echo "The environment was sucessful saved."
else
    echo "The environment cannot be saved."
fi
