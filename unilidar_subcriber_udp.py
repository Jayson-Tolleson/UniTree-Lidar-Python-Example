import socket
import struct
import time
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pydeck
import pandas as pd
import numpy as np
# IP and Port
UDP_IP = "0.0.0.0"
UDP_PORT = 80
cloud_scan_num = np.clip(int(sys.argv[1]), 0, 20000)
##################################################################################
def plot(x,y,z,intensity):
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection ="3d")
    ax.grid(visable = True, color ='grey',linestyle ='-.', linewidth = 0.3, alpha = 0.2)
    my_cmap = plt.get_cmap('tab20b')  
    sctt = ax.scatter3D(x, y, z, alpha = 1, c = z, cmap = my_cmap, marker ='.')
    plt.title("Lidar Scan 3D scatter plot")
    fig.colorbar(sctt, ax = ax, shrink = 0.5, aspect = 5)
    plt.savefig('/home/jay/Documents/unitree-lidar/WorkingUnilidar/static/xyz.jpg')
#############################################################################
def plot2(pointlist):
    pointlist2 = pd.DataFrame(pointlist, columns=['x', 'y', 'z','r','g','b','i'])
    target = [pointlist2.x.mean(), pointlist2.y.mean(), pointlist2.z.mean()]
    point_cloud_layer = pydeck.Layer(    "PointCloudLayer",    data=pointlist2,    get_position=["x", "y", "z"],    get_color=["r", "g", "b"],    get_normal=[0, 0, 15],    auto_highlight=True,    pickable=True,    point_size=3,)
    view_state = pydeck.ViewState(target=target, controller=True, rotation_x=15, rotation_orbit=30, zoom=10)
    view = pydeck.View(type="OrbitView", controller=True)
    r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view])
    r.to_html("/home/jay/Documents/unitree-lidar/WorkingUnilidar/static/point_cloud_layer.html", css_background_color="#add8e6")
#############################################################################
# Point Type
class PointUnitree:
    def __init__(self, x, y, z, intensity, time, ring):
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.time = time
        self.ring = ring

# Scan Type
class ScanUnitree:
    def __init__(self, stamp, id, validPointsNum, points):
        self.stamp = stamp
        self.id = id
        self.validPointsNum = validPointsNum
        self.points = points

# IMU Type
class IMUUnitree:
    def __init__(self, stamp, id, quaternion, angular_velocity, linear_acceleration):
        self.stamp = stamp
        self.id = id
        self.quaternion = quaternion
        self.angular_velocity = angular_velocity
        self.linear_acceleration = linear_acceleration

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Calculate Struct Sizes
imuDataStr = "=dI4f3f3f"
imuDataSize = struct.calcsize(imuDataStr)

pointDataStr = "=fffffI"
pointSize = struct.calcsize(pointDataStr)

scanDataStr = "=dII" + 120 * "fffffI"
scanDataSize = struct.calcsize(scanDataStr)

print("pointSize = " +str(pointSize) + ", scanDataSize = " + str(scanDataSize) + ", imuDataSize = " + str(imuDataSize))

while True:
    # Recv data
    data, addr = sock.recvfrom(10000)
    print(f"Received data from {addr[0]}:{addr[1]}")

    msgType = struct.unpack("=I", data[:4])[0]
    print("msgType =", msgType)


    if msgType == 102:  # Scan Message
        length = struct.unpack("=I", data[4:8])[0]
        stamp = struct.unpack("=d", data[8:16])[0]
        id = struct.unpack("=I", data[16:20])[0]
        validPointsNum = struct.unpack("=I", data[20:24])[0]
        scanPoints = []
        pointStartAddr = 24
        for i in range(validPointsNum):
            pointData = struct.unpack(pointDataStr, data[pointStartAddr: pointStartAddr+pointSize])
            pointStartAddr = pointStartAddr + pointSize
            point = PointUnitree(*pointData)
            scanPoints.append(point)
        scanMsg = ScanUnitree(stamp, id, validPointsNum, scanPoints)

        print("A Scan msg is parsed!")
        print("\tstamp =", scanMsg.stamp, "id =", scanMsg.id)
        print("\tScan size =", scanMsg.validPointsNum)
        print("\tfirst 10 points (x, y, z, intensity, time, ring) =")
        x = []
        y = []
        z = []
        r = []
        g = []
        b = []
        intensity = []
        for i in range(min(10, scanMsg.validPointsNum)):
            point = scanMsg.points[i]
            print("\t", point.x, point.y, point.z, point.intensity, point.time, point.ring)
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
            intensity.append(point.intensity)
            r.append(64)
            g.append(130)
            b.append(109)
        print("\n")
        pointlist = list(zip(x,y,z,r,g,b,intensity))
        print (pointlist[:10])
        plot(x,y,z,intensity)
        plot2(pointlist)
###############################################################


sock.close()
