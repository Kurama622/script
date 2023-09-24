#!/bin/bash
var1=+50
var1=$(($var1 + $(cat /sys/class/backlight/amdgpu_bl0/brightness)))
sudo tee /sys/class/backlight/amdgpu_bl0/brightness <<< $var1

