import numpy as np

# np.save ("./文件名", 数组名)
# np.load("./文件名.npy")： 函数是从二进制的文件中读取数据 

# 创建2行2列取值范围为[0,1)的数组
# arr = np.random.rand(2,2)

# 创建一维数组，元素个数为10，取值范围为[0,1)
# arr1 = np.random.rand(10)

# 判断一维数组不相同元素的位置
'''
    a = np.array([1,2,3,4,5])
    b = np.array([1,2,3,3,4])
    #定义数组下标
    index = np.arange(0,5)
    #找到两个数组相等元素的下标位置
    print(index[a == b])
    #找到两个数组不相等元素的下标位置
    print(index[a != b])

'''

# 判断两个矩阵是否相同
# (a==c).all() 
# 为true说明相同，不为true说明不相同

# 判断矩阵不同
# a = np.array([[1,2],[3,4]])
# b = np.array([[1,4],[4,6]])
# c=np.argwhere(a != b)
# print(c)
# print(c.shape)

# 所有满足条件的数修改为
result[result % 2 == 1] = 666

# 多条件替换
# 满足条件，则为第二个参数，不满足是第三个参数
np.where((a > 3) & (a < 7), a, 10*a)

# numpy拷贝
# a = b  # 这种拷贝修改原始的a后，b仍然改变
# 拷贝使用
# b  = a.copy()


# 字典形式的内容转numpy
def test_1():
    d = {'a':123,'b':456}
    d1 = {'e':321,'f':654}
    d2 = []
    d2.append(d)
    d2.append(d1)
    print(d2)
    res = np.array([list(item.values()) for item in d2])
    print(res)

# 最大的数字
c.max()


#numpy 拼接
a = np.random.rand(3,3)
b = np.random.rand(3,3)
a = a[np.newaxis,:,:]
b = b[np.newaxis,:,:]
c = np.concatenate((a,b))



# 统计元素个数
# 需要先展开成一维
res = np.load('c_007_0012.npy').flatten()
import collections
data_count2=collections.Counter(random_data)


