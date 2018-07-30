# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 20:35:00 2018

@author: gx
"""
import matplotlib.pyplot as mp
import numpy as np
import os
import shutil
import sys
import traceback
import time
import scipy.stats
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl  













def ploter(path,name):
    mat = np.loadtxt(path+'\\'+name, skiprows=400)
    # 采集频率
    f1 = 0.01   # 100Hz
    # 信号源数量
    mat=mat[:,1:]
    l = ((mat.shape)[1])/2##number of elements , for data without time information
    l=int(l)
    tcodnt = np.array(list(range(mat.shape[0]))) * f1
    #delete head data of original data and tail data of prediction data for accuracy test
    tcodnt=tcodnt[5:]
    added_tcodnt=tcodnt
    temp=mat[5:,:4]
    forecastc=mat[:-5,4:]
    forecast=mat[:-5,4:]
    n_steps=4
    mean_plate_n=20
    platevalue=np.vstack([np.full(temp[0].shape,temp.max(),dtype=float) for e in temp[0:int(mean_plate_n/2)]])
    for i in range(int(mean_plate_n/2), temp.shape[0]-int(mean_plate_n/2)):
        local_max=np.matrix(list(map(lambda x:(abs(temp[i-int(mean_plate_n/2):i+int(mean_plate_n/2)+1,x])).max(),range(temp.shape[1]))))
        platevalue=np.vstack([platevalue,local_max])
    for i in range(temp.shape[0]-int(mean_plate_n/2),temp.shape[0]):
        platevalue=np.vstack([platevalue,np.full(temp[0].shape,temp.max(),dtype=float)])
    
    
    rsdlsc=(forecastc-temp) 
    rsdlpctgc=rsdlsc/platevalue#percentage
    sqrpctgc=np.array(rsdlpctgc)*np.array(rsdlpctgc)
    #distance is mormalized by dividing it by the sum of original data square
    distance_normalized=[np.sum(np.array(rsdlsc[:,i])*np.array(rsdlsc[:,i]))/np.sum(np.array(temp[:,i])*np.array(temp[:,i])) for i in range(l)]
    #0<similarity<=1 
    similarity=[1/(1+e) for e in distance_normalized]
    if not os.path.exists(path+'\\'+'results'):
            os.makedirs(path+'\\'+'results')
    partial_plot_for_ahead_interval(0,tcodnt, temp, forecast,added_tcodnt,n_steps,path,rsdlpctgc)
#    for i in range(l):
#            cpplot(i,tcodnt, temp, forecast,added_tcodnt,n_steps,path)
#    for i in range(l):
#            rscplot(i,tcodnt, rsdlsc, rsdlpctgc, sqrpctgc,path)
#    for i in range(l):
#            partial_plot_for_ahead_interval(i,tcodnt, temp, forecast,added_tcodnt,n_steps,path)#selected channel
#    for i in range(l):
#            partial_plot_for_accuracy_test(i,tcodnt, temp, forecast,added_tcodnt,n_steps,path)#selected channel
    out=open(path+'\\'+'results'+'\\'+'output.txt','a')
    out.write('normalized distance:')
    out.write('\n')
    out.write(str(distance_normalized))
    out.write('\n')
    out.write('similarity:')
    out.write('\n')
    out.write(str(similarity))
    out.write('\n')
    out.close()

def cpplot(i,tcodnt, temp, forecast,added_tcodnt,n_steps,path):
    mp.figure(figsize=[20,10])
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    #mp.subplot(211)
    mp.plot(tcodnt, temp[:,i],color='limegreen')
    #mp.title('The Timing Diagram of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.ylim(0,np.amax(temp[:,i]))
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    #mp.subplot(212)
    mp.plot(added_tcodnt, forecast[:, i], color='orangered')
    mp.title('The Timing Diagram and The %d-Step Forecast Of Signal %d' % ((n_steps+1), i), fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.tight_layout()       
    mp.savefig((str(path)+'\\'+'results'+'\\'+'Timing_Graph_%d'+'.jpg')%i,format='jpg',dpi=1200)
    
def rscplot(i,tcodnt, rsdlsc, rsdlpctgc, sqrpctgc,path):
    mp.figure(figsize=[20,10])
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.subplot(311)
    mp.plot(tcodnt, rsdlsc[:,i], color='limegreen')
    mp.title('The Residuls After Correction Of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("value", fontsize=12)
    mp.ylim(np.amin(rsdlsc[:,i]),np.amax(rsdlsc[:,i]))
    #mp.yticks(np.arange(-0.03, 0.035, 0.01))
    mp.tick_params(which='both', top=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.subplot(312)
    mp.plot(tcodnt, rsdlpctgc[:,i], color='dodgerblue')
    mp.title('The Residual Percentage After Correction Of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("value", fontsize=12)
    mp.ylim((-0.6, 0.6))
    #mp.yticks(np.arange(-1, 1, 0.2))
    mp.tick_params(which='both', top=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.subplot(313)
    mp.plot(tcodnt, sqrpctgc[:,i], color='orangered')
    mp.title('The Squared Percentage After Correction Of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("value", fontsize=12)
    mp.ylim((0, 0.4))
    #mp.yticks(np.arange(0, 0.5, 0.1))
    mp.tick_params(which='both', top=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.tight_layout()
    mp.savefig((str(path)+'\\'+'results'+'\\'+r'Error_Graph_%d'+'.jpg')%i,format='jpg',dpi=1200)
    
def partial_plot_for_ahead_interval(i,tcodnt, temp, forecast,added_tcodnt,n_steps,path,rsdlpctgc):
    mp.figure(figsize=[8,5])
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.plot(tcodnt[1300:1500], temp[1300:1500,i],color='limegreen')
    mp.title('Partial Graph', fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.ylim(np.amin(temp[1300:1500,i]),np.amax(temp[1300:1500,i]))
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.plot(added_tcodnt[1300:1500], forecast[1305:1505, i], color='orangered')
    #mp.title('(Partial)The Timing Diagram and The %d-Step Forecast Of Signal %d' % ((n_steps+1), i), fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    colorbar(tcodnt, rsdlpctgc,i)
    mp.tight_layout()
    #mp.savefig((str(path)+'\\'+'results'+'\\'+'Partial_Timing_Graph_ahead_%d'+'.jpg')%i,format='jpg',dpi=2000)
 
#not used    
def partial_plot_for_accuracy_test(i,tcodnt, temp, forecast,added_tcodnt,n_steps,path):
    mp.figure(figsize=[15,5])
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.plot(tcodnt[1000:2000], temp[1000:2000,i],color='limegreen')
    mp.title('The Timing Diagram of Signal %d' %i, fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.plot(added_tcodnt[1000:2000], forecast[1000:2000, i], color='orangered')
    mp.title('The %d-Step Forecast Of Signal %d' % ((n_steps+1), i), fontsize=16)
    mp.xlabel('time (s)', fontsize=12)
    mp.ylabel("EMG", fontsize=12)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')
    mp.tight_layout()
    mp.savefig((str(path)+'\\'+'results'+'\\'+'Partial_Timing_accuracy_Graph_%d'+'.jpg')%i,format='jpg',dpi=2000)

def colorbar(T,Y,i):
    mp.figure(figsize=[15,5])
    ax=mp.subplot(111)
    Y=np.array(Y)
    Y=Y[:,i]
    TY=np.vstack([T,Y])
    kde=scipy.stats.gaussian_kde(TY)
    kde.set_bandwidth(bw_method='silverman')
    Z=kde(TY)
    print(Z.shape)
    color=np.vstack([Z,Z])
    color=color[:,0:100]
    im=ax.imshow(color)
    clb=mp.colorbar(im,extend='both')





def process(path_origin):
    finder_father(path_origin)
    
def worker(path,name):
    if os.path.exists(path+'\\'+'results'):
        shutil.rmtree(path+'\\'+'results')
    if not os.path.exists(path+'\\'+'results'):
        os.makedirs(path+'\\'+'results')
    if os.path.exists(path+'\\'+'results'+'\\'+'output.txt'):
        os.remove(path+'\\'+'results'+'\\'+'output.txt')
    mp.close('all')#for memory usage consideration
    ploter(path,name)
        #print(name)
            
def finder(path,files):
    for file in files:
        try:
            path_lower=path+'\\'+file
            folders=os.listdir(path_lower)
            finder(path_lower,folders)
        except NotADirectoryError:
            if file!='realtimerecord.txt':
                continue
#            #rename for every file
#            path_residual=path_lower.lstrip(path_origin)
#            newname=path_residual.replace('\\','_')
#            os.rename(path_lower,path+'\\'+newname)
            #do something
            worker(path,file)
            
def finder_father(path_origin):
    folders=os.listdir(path_origin)
    folders_for_loop=folders.copy()
    for element in folders_for_loop:
        if os.path.isfile(path_origin+'\\'+element):
            folders.remove(element)
    finder(path_origin,folders)
    



    
    
    
if __name__=='__main__':
    t=time.time()
#    try:
#    path_origin=r'D:\C盘备份\Tencent Files\391059727\FileRecv\谢志亮'
#    process(path_origin)    
#    except Exception:
#        e=Exception
#        print('error',e,'-'*64,traceback.print_exc(file=sys.stdout),'-'*64)
    name=r'realtimerecord.txt'
    path=r'D:\C盘备份\Tencent Files\391059727\FileRecv\谢志亮\1\三分之一'
    worker(path,name)
    deltat=time.time()-t
    print('time:',deltat)