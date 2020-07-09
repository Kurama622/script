#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
##########################################################################
# File Name: code2image.py
# Author: stubborn vegeta
# Created Time: 2020年07月08日 星期三 23时03分01秒
##########################################################################
import pyperclip

def head():
    return r"""
\documentclass[border=2pt]{standalone}
\usepackage{xeCJK}
\usepackage{listings}
\usepackage{xcolor}
"""
def col():
    return r"""
% 定义可能使用到的颜色
\definecolor{Crimson}{HTML}{DC143C}
\definecolor{DarkGray}{HTML}{808080}
\definecolor{MediumBlue}{HTML}{0000CD}
\definecolor{ForestGreen}{HTML}{228B22}
\definecolor{GoldEnrod}{HTML}{FD971F}
"""
def settings(language):
    if language == 'python':
        return r"""
    \lstset{
        columns=fixed,
        frame=none,                                          % 不显示背景边框
        keywordstyle=[1]\color{Crimson},                     % 设定关键字颜色
        keywordstyle=[2]\bf\color{GoldEnrod},                % 设定关键字颜色
        commentstyle=\it\color{DarkGray},                    % 设置代码注释的格式
        stringstyle=\rmfamily\slshape\color{ForestGreen},    % 设置字符串格式
        showstringspaces=false,                              % 不显示字符串中的空格
        language=python,                                     % 设置语言
        morekeywords= {with, as},
        morekeywords= [2]{seed, stddev, axis, axes, label, color, dtype,n_components,n_dim,figsize, },
        %emph={tf,append, argmax, cast, nn,divide,math,add,matmul,tanh,softmax,norm,moments,transpose,conv2d,pool},
        emph={append,c,},
        emphstyle=\color{MediumBlue}
    }
    """
def body():
    return r"""
\begin{document}
{\setmainfont{DejaVu Sans Mono}                          % 设置代码字体
\begin{lstlisting}
"""+ pyperclip.paste() +"""
\end{lstlisting}}
\end{document}
"""
def to_generate( arch, pathname="file.tex" ):
    with open(pathname, "w") as f: 
        for c in arch:
            print(c)
            f.write( c )
