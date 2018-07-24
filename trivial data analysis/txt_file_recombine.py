# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 20:21:18 2018

@author: GX

.txt file recombined
"""

import os
import re

def process(path):
    for participant in participants:
        for trial_number in trials:
            trial=str(participant)+'_'+str(trial_number)
            pattern=trial+r'_\ds_recordData_1'
            matcher(pattern,path,trial)

def matcher(pattern,path,trial):
    pattern=re.compile(pattern)
    files=os.listdir(path)
    selected_files=re.findall(pattern,str(files))
    new_file_name=trial+r'_recordData_1'+r'.txt'
    new_file=open(path+'\\'+new_file_name,'a')
    for file in selected_files:
        f=open(path+'\\'+file+r'.txt','r',encoding='UTF-8')
        content=f.readlines()
        for element in content:
            new_file.write(element)
        f.close()    
    new_file.close()

if __name__=='__main__':
    path=r'D:\C盘备份\Tencent Files\391059727\FileRecv\EMG信号强度与速度关系\new_folder\新建文件夹'
    participants=['S1','S2','S3','S4','S5']
    trials=['1','2','3','4']
    process(path)

