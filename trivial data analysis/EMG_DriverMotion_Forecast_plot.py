# -*- coding: utf-8 -*-
"""
Created on Sat May 26 15:53:43 2018

@author: gx
"""

import numpy as np
import matplotlib.pyplot as plt


path=r'C:\Users\gx\Documents\Tencent Files\391059727\FileRecv\realtimerecord(1).txt'
data=np.loadtxt(path)
data=data[50:500]
size=data.shape[0]
t=np.arange(0,size,1)
y_range=np.array([0,1200,500,700,600,6100,6100,6100,6100,1200,500,700,600,6100,6100,6100,6100])
tick_range=np.array([0,100,100,100,100,500,500,500,500,100,100,100,100,500,500,500,500])
#for i in range(1,data.shape[1]):
#    mp.figure(figsize=(10,5))
#    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
#    mp.plot(t,data[:,i], color='limegreen')
#    mp.ylim((0, y_range[i]))
#    mp.yticks(np.arange(0, y_range[i], tick_range[i]))
#    #mp.tick_params(which='both', top=True, labelsize=10)
#    mp.grid(linestyle=':')
#    mp.tight_layout()
#    mp.show()
#
#mp.figure(figsize=(10,5))
#mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
#mp.plot(t,data[:,i], color='limegreen')
#mp.ylim((0, y_range[2]))
#mp.yticks(np.arange(0, y_range[2], tick_range[2]))
##mp.tick_params(which='both', top=True, labelsize=10)
#mp.grid(linestyle=':')
#mp.tight_layout()
#
#
#
##mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
#mp.plot(t,data[:,i], color='limegreen')
#mp.ylim((0, y_range[10]))
#mp.yticks(np.arange(0, y_range[10], tick_range[10]))
##mp.tick_params(which='both', top=True, labelsize=10)
#mp.grid(linestyle=':')
#mp.tight_layout()
#mp.show()

plt.plot(t,data[:,2],color='r')
plt.plot(t,data[:,10],color='b')

