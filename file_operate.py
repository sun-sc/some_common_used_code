import os
import shutil

'''
    把文件A移动到B的位置
    fileA 是源文件的位置,是一个文件
    fileB 是移动到的目标，是一个文件,要写文件名

    使用
    shutil.copyfile(fileA, fileB)
    e.g
    
'''
shutil.copyfile('04929753/c.nii.gz', 'hhh/c.nii.gz')

# 列出指定目录下的指定文件或者是目录

for i in os.listdir('.'):
    if os.path.isfile('./'+i):
        print(i,'   file')
    elif os.path.isdir('./'+i):
        print(i,'   dir')




'''
判断一个文件或者文件夹是否存在
返回true,false
'''
os.path.exists('test_file.txt')


# 新建文件夹
# mkdir(要新建的目录)
def mkdir(path):
	folder = os.path.exists(path)
 
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print ("---  new folder...  ---")
	else:
		print ("---  There is this folder!  ---")