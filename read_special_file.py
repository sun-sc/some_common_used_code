

# 读取下面格式的文件
'''
病人id
病人数据1 病人数据2 病人数据3 。。。 病人数据n
病人id
病人数据1 病人数据2 病人数据3 。。。 病人数据n

'''
def get_data(filename):
    dict={}
    f = open(filename,'r')
    lines = f.readlines()
    for i in range(int(len(lines)/2)):
        patientid = lines[i*2].splitlines()[0]
        pos = lines[i*2+1].splitlines()[0].split(' ')
        # print(patientid)
        # print(pos)
        # print('----------------')
        pos = [ int(x) for x in pos ]
        dict[patientid] = pos
    print(dict)