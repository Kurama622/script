#!/bin/bash
var1=+50
var1=$(($var1 + $(cat /sys/class/backlight/intel_backlight/brightness)))
sudo tee /sys/class/backlight/intel_backlight/brightness <<< $var1

