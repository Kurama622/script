#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
##########################################################################
# File Name: draw.py
# Author: stubborn vegeta
# Created Time: 2020年07月08日 星期三 23时10分02秒
##########################################################################
import sys
from code2image import *

code = [
    head(),
    col(),
    settings('python'),
    body(),
        ]
def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(code, namefile + '.tex')

if __name__ == "__main__":
    main()
