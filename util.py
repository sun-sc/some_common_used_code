#coding=utf-8
import os
from posixpath import split
import SimpleITK as sitk
import numpy as np
def get_medical_image(path):
    '''
    加载一幅2D/3D医学图像(除.dcm序列图像)，支持格式：.nii, .nrrd, ...
    :param path: 医学图像的路径/SimpleITK.SimpleITK.Image
    :return:(array,origin,spacing,direction)
    array:  图像数组
    origin: 三维图像坐标原点
    spacing: 三维图像坐标间距
    direction: 三维图像坐标方向
    image_type: 图像像素的类型
    注意：实际取出的数组不一定与MITK或其他可视化工具中的方向一致！
    可能会出现旋转\翻转等现象，这是由于dicom头文件中的origin,spacing,direction的信息导致的
    在使用时建议先用matplotlib.pyplot工具查看一下切片的方式是否异常，判断是否需要一定的预处理
    '''

    if isinstance(path, sitk.Image):
        reader = path
    else:
        assert os.path.exists(path), "{} is not existed".format(path)
        assert os.path.isfile(path), "{} is not a file".format(path)
        reader = sitk.ReadImage(path)

    array = sitk.GetArrayFromImage(reader)
    spacing = reader.GetSpacing()  ## 间隔
    origin = reader.GetOrigin()  ## 原点
    direction = reader.GetDirection()  ## 方向
    image_type = reader.GetPixelID()  ## 原图像每一个像素的类型，
    return array, {'origin': origin, 'spacing': spacing, 'direction': direction, 'type': image_type}

# 转换为npy
'''
dirname = '/home/user/peizhun/rawdata/c2/labelsTr'
i = 1
for filename in os.listdir(dirname):
    c = filename.split('.',1)
    
    if c[1] == 'nii.gz':
        print(i , filename)
        res , p = get_medical_image(os.path.join(dirname,filename))
        filename = c[0] + '.npy'
        np.save(os.path.join(dirname,filename) , res)
        i = i + 1 
'''

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
# mvfiles(FromRootDir , ToRootDir)

def get_medical_image(path):
    '''
    加载一幅2D/3D医学图像(除.dcm序列图像)，支持格式：.nii, .nrrd, ...
    :param path: 医学图像的路径/SimpleITK.SimpleITK.Image
    :return:(array,origin,spacing,direction)
    array:  图像数组
    origin: 三维图像坐标原点
    spacing: 三维图像坐标间距
    direction: 三维图像坐标方向
    image_type: 图像像素的类型
    注意：实际取出的数组不一定与MITK或其他可视化工具中的方向一致！
    可能会出现旋转\翻转等现象，这是由于dicom头文件中的origin,spacing,direction的信息导致的
    在使用时建议先用matplotlib.pyplot工具查看一下切片的方式是否异常，判断是否需要一定的预处理
    '''

    if isinstance(path, sitk.Image):
        reader = path
    else:
        assert os.path.exists(path), "{} is not existed".format(path)
        assert os.path.isfile(path), "{} is not a file".format(path)
        reader = sitk.ReadImage(path)

    array = sitk.GetArrayFromImage(reader)
    spacing = reader.GetSpacing()  ## 间隔
    origin = reader.GetOrigin()  ## 原点
    direction = reader.GetDirection()  ## 方向
    image_type = reader.GetPixelID()  ## 原图像每一个像素的类型，
    return array, {'origin': origin, 'spacing': spacing, 'direction': direction, 'type': image_type}

## 将numpy数组保存为3D医学图像格式，支持 .nii, .nrrd
def save_medical_image(array, target_path, param):
    '''
    将得到的数组保存为医学图像格式
    :param array: 想要保存的医学图像数组，为避免错误，这个函数只识别3D数组
    :param origin:读取原始数据中的原点
    :param space: 读取原始数据中的间隔
    :param direction: 读取原始数据中的方向
    :param target_path: 保存的文件路径，注意：一定要带后缀，E.g.,.nii,.nrrd SimpleITK会根据路径的后缀自动判断格式，填充相应信息
    :param type: 像素的储存格式
    :return: None 无返回值
    注意，因为MITK中会自动识别当前载入的医学图像文件是不是标签(label)【通过是否只有0,1两个值来判断】
    所以在导入的时候，MITK会要求label的文件格式为unsigned_short/unsigned_char型，否则会有warning
    '''

    assert len(np.asarray(array).shape) == 3, "array's shape is {}, it's not a 3D array".format(np.asarray(array).shape)

    ## if isVector is true, then a 3D array will be treaded as a 2D vector image
    ## otherwise it will be treaded as a 3D image
    image = sitk.GetImageFromArray(array, isVector=False)

    if 'direction' in param: image.SetDirection(param['direction'])
    if 'spacing' in param: image.SetSpacing(param['spacing'])
    if 'origin' in param: image.SetOrigin(param['origin'])

    if 'type' not in param:
        sitk.WriteImage(sitk.Cast(image, sitk.sitkInt32), target_path, True)
    else:
        ## 如果是标签，按照MITK要求改为unsigned_char/unsigned_short型 [sitk.sitkUInt8]
        sitk.WriteImage(sitk.Cast(image, param['type']), target_path, True)

def writereadme(file,content):
    f = open(file , 'w')
    f = f.write(content)

# mkdir(要新建的目录)
def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径


## 归一化 (0,1)标准化
def norm_zero_one(array, span=None):
    '''
    根据所给数组的最大值、最小值，将数组归一化到0-1
    :param array: 数组
    :return: array: numpy格式数组
    '''
    array = np.asarray(array).astype(np.float32)
    if span is None:
        mini = array.min()
        maxi = array.max()
    else:
        mini = span[0]
        maxi = span[1]
        array[array < mini] = mini
        array[array > maxi] = maxi

    range = maxi - mini

    def norm(x):
        return (x - mini) / range

    return np.asarray(list(map(norm, array))).astype(np.float32)