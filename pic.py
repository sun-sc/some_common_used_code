from array import ArrayType
import matplotlib.pyplot as plt # plt 用于显示图片
import numpy as np

# 清空画布
plt.clf()


plt.imshow(Array)
plt.show() #显示图片
plt.savefig('xx.png')


#绘制热力图
plt.imshow(a,  cmap='jet')
plt.colorbar()
plt.axis('off')
plt.savefig('heat.png')