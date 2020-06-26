#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
##########################################################################
# File Name: efig.py
# Author: stubborn vegeta
# Created Time: 2020年06月25日 星期四 18时54分06秒
##########################################################################
import os
from subprocess import call
import argparse

if not os.path.exists("images"):
    os.makedirs("images")

parser = argparse.ArgumentParser(description='extact_image_from_pdf')
parser.add_argument('--inputfile', '-i', help='input your pdf file',required=True)
args = parser.parse_args()

output = args.inputfile[0:-4]
call(['pdfimages', '-png', args.inputfile, 'images/'+output])

