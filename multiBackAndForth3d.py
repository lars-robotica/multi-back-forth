# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

import math
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

#Uav is used to store a path
class Vant():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.xs = [x]
        self.ys = [y]
        self.zs = [z]
        self.path = [[x,y,z]]

    #add one point in the path
    def addStraight(self,p):
        self.path.append(p)
        self.xs.append(p[0])
        self.ys.append(p[1])
        self.zs.append(p[2])

    #add semicircle in the end of the straight - permit the uav return
    def addSemicircle(self,center,radiu,direction,height): #false->back
        if(direction): #true->forth
            angles = range(1,179,10)
            for n in angles:
                circle_x = radiu * math.cos(math.radians(180-n)) + center[0]
                circle_y = (radiu*0.6) * math.sin(math.radians(n)) + center[1]
                circle_z = height
                self.path.append([circle_x,circle_y,circle_z]) #add one point per iteration
                self.xs.append(circle_x)
                self.ys.append(circle_y)
                self.zs.append(circle_z)
        else: #false->back
            angles = range(180,360,10)
            for n in angles:
                circle_x = radiu * math.cos(math.radians(n)) + center[0]
                circle_y = (radiu*0.6) * math.sin(math.radians(n)) + center[1]
                circle_z = height
                self.path.append([circle_x,circle_y]) #add one point per iteration
                self.xs.append(circle_x)
                self.ys.append(circle_y)
                self.zs.append(circle_z) 

def explore(width,length,qtdUavs,reach,overleap,height):
    uavs = []
    captureWidth = reach - overleap #capture area per uav without overleap
    #set the initial position for each uav
    for i in range(qtdUavs):
        uavs.append(Vant(captureWidth/2,0,height)) #the initial position is composed with the (x->width without overleap,y->0,z->height)
        #captureWidth = captureWidth + 2 * (reach - overleap)
        captureWidth = captureWidth + reach - overleap


    #the area will be covereged
    total_area = length * width
    covereged_area = 0

    radiu = ((reach - overleap) * qtdUavs)/2
    forth = True

    while(covereged_area < total_area):
        if(forth):
            for i in range(qtdUavs):
                uavs[i].addStraight([uavs[i].path[-1][0],length,height])
                covereged_area = (uavs[i].path[-1][0] + reach - overleap) * uavs[i].path[-1][1]
                #print (covereged_area,i)
                if(covereged_area < total_area):
                    center = [uavs[i].path[-1][0] + radiu,length]
                    uavs[i].addSemicircle(center,radiu,True,height)
                    uavs[i].addStraight([uavs[i].path[-1][0],length,height])

            forth = False
        else:
            for i in range(qtdUavs):
                uavs[i].addStraight([uavs[i].path[-1][0],0,height])
                covereged_area = (uavs[i].path[-1][0] + reach - overleap) * length
                #print (covereged_area,i)
                if ((covereged_area < total_area)):
                    center = [uavs[i].path[-1][0] + radiu,0]
                    uavs[i].addSemicircle(center,radiu,False,height)
                    uavs[i].addStraight([uavs[i].path[-1][0],0,height])
            
            forth = True
    return uavs

#parameters
qtdUavs = 4
width = 600
length = 600
height = 90
fov = 1.64 #06094968746698
reach = 2 * height * math.tan(fov/2) #these inputs and values were verified
overleap = 0.4 * reach
velocity = 15

paths = explore(width,length,qtdUavs,reach,overleap,height) #largura, comprimento, qtd_uavs, alcance, sobreposição, altura


########################################## Plots ###############################################
fig = plt.figure()
plt.rcParams['figure.figsize'] = (44,28)
ax = plt.axes(projection='3d')
dst = 0
dstotal = 0

for k in range(qtdUavs):
	xline = paths[k].xs
	yline = paths[k].ys
	zline = paths[k].zs
	ts = [0]
	tt = 0
	for i in range(1,len(xline)):
		dst = distance.euclidean([xline[i-1],yline[i-1],zline[i-1]],[xline[i],yline[i],zline[i]])
		t = dst / velocity
		tt = tt + t
		ts.append(tt)
		dstotal = dstotal + dst
	time = dstotal / velocity
	print(k+1,dstotal,time)
	dstotal = 0
	dst = 0
	ax.plot3D(xline, yline, zline, label = 'Uav' + str(k+1))

#print(ts)
ax.set_xlabel('x (meters)')
ax.set_ylabel('y (meters)')
ax.set_zlabel('z (meters)')
#ax.set(xlim=(0, 10), ylim=(-2, 2),
plt.title("Multi Back and Forth Method")
plt.legend(loc='best')
plt.plot([0,0,width,width,0],[0,length,length,0,0])
plt.show()