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