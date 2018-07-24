# -*- coding: utf-8 -*-
"""
Created on Sat May 26 17:43:15 2018

@author: gx
"""



import numpy as np
import matplotlib.pyplot as mp

f=0.01   #100Hz
tp=np.loadtxt(r'C:\Users\gx\Documents\Tencent Files\391059727\FileRecv\新建文本文档.txt',skiprows=7)
tcodnt=tp.shape[0]*f
n=2
mp.figure(figsize=(250,10))
mp.plot(tcodnt[400:],tp[400:,n],'r')
mp.plot(tcodnt[400:],tp[405:,n+4],'b')

#n=2
#mp.figure(figsize=(250,10))
#mp.plot(tcodnt[400:],temp[400:,n],'r')
#mp.plot(tcodnt[400:],forecast[405:,n],'b')