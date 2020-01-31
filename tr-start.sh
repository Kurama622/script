#!/bin/bash

result=$(ps ax|grep -v grep|grep trayer)
if [ "$result" == "" ]; then
  eval  "trayer --transparent true --expand false --edge top --align right --width 20 --height 20 --SetDockType false --tint 0x88888888 &"
else
  eval "killall trayer"
fi
