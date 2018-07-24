# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 19:55:10 2018

@author: gx

search all files under multiple folders, rename them and move them out
select some of them to a new_folder
"""
import os #only convenient for clusters of files
import shutil
import re





def process(path_origin):
    #path=r'D:\C盘备份\Tencent Files\391059727\FileRecv\data2(1)\data2\processed'
    #path_origin=r'D:\C盘备份\Tencent Files\391059727\FileRecv\EMG信号强度与速度关系'
    #path=r'D:\C盘备份\Tencent Files\391059727\FileRecv\徐小薇_伸肌(1)\徐小薇_伸肌'
    finder_father(path_origin)

def finder(path,files):
    for file in files:
        try:
            path_lower=path+'\\'+file
            folders=os.listdir(path_lower)
            finder(path_lower,folders)
        except NotADirectoryError:
            path_residual=path_lower.lstrip(path_origin)
            newname=path_residual.replace('\\','_')
            os.rename(path_lower,path+'\\'+newname)
            shutil.copy(path+'\\'+newname,path_origin)
    
def finder_father(path_origin):
    folders=os.listdir(path_origin)
    finder(path_origin,folders)
    
def mover(path_origin,pattern):
    pattern=re.compile(pattern)
    files=os.listdir(path_origin)
    selected_files=pattern.findall(str(files))
    if not os.path.exists(path_origin+'\\'+'new_folder'):
            os.makedirs(path_origin+'\\'+'new_folder')
    for file in selected_files:
        if os.path.isdir(path_origin+'\\'+file):
            continue
        shutil.copy(path_origin+'\\'+file,path_origin+'\\'+'new_folder')
    
    
    
if __name__=='__main__':
    path_origin=r'D:\C盘备份\Tencent Files\391059727\FileRecv\EMG信号强度与速度关系'
    pattern=r'S\d_\d_\ds_recordData_1.txt'
    
    process(path_origin)
    mover(path_origin,pattern)
    
