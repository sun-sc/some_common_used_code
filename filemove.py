import os
# import shutil

'''
功能：把一堆文件批量移动到另一个位置
修改filenames列表中的内容为要移动的文件名
修改FromRootDir为源文件的前缀地址
修改ToRootDir为要移动到的位置
执行函数mvfiles
'''
# filenames要移动的文件名，FromRootDir,文件所在的路径
# 可以通过rootdir + filename 找到文件
FileNames = ['c_002', 'c_004', 'c_008', 'c_012', 'c_024', 'c_030', 'c_032', 'c_035', 'c_037', 'c_044', 'c_060', 'c_065', 'c_078', 'c_082', 'c_088', 'c_092', 'c_098', 'c_102', 'c_106', 'c_112', 'c_114', 'c_115', 'c_119', 'c_127', 'c_130', 'c_141', 'c_143', 'c_146', 'c_148', 'c_153']
FromRootDir = '/workspaces/work/nnUNetFrame/DATASET/nnUNet_raw/nnUNet_raw_data/Task501_tummor1/imagesTr'
# ToRootDir 是要移动到的目标路径
# ToRootDir + filename 是希望到到位置
ToRootDir = '/workspaces/work/nnUNetFrame/test/input'
def mvfiles(filenames,fromrootdir,torootdir):
    for filename in filenames:
        filename = filename + '_0000.nii.gz'
        print(filename)
        fromfile = os.path.join(fromrootdir,filename)
        tofile = os.path.join(torootdir,filename)
        os.system('cp '+fromfile+' '+tofile)

# 移动某个文件夹固定后缀的内容
FromRootDir = '/home/user/peizhun/rawdata/c2/imagesTr'
ToRootDir = '/home/user/attention/data/c2/image'
def mvfiles(fromrootdir,torootdir):
    i = 1
    for filename in os.listdir(FromRootDir):
        c = filename.split('.',1)
        if c[1] == 'npy':
            print(i , filename)
            fromfile = os.path.join(fromrootdir,filename)
            tofile = os.path.join(torootdir,filename)
            os.system('cp '+fromfile+' '+tofile)
            i = i + 1
mvfiles(FromRootDir , ToRootDir)

'''
功能：把一个文件夹下所有的文件，放入一个文件夹中
如 a文件夹有文件a1.xxx,a2.xxx,则执行后，a文件夹中有两个文件夹a1,a2,里面分别是a1.xxx,a2.xxx
输入参数为文件夹路径，
'''
def folder_name(filename):
    r = filename.split('.')
    return r[0]
def pack_file(rootdir):
    for fname in os.listdir(rootdir):
        print(fname)
        if os.path.isfile(os.path.join(rootdir,fname)): #只处理文件
            # 对于要包裹的文件，通过修改这个函数，来确定文件夹的命名
            foldername = folder_name(fname) 
            os.system('mkdir '+ os.path.join(rootdir,foldername))
            
            # 新建完文件夹后，把文件移动进文件夹
            fromname = os.path.join(rootdir,fname)
            toname = os.path.join(rootdir,foldername,fname)
            os.system('mv '+fromname+' '+toname)
# 使用
# pack_file('~/nnUNetFrame/test/input')

def unpack_file(rootdir):
    for fname in os.listdir(rootdir):
        print(fname)
        if os.path.isdir(os.path.join(rootdir,fname)): #只处理文件夹
            # 新建完文件夹后，把文件移动进文件夹
            for file in os.listdir(os.path.join(rootdir,fname)):
                fromname = os.path.join(rootdir,fname,file)
                toname = os.path.join(rootdir,file)
                os.system('mv '+fromname+' '+toname)
            os.system('rm -rf ' + os.path.join(rootdir,fname))
# 以列表的形式输出所有的文件夹
def print_as_list(rootdir):
    c = [] 
    for i in os.listdir(rootdir):
        c.append(i)
    print(c)