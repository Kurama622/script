#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
##########################################################################
# File Name: pdf2jpg.py
# Author: stubborn vegeta
# Created Time: 2020年06月14日 星期日 23时17分25秒
##########################################################################
import tempfile
import argparse
from pdf2image import convert_from_path,convert_from_bytes
 
parser = argparse.ArgumentParser(description='pdf2image')
parser.add_argument('--inputfile', '-i', help='input your pdf file',required=True)
parser.add_argument('--dpi', '-d', help='input your image dpi',default=400)
parser.add_argument('--outfolder', '-f', help='set your image\'s path', required=True)
parser.add_argument('--outfile', '-o', help='set your image\'s name', default="out")
args = parser.parse_args()

with tempfile.TemporaryDirectory() as path:
    image_from_path = convert_from_path(args.inputfile, dpi=args.dpi, fmt='png',output_folder=args.outfolder,output_file=args.outfile)

