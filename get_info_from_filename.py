
# 针对c_{病人号}_{病人切片号}.npy的文件名
def which_slice(filename):
    beforepoint = filename.split('.' , 1)[0]
    # print(beforepoint)
    c = beforepoint.split('_')
    # print(c[1] , c[2])
    return c[1] , c[2]

