import os
import shutil

'''
    把文件A移动到B的位置
    fileA 是源文件的位置,是一个文件
    fileB 是移动到的目标，是一个文件,要写文件名

    使用
    shutil.copyfile(fileA, fileB)
    e.g
    shutil.copyfile('04929753/c.nii.gz', 'hhh/c.nii.gz')
'''

'''
# 列出指定目录下的指定文件或者是目录

for i in os.listdir('.'):
    if os.path.isfile('./'+i):
        print(i,'   file')
    elif os.path.isdir('./'+i):
        print(i,'   dir')

'''

'''
判断一个文件或者文件夹是否存在

返回true,false
'''

'''
    os.path.exists(test_file.txt)
'''