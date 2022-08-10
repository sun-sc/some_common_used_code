#保存
dict_name = {1:{1:2,3:4},2:{3:4,4:5}}
f = open('temp.txt','w')
f.write(str(dict_name))
f.close()

#读取
f = open('temp.txt','r')
a = f.read()
dict_name = eval(a)
f.close()

# 查看字典长度
len(data_count2)

#获取值为2的键，返回一个list
k2 = [k for k, v in d.items() if v == 2]




