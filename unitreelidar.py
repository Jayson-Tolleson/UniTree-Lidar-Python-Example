#!/usr/bin/env python3
################################################################################
import time
import sys
from unitree_lidar_sdk import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
################################################################################
cloud_scan_num = int(sys.argv[1])
lreader = createUnitreeLidarReader()
port_name = "/dev/ttyUSB0"
################################################################################
try:
    lreader.initialize(cloud_scan_num, port_name)
    print ("Unilidar initialization succeed!")
    print ("Set Lidar working mode to: NORMAL ...")
    lreader.setLidarWorkingMode(NORMAL) 
    print ()
    result = lreader.runParse()
    while result == IMU:
        print ("An IMU msg is parsed!")
        imu = lreader.getIMU()
        print ("\tstamp =", imu.stamp, "id =", imu.id)
        print ("\tquaternion (x, y, z, w) =", imu.quaternion)
        print ("\ttimedelay (us) =", lreader.getTimeDelay())
    while result == POINTCLOUD:
        print ("A Cloud msg is parsed!")
        cloud = lreader.getCloud()
        print ("\tstamp =", cloud.stamp, "id =", cloud.id)
        print ("\tcloud size =", len(cloud.points), "ringNum =", cloud.ringNum)
        print ("\tfirst amount of points (x,y,z,intensity,time,ring) =")
        pointlist = []
        for point in cloud.points:
            print ("\t  (", point.x, ",", point.y, ",", point.z, ",", point.intensity, ",", point.time, ",", point.ring, ")")
            pointlist.append([point.x,point.y,point.z,point.intensity,point.time,point.ring])
        print ("\t  ...")
        print ("\ttimedelay (us) =", lreader.getTimeDelay())
except:
    print ("Unilidar initialization failed! Exit here!")
##################################################################################
def plot(pointlist):
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection ="3d")
    ax.grid(visable = True, color ='grey',linestyle ='-.', linewidth = 0.3, alpha = 0.2)
    my_cmap = plt.get_cmap('hsv')  
    sctt = ax.scatter3D(pointlist[0], pointlist[1], pointlist[2], alpha = 1, c = 'blue', cmap = my_cmap, marker ='^')
    plt.title("Lidar Scan 3D scatter plot")
    fig.colorbar(sctt, ax = ax, shrink = 0.5, aspect = 5)
    plt.savefig('static/xyz.jpg')
#########################################
########################################
#############################################################################
pointlist= [[3,4,5],[3,4,5],[3,4,5]]   # for testing
plot(pointlist)
################################################################################
