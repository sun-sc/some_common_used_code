#coding=utf-8
# 本文件主要是基于 SimpleITK 完成的
import SimpleITK as sitk
# 得到2D/3D的医学图像(除.dcm序列图像)
# e.g使用
# res,p = get_medical_image(os.path.join(savedir,file,'label',filename)) #读取数组到res中

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

# e.g
# save_medical_image(res,os.path.join(savedir,file,'label',save_filename),p)
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

# 转变图像的类型
# e,g
# change_medical_image('file1/1.nii.gz','file2/2.nrrd)
def change_medical_image(path,target_path):
    '''
        输入：
        path 源文件的路径+名称
        target_path 要转换的的文件的路径+名称
        返回：无
        输出：无
        功能：转换医学图像的格式
    '''
    res,p = get_medical_image(path)
    save_medical_image(res,target_path,p)

## 按顺序得到当前目录下，所有文件（包括文件夹）的名字
def get_files_name(dire):
    '''
    按顺序得到当前目录下，所有文件（包括文件夹）的名字
    :param dire: 文件夹目录
    :return:files[list]，当前目录下所有的文件（包括文件夹）的名字，顺序排列
    '''

    assert os.path.exists(dire), "{} is not existed".format(dire)
    assert os.path.isdir(dire), "{} is not a directory".format(dire)

    files = os.listdir(dire)
    files = natsort.natsorted(files)
    return files
## 得到一组dicom序列图像
## 要同时复制上面的get_files_name函数
import natsort
from tempfile import TemporaryDirectory
import shutil
import numpy as np
def get_dicom_image(dire):
    '''
    加载一组dicom序列图像
    :param dire: dicom序列所在的文件夹路径，E.g. "E:/Work/Database/Teeth/origin/1/"
    :return: (array,origin,spacing,direction)
    array:  图像数组
    origin: 三维图像坐标原点
    spacing: 三维图像坐标间距
    direction: 三维图像坐标方向
    注意：实际取出的数组不一定与MITK或其他可视化工具中的方向一致！
    可能会出现旋转\翻转等现象，这是由于dicom头文件中的origin,spacing,direction的信息导致的
    在使用时建议先用matplotlib.pyplot工具查看一下切片的方式是否异常，判断是否需要一定的预处理
    注意：实际DICOM第一张可能是定位图，同时取出会导致位置错乱
    '''

    assert os.path.exists(dire), "{} is not existed".format(dire)
    assert os.path.isdir(dire), "{} is not a directory".format(dire)

    ## 厚度不一样，则有一样定位图
    thickness = dict()
    files = get_files_name(dire)
    for index in range(len(files)):
        file = sitk.ReadImage(os.path.join(dire, files[index]))
        sthick = file.GetMetaData('0018|0050')
        if sthick in thickness:
            thickness[sthick].append(files[index])
        else:
            thickness[sthick] = [files[index]]

    thickness = sorted(thickness.items(), key=lambda x: len(x[1]), reverse=True)
    files = thickness[0][1]

    with TemporaryDirectory() as dirname:
        for index in range(len(files)):
            shutil.copyfile(src=os.path.join(dire, files[index]), dst=os.path.join(dirname, files[index]))

        ## 重新加载图片
        reader = sitk.ImageSeriesReader()
        reader.MetaDataDictionaryArrayUpdateOn()  # 加载公开的元信息
        reader.LoadPrivateTagsOn()  # 加载私有的元信息

        series = reader.GetGDCMSeriesIDs(dirname)
        filesn = reader.GetGDCMSeriesFileNames(dirname, series[0])

        reader.SetFileNames(filesn)
        dcmimg = reader.Execute()

    array = sitk.GetArrayFromImage(dcmimg)
    origin = dcmimg.GetOrigin()  # x, y, z
    spacing = dcmimg.GetSpacing()  # x, y, z
    direction = dcmimg.GetDirection()
    image_type = dcmimg.GetPixelID()  ## 原图像每一个像素的类型
    return array, origin, spacing, direction, image_type


# 输入一个路径名，把一个文件夹下面nii.gz文件转换为npy文件
def change_nifi2npy(dirname):
    for filename in os.listdir(dirname):
        c = filename.split('.',1)
        if c[1] == 'nii.gz':
            print(c[0] + '.npy')
            res , p = get_medical_image(os.path.join(dirname , filename))
            savename = os.path.join(dirname,c[0] + '.npy')
            np.save(savename ,res)



# niigz 转为 npy
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