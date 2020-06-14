#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
##########################################################################
# File Name: pdf2jpg.py
# Author: stubborn vegeta
# Created Time: 2020年06月14日 星期日 23时17分25秒
##########################################################################
import tempfile
import argparse
import os
from pdf2image import convert_from_path,convert_from_bytes
 
#以下三种方式都可以读取文件，第三种最好
# image = convert_from_path("./")

# image = convert_from_bytes(open('./csp2nn.pdf', 'rb').read())
# inputfile = input()
# outfile = input()
parser = argparse.ArgumentParser(description='pdf2image')
parser.add_argument('--inputfile', '-i', help='input your pdf file',required=True)
parser.add_argument('--outfolder', '-f', help='set your image\'s path', required=True)
parser.add_argument('--outfile', '-o', help='set your image\'s name', default="out")
args = parser.parse_args()

with tempfile.TemporaryDirectory() as path:
    image_from_path = convert_from_path(args.inputfile, dpi=400, fmt='png',output_folder=args.outfolder,output_file=args.outfile)

