# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 19:57:03 2018

@author: 39105
"""

import os #only convenient for clusters of files
import numpy as np
import re
import shutil
import pandas as pd

path=r'C:\Users\39105\Downloads\精确控制频率\new_folder\新建文件夹\results'
pattern=r"\d+\.\d*"
pd.set_option('precision', 18)
files=os.listdir(path)
pattern=re.compile(pattern)
if os.path.exists(path+'\\'+'results'):
    shutil.rmtree(path+'\\'+'results')
if not os.path.exists(path+'\\'+'results'):
    os.makedirs(path+'\\'+'results')
if os.path.exists(path+'\\'+'results'+'\\'+'output.txt'):
    os.remove(path+'\\'+'results'+'\\'+'output.txt') 
all_data = np.ones((1,11,2,4))
for file in files:
    if os.path.isdir(path+'\\'+file):
        continue
    if file=='note.txt':
        continue
    f=open(path+'\\'+file,'r')
    txt=f.readlines()
    data=pattern.findall(str(txt))
    f.close()
    data=[float(e) for e in data]
    data=np.array(data)
    data=data.reshape(1,11,2,4)
    all_data=np.vstack([all_data,data])
for i in range(all_data.shape[0]):
    person=all_data[i]
    person=person.reshape(22,4)
    pd_data = pd.DataFrame(person,columns=['channel0','channel1','channel2','channel3'],index=['distance','similarity']*11)
    pd_data.to_csv((path+'\\'+'results'+'\\'+'person_%d.csv')%i)
