# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

import math
import matplotlib.pyplot as plt

class Vant():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xs = [x]
        self.ys = [y]
        self.path = [[x,y]]

    def addStraight(self,p):
        self.path.append(p)
        self.xs.append(p[0])
        self.ys.append(p[1])

    def addSemicircle(self,center,radiu,direction): #false->back
        if(direction): #true->forth
            angles = range(1,179,10)
            for n in angles:
                circle_x = radiu * math.cos(math.radians(180-n)) + center[0]
                circle_y = radiu/5 * math.sin(math.radians(n)) + center[1]
                self.path.append([circle_x,circle_y]) #add one point per iteration
                self.xs.append(circle_x)
                self.ys.append(circle_y)
        else: #false->back
            angles = range(180,360,10)
            for n in angles:
                circle_x = radiu * math.cos(math.radians(n)) + center[0]
                circle_y = radiu/5 * math.sin(math.radians(n)) + center[1]
                self.path.append([circle_x,circle_y]) #add one point per iteration
                self.xs.append(circle_x)
                self.ys.append(circle_y) 

def explore(width,length,qtdUavs,reach,overleap):
    uavs = []
    captureWidth = reach - overleap #capture area per uav without overleap

    #initial points for each uav
    for i in range(qtdUavs):
        uavs.append(Vant(captureWidth,0))
        captureWidth = captureWidth + 2 * (reach - overleap)

    #the area will be covereged
    total_area = length * width
    print (total_area)
    covereged_area = 0

    forth = True

    while(covereged_area < total_area):
        if(forth):
            for i in range(qtdUavs):
                uavs[i].addStraight([uavs[i].path[-1][0],length])
                covereged_area = (uavs[i].path[-1][0] + reach - overleap) * uavs[i].path[-1][1]
                print (covereged_area,i)

                if(covereged_area < total_area):
                    radiu = (reach - overleap) * qtdUavs
                    center = [uavs[i].path[-1][0] + radiu,length]
                    uavs[i].addSemicircle(center,radiu,True)
                    uavs[i].addStraight([round(uavs[i].path[-1][0]),length])

            forth = False
        else:
            for i in range(qtdUavs):
                uavs[i].addStraight([uavs[i].path[-1][0],0])
                covereged_area = (uavs[i].path[-1][0] + reach - overleap) * length
                print (covereged_area,i)
                if ((covereged_area < total_area)):
                    radiu = (reach - overleap) * qtdUavs
                    center = [uavs[i].path[-1][0] + radiu,0]
                    uavs[i].addSemicircle(center,radiu,False)
                    uavs[i].addStraight([round(uavs[i].path[-1][0]),0])


            forth = True

    return uavs

#parameters
qtdUavs = 4
width = 7000
length = 7000
#reach = 12
height = 90
fov = 1.64
reach = 2 * height * math.tan(fov/2)
overleap = 0.4 * reach

paths = explore(width,length,qtdUavs,reach,overleap) #largura, comprimento, qtd_uavs, alcance, sobreposição

for i in range(qtdUavs):
    x = paths[i].xs
    y = paths[i].ys
    plt.plot(x,y)

plt.show()