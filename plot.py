# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 20:35:00 2018

@author: gx
"""
import matplotlib.pyplot as mp
import numpy as np
import os

def cpplot(i):
    mp.figure(figsize=[15,10])
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.subplot(211)
    mp.plot(tcodnt, temp[:,i],color='limegreen')
    mp.title('The Timing Diagram of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.subplot(212)
    mp.plot(added_tcodnt, forecast[:, i], color='orangered')
    mp.title('The %d-Step Forecast Of Signal %d' % ((n_steps+1), i), fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.tight_layout()       
    mp.savefig((str(path)+'\\'+'results'+'\\'+'Timing_Graph_%d'+'.jpg')%i,format='jpg',dpi=1200)
    
def rscplot(i):
    mp.figure(figsize=[15,10])
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.subplot(311)
    mp.plot(tcodnt, rsdlsc[:,i], color='limegreen')
    mp.title('The Residuls After Correction Of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.ylim((-0.03, 0.03))
    mp.yticks(np.arange(-0.03, 0.035, 0.01))
    mp.tick_params(which='both', top=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.subplot(312)
    mp.plot(tcodnt, rsdlpctgc[:,i], color='dodgerblue')
    mp.title('The Residual Percentage After Correction Of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.ylim((-0.6, 0.6))
    mp.yticks(np.arange(-1, 1, 0.2))
    mp.tick_params(which='both', top=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.subplot(313)
    mp.plot(tcodnt, sqrpctgc[:,i], color='orangered')
    mp.title('The Squared Percentage After Correction Of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.ylim((0, 0.4))
    mp.yticks(np.arange(0, 0.5, 0.1))
    mp.tick_params(which='both', top=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.tight_layout()
    mp.savefig((str(path)+'\\'+'results'+'\\'+r'Error_Graph_%d'+'.jpg')%i,format='jpg',dpi=1200)
    
    
def partial_plot(i):
    mp.figure(figsize=[15,5])
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.plot(tcodnt[1000:2000], temp[1000:2000,i],color='limegreen')
    mp.title('The Timing Diagram of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.plot(added_tcodnt[1000:2000], forecast[1005:2005, i], color='orangered')
    mp.title('The %d-Step Forecast Of Signal %d' % ((n_steps+1), i), fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.tight_layout()
    mp.savefig((str(path)+'\\'+'results'+'\\'+'Partial_Timing_Graph_%d'+'.jpg')%i,format='jpg',dpi=2000)
    
    
    
if __name__=='__main__':
    path=r'D:\C盘备份\Tencent Files\391059727\FileRecv\xiezhiliang'
    name=r'xiezhiliang\1\三分之一'
    mat = np.loadtxt(path+r'\realtimerecord1.txt', skiprows=0)
    # 采集频率
    f1 = 0.01   # 100Hz
    # 信号源数量
    mat=mat[:,1:]
    l = ((mat.shape)[1])/2##number of elements , for data without time information
    l=int(l)
    tcodnt = np.array(list(range(mat.shape[0]))) * f1
    tcodnt=tcodnt[5:]
    added_tcodnt=tcodnt
    temp=mat[5:,:4]
    forecastc=mat[:-5,4:]
    forecast=mat[:-5,4:]
    n_steps=4
    mean_plate_n=20
    platevalue=np.vstack([temp.max()*e/e for e in temp[0:int(mean_plate_n/2)]])
    for i in range(int(mean_plate_n/2), temp.shape[0]-int(mean_plate_n/2)):
        local_max=np.matrix(list(map(lambda x:(abs(temp[i-int(mean_plate_n/2):i+int(mean_plate_n/2)+1,x])).max(),range(temp.shape[1]))))
        platevalue=np.vstack([platevalue,local_max])
    for i in range(temp.shape[0]-int(mean_plate_n/2),temp.shape[0]):
        platevalue=np.vstack([platevalue,temp.max()*temp[i]/temp[i]])
    
    
    rsdlsc=(forecastc-temp) 
    rsdlpctgc=rsdlsc/platevalue#percentage
    sqrpctgc=np.array(rsdlpctgc)*np.array(rsdlpctgc)
    square=np.sum(np.array(rsdlsc[:,3])*np.array(rsdlsc[:,3]))/np.sum(np.array(temp[:,3])*np.array(temp[:,3]))
    if not os.path.exists(path+'\\'+'results'):
            os.makedirs(path+'\\'+'results')
    for i in range(l):
            cpplot(i)
    for i in range(l):
            rscplot(i)
    partial_plot(3)#selected channel
    
    
    