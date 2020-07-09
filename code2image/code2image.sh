#!/bin/bash

FILEPATH=~/scripts/code2image

python3  $FILEPATH/draw.py

/usr/local/texlive/2019/bin/x86_64-linux/xelatex  $FILEPATH/draw.tex

rm *.aux *.log
rm $FILEPATH/draw.tex

python3 ~/scripts/pdf2img.py -i $1/draw.pdf -f $1 -o $2

mv $20001-1.png $2-code.png

rm $1/draw.pdf

feh $2-code.png
