# -*- coding: utf-8 -*-
"""
Created on Sat May 26 10:02:28 2018

@author: gx
"""

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import sys
import traceback
import os #only convenient for clusters of files
import scipy.stats

def process():
    #path=r'D:\C盘备份\Tencent Files\391059727\FileRecv\data2(1)\data2\processed'
    path_origin=r'D:\C盘备份\Tencent Files\391059727\FileRecv\EMG信号强度与速度关系\S1\1'
    #path=r'D:\C盘备份\Tencent Files\391059727\FileRecv\徐小薇_伸肌(1)\徐小薇_伸肌'
    folders=os.listdir(path_origin)
    for folder in folders:
        path=path_origin+'\\'+folder
        files=os.listdir(path)
        if not os.path.exists(path+'\\'+'results'):
            os.makedirs(path+'\\'+'results')
        if os.path.exists(path+'\\'+'results'+'\\'+'output.txt'):
            os.remove(path+'\\'+'results'+'\\'+'output.txt')
        for name in files:
            if name == '受试者信息.txt':
                continue
            if name == 'results':
                continue
            OLS_Verify(path,name)
            #print(name)



def OLS_Verify(path,name):
    file=str(path)+"\\"+str(name)
    data=np.loadtxt(file,skiprows=1)
    Y=data[:,-1]#EMG amplitude
    X=data[:,2]#velocity
    Z=data[:,1]#position
    X=abs(X)
    t=np.vstack([Y,X,Z])
    t=np.delete(t,np.where(t[1]<=50),axis=1)#reason needs to be found here
#    t=np.delete(t,np.where(t[1]<=0),axis=1)
#    t=np.delete(t,np.where(t[2]>=-5),axis=1)
    #t=np.delete(t,np.where(t[1]>=0),axis=1)
    Y=t[0]
    X=t[1]
    Z=t[2]
    model=sm.OLS(Y,X)
    results=model.fit()
    print('results.params:',results.params)
    print(results.summary())
    Xfit=X
    Yfit=results.predict(X)
    
    XY=np.vstack([X,Y])
    kde=scipy.stats.gaussian_kde(XY)
    kde.set_bandwidth(bw_method='silverman')
    Z=kde(XY)
#    idx = Z.argsort()
#    X, Y, Z = X[idx], Y[idx], Z[idx]
    
    fig=plt.figure()
    #plt.ylim(0,120)
    plt.ylim(0,250)
    plt.grid(False)
    #plt.style.use('seaborn-whitegrid')
    plt.scatter(X,Y,s=10,c=Z,label='scatter',edgecolor='')
    plt.plot(Xfit,Yfit,linewidth=2,color='pink',label='OLS Regression')
    plt.title(name)    
    clb=plt.colorbar(extend='both')
    plt.xlabel('speed of hand joint',fontsize=14,color='grey')
    plt.ylabel('amplititude of EMG',fontsize=14,color='grey')
    clb.set_label('probability density',fontsize=14,color='grey')
    print(name)
    #save image
    plt.savefig(str(path)+'\\'+'results'+'\\'+str(name)+'1.jpg',format='jpg',dpi=1200)
    string='\n\n\n\n'+str(name)+':\n'+str(results.summary())
    #save table
    out=open(path+'\\'+'results'+'\\'+'output.txt','a')
    out.write(string)
    out.close()
    #np.delete(data[:,1][data[:,1]>0])


if __name__=='__main__':
    try:
        process()
    except Exception as e:
        print('Error:')
        print(e)
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)