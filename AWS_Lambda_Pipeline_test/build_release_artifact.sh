#!/bin/bash


if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux-gnu"
elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Mac OSX"
elif [[ "$OSTYPE" == "cygwin" ]]; then
        echo "POSIX compatibility layer and Linux environment emulation for Windows"
elif [[ "$OSTYPE" == "msys" ]]; then
        echo "Lightweight shell and GNU utilities compiled for Windows (part of MinGW)"
elif [[ "$OSTYPE" == "win32" ]]; then
        echo "I'm not sure this can happen."
elif [[ "$OSTYPE" == "freebsd"* ]]; then
        echo "freebsd"
else
        echo "Unknown"
fi

# this is b/c pipenv stores the virtual env in a different
# directory so we need to get the path to it
SITE_PACKAGES=$(pipenv --venv)/lib/python3.6/site-packages
echo "Library Location: $SITE_PACKAGES"
DIR=$(pwd)

# Make sure pipenv is good to go
echo "Do fresh install to make sure everything is there"
# pipenv install
