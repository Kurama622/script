#!/bin/bash

returnPath=`udisksctl mount --block-device "/dev/sdb1" --no-user-interaction | grep -o '/run.*'`

cd $returnPath

