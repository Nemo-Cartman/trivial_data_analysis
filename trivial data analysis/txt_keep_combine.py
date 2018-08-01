# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 19:40:19 2018

@author: 39105
"""

import os #only convenient for clusters of files
import shutil
import re


try:
    path=r'C:\Users\39105\Downloads\精确控制频率\new_folder\新建文件夹'
    files=os.listdir(path)
    if not os.path.exists(path+'\\'+'results'):
        os.makedirs(path+'\\'+'results')
    if os.path.exists(path+'\\'+'results'+'\\'+'output.txt'):
        os.remove(path+'\\'+'results'+'\\'+'output.txt') 
    #string='\n\n\n\n'+str(name)+':\n'+str(results.summary())
        #save table
    for file in files:
        if os.path.isdir(path+'\\'+file):
            continue
        out=open(path+'\\'+'results'+'\\'+'output.txt','a')
        f=open(path+'\\'+file,'r')
        string=f.readlines()
        out.write(str(file))
        out.write('\n')
        out.write(str(string))
        out.write('\n')
        out.close()    

finally:
    out.close()   