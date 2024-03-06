#!/bin/bash

# Declare environment variables
export CAMERA_NAME=/base/soc/i2c0mux/i2c@1/ov5647@36
export MICROPHONE_ID=0,0
export PORTNUMBER=8000

mkdir -p recordings

pip3 install --ignore-installed -r requirements.txt

python3 main.py
