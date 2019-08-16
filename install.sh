#!/bin/bash

# This script will help you to install dependencies, spython and container-diff
# After install, you can use the provided extract.py scripts. You should have
# pip installed before running it.

exists () {
    type "$1" >/dev/null 2>/dev/null
}

################################################################################
# Step 1: spython
################################################################################

## To Parse Dockerfile (Singularity Python)

if [ ! -x "$(which spython)" ] ; then

    echo "Singularity python not found on path, installing with pip.";
    if [ ! -x "$(which pip)" ] ; then
        echo "pip is required to install dependencies.";
        exit 1;
    fi

    if [ ! -f "requirements.txt" ]; then
        echo "requirements.txt not found, return to repository root.";
        exit 1;
    else
        pip install -r requirements.txt;
    fi
else
    echo "Singularity Python is installed";
fi

## Container Diff 

# If container-diff not on PATH, get it

if [ ! -x "$(which container-diff)" ] ; then
    echo "Container diff not found on PATH! Downloading to /tmp"
    curl -LO https://storage.googleapis.com/container-diff/latest/container-diff-linux-amd64
    chmod +x container-diff-linux-amd64
    mkdir -p /tmp/bin
    mv container-diff-linux-amd64 /tmp/bin/container-diff
    # export to bash environment
    export PATH="/tmp/bin:${PATH}"
else
    echo "ContainerDiff is installed.";
fi
