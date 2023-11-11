#!/usr/bin/env python3
################################################################################
import time
import sys
from unitree_lidar_sdk import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pydeck
import pandas as pd
import laspy
import random
################################################################################
num = int(sys.argv[1])
lreader = createUnitreeLidarReader()
port_name = "/dev/ttyUSB0"
################################################################################
try:
    lreader.initialize(num, port_name)
    print ("Unilidar initialization succeed!")
    print ("Set Lidar working mode to: NORMAL ...")
    lreader.setLidarWorkingMode(NORMAL) 
    print ()
    result = lreader.runParse()
    while result == POINTCLOUD:
        cloud = lreader.getCloud()
        pointlist = []
        for point in cloud.points:
            pointlist.append([point.x,point.y,point.z,point.intensity])
    print ('lidar has shot.... we have the scatter plot building....')
except:
    print ("Unilidar initialization failed! use sample data!!!Site 6 lhc, AZ")
    with laspy.open('/home/jay/Documents/unitree-lidar/site6AZ.laz') as fh:
        las = fh.read()
    x = las.X
    y = las.Y
    z = las.Z
    i = las.intensity
    r = [64] * len(x)
    g = [130] * len(x)
    b = [109] * len(x)
    x2 = x[:num]
    y2 = y[:num]
    z2 = z[:num]
    r2 = r[:num]
    g2 = g[:num]
    b2 = b[:num]
    i2 = i[:num]
    pointlist = list(zip(x2,y2,z2,r2,g2,b2,i2))
##################################################################################
def plot(x,y,z,i):
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection ="3d")
    ax.grid(visable = True, color ='grey',linestyle ='-.', linewidth = 0.3, alpha = 0.2)
    my_cmap = plt.get_cmap('tab20b')  
    sctt = ax.scatter3D(x, y, z, alpha = 1, c = i, cmap = my_cmap, marker ='.')
    plt.title("Lidar Scan 3D scatter plot")
    fig.colorbar(sctt, ax = ax, shrink = 0.5, aspect = 5)
    plt.savefig('/home/jay/Documents/unitree-lidar/static/xyz.jpg')
#############################################################################
def plot2(pointlist):
    pointlist2 = pd.DataFrame(pointlist, columns=['x', 'y', 'z','r','g','b','i'])
    target = [pointlist2.x.mean(), pointlist2.y.mean(), pointlist2.z.mean()]
    point_cloud_layer = pydeck.Layer(    "PointCloudLayer",    data=pointlist2,    get_position=["x", "y", "z"],    get_color=["r", "g", "b"],    get_normal=[0, 0, 15],    auto_highlight=True,    pickable=True,    point_size=3,)
    view_state = pydeck.ViewState(target=target, controller=True, rotation_x=15, rotation_orbit=30, zoom=5.3)
    view = pydeck.View(type="OrbitView", controller=True)
    r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view])
    r.to_html("/home/jay/Documents/unitree-lidar/static/point_cloud_layer.html", css_background_color="#add8e6")
#############################################################################
plot(x,y,z,i)
plot2(pointlist)
###############################################################
