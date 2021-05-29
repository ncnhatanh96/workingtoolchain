#!/bin/bash

apt update

if ! command -v python3.8 &> /dev/null
then
    apt install python3.8
fi

if ! command -v pylint &> /dev/null
then
    apt install pylint
    cp .pylintrc ~/
fi

if ! command -v pip3.8 &> /dev/null
then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.8 get-pip.py
fi

pip3.8 install jira
pip3.8 install DateTime
