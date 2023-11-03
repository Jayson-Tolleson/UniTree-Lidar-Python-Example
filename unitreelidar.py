import time
import sys
from unitree_lidar_sdk import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
cloud_scan_num = int(sys.argv[1])
lreader = createUnitreeLidarReader()
port_name = "/dev/ttyUSB0"
################################################################################
if lreader.initialize(cloud_scan_num, port_name):
    print ("Unilidar initialization failed! Exit here!")
    exit(-1)
else:
    print ("Unilidar initialization succeed!")

print ("Set Lidar working mode to: STANDBY ...")
lreader.setLidarWorkingMode(STANDBY)
time.sleep(1)
print ("Set Lidar working mode to: NORMAL ...")
lreader.setLidarWorkingMode(NORMAL)
time.sleep(1)
print ()

while True:
    if lreader.runParse() == VERSION:
        print ("lidar firmware version =", lreader.getVersionOfFirmware())
        break
    time.sleep(0.5)
print ("lidar sdk version =", lreader.getVersionOfSDK())
time.sleep(2)

count_percentage = 0
while True:
    if lreader.runParse() == AUXILIARY:
        print ("Dirty Percentage =", lreader.getDirtyPercentage(), "%")
        if count_percentage > 2:
            break
        if lreader.getDirtyPercentage() > 10:
            print ("The protection cover is too dirty! Please clean it right now! Exit here ...")
            exit(0)
        count_percentage += 1
    time.sleep(0.5)
print ()
time.sleep(2)

print ("Turn on all the LED lights ...")
led_table = [0xFF] * 45
lreader.setLEDDisplayMode(led_table)
time.sleep(2)
print ("Turn off all the LED lights ...")
led_table = [0x00] * 45
lreader.setLEDDisplayMode(led_table)
time.sleep(2)
print ("Set LED mode to: FORWARD_SLOW ...")
lreader.setLEDDisplayMode(FORWARD_SLOW)
time.sleep(2)
print ("Set LED mode to: REVERSE_SLOW ...")
lreader.setLEDDisplayMode(REVERSE_SLOW)
time.sleep(2)
print ("Set LED mode to: SIXSTAGE_BREATHING ...")
lreader.setLEDDisplayMode(SIXSTAGE_BREATHING)
print ()
time.sleep(2)

while True:
    result = lreader.runParse()
    if result == NONE:
        continue
    elif result == IMU:
        print ("An IMU msg is parsed!")
        imu = lreader.getIMU()
        print ("\tstamp =", imu.stamp, "id =", imu.id)
        print ("\tquaternion (x, y, z, w) =", imu.quaternion)
        print ("\ttimedelay (us) =", lreader.getTimeDelay())
    elif result == POINTCLOUD:
        print ("A Cloud msg is parsed!")
        cloud = lreader.getCloud()
        print ("\tstamp =", cloud.stamp, "id =", cloud.id)
        print ("\tcloud size =", len(cloud.points), "ringNum =", cloud.ringNum)
        print ("\tfirst amount of points (x,y,z,intensity,time,ring) =")
        for point in cloud.points[:10]:
            print ("\t  (", point.x, ",", point.y, ",", point.z, ",", point.intensity, ",", point.time, ",", point.ring, ")")
        print ("\t  ...")
        print ("\ttimedelay (us) =", lreader.getTimeDelay())
    else:
        continue
    
cloud.points = pointslist
##################################################################################
def plot(pointlist):
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection ="3d")
    ax.grid(visable = True, color ='grey',linestyle ='-.', linewidth = 0.3, alpha = 0.2)
    my_cmap = plt.get_cmap('hsv')  
    sctt = ax.scatter3D(pointlist[0], pointlist[1], pointlist[2], alpha = pointslist[3], c = 'blue', cmap = my_cmap, marker ='^')
    plt.title("Lidar Scan 3D scatter plot")
    fig.colorbar(sctt, ax = ax, shrink = 0.5, aspect = 5)
    plt.savefig('xyz.jpg')
    return sctt,ax
#########################################
def plot_updater(sctt,ax,pointlist):
    ax.relim()
    ax.autoscale()
    sctt.set_xdata(pointlist[0])
    sctt.set_ydata(pointlist[1])
    sctt.set_3d_properties(pointlist[2])
    plt.savefig('xyz.jpg')
    return sctt,ax
########################################
#############################################################################
pointlist= [[3,4,5],[3,4,5],[3,4,5]]   # for testing
sctt,ax=plot(pointlist)
