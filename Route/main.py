from Route import ZumoExtension
from Route.Vector2 import *

import matplotlib.pyplot as plt

zumo = ZumoExtension.ZumoExtension()

#zumo.gogoSimple([0,0, 0,1, 5,4, 0,1, 10,10, 0,1])

#zumo.printRoute()

#print(zumo.actionb
oo = [[Vector2(3,5),Vector2(4,5),Vector2(4,8),Vector2(3,8)],[Vector2(1.5,1.5),Vector2(2.5,1.5),Vector2(2.5,2.5),Vector2(1.5,2.5)]]
ooo = [[Vector2(3,2),Vector2(3,3),Vector2(4,1)]]
#res = zumo.superGOGO([0,0, 0,1, 60,40 ,1,0 , 80 ,100,1,0],[])

res = zumo.gogoBezier([0,0, 0,1, 60,40 ,1,0 , 80 ,100,0,1])
x = []
y = []
#zumo.printRoute(res)
timer = 0
#zumo.gogoSimple([0,0, 0,1, 60,40 ,1,0 , 80 ,100,1,0])

'''
for a in zumo.route :
    x.append(a.x)
    y.append(a.y)
'''

for a in res :
    x.append(a[0].x)
    y.append(a[0].y)
    print(a[3])

plt.figure(figsize=(10,10)) #创建绘图对象
plt.plot(x,y,"b--",linewidth=1)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
plt.xlabel("X") #X轴标签
plt.ylabel("Y")  #Y轴标签
plt.title("Route ") #图标题
plt.show()  #显示图
plt.savefig("/Users/mingzheyu/Documents/line.jpg") #保存图

