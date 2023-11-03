import math
from typing import List

PI_UNITEE = 3.14159265358979323846
DEGREE_TO_RADIAN = PI_UNITEE / 180.0
RADIAN_TO_DEGREE = 180.0 / PI_UNITEE

def get_system_timestamp() -> float:
    pass

class PointUnitree:
    def __init__(self, x: float, y: float, z: float, intensity: float, time: float, ring: int):
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.time = time
        self.ring = ring

class PointCloudUnitree:
    def __init__(self, stamp: float, id: int, ringNum: int, points: List[PointUnitree]):
        self.stamp = stamp
        self.id = id
        self.ringNum = ringNum
        self.points = points

class ScanUnitree:
    def __init__(self, stamp: float, id: int, validPointsNum: int, points: List[PointUnitree]):
        self.stamp = stamp
        self.id = id
        self.validPointsNum = validPointsNum
        self.points = points

class IMUUnitree:
    def __init__(self, stamp: float, id: int, quaternion: List[float], angular_velocity: List[float], linear_acceleration: List[float]):
        self.stamp = stamp
        self.id = id
        self.quaternion = quaternion
        self.angular_velocity = angular_velocity
        self.linear_acceleration = linear_acceleration

class MessageType:
    NONE = 0
    IMU = 1
    POINTCLOUD = 2
    RANGE = 3
    AUXILIARY = 4
    VERSION = 5
    TIMESYNC = 6

class LidarWorkingMode:
    NORMAL = 1
    STANDBY = 2

class LEDDisplayMode:
    FORWARD_SLOW = 2
    FORWARD_FAST = 3
    REVERSE_SLOW = 4
    REVERSE_FAST = 5
    TRIPLE_FLIP = 6
    TRIPLE_BREATHING = 7
    SIXSTAGE_BREATHING = 8

class UnitreeLidarReader:
    def initialize(self, cloud_scan_num: int = 18, port: str = "/dev/ttyUSB0", baudrate: int = 2000000, rotate_yaw_bias: float = 0, range_scale: float = 0.001, range_bias: float = 0, range_max: float = 50, range_min: float = 0) -> int:
        pass

    def initializeUDP(self, cloud_scan_num: int = 18, lidar_port: int = 5001, lidar_ip: str = "10.10.10.10", local_port: int = 5000, local_ip: str = "10.10.10.100", rotate_yaw_bias: float = 0, range_scale: float = 0.001, range_bias: float = 0, range_max: float = 50, range_min: float = 0) -> int:
        pass

    def runParse(self) -> MessageType:
        pass

    def reset(self) -> None:
        pass

    def getCloud(self) -> PointCloudUnitree:
        pass

    def getIMU(self) -> IMUUnitree:
        pass

    def getVersionOfFirmware(self) -> str:
        pass

    def getVersionOfSDK(self) -> str:
        pass

    def getTimeDelay(self) -> int:
        pass

    def getDirtyPercentage(self) -> float:
        pass

    def setLidarWorkingMode(self, mode: LidarWorkingMode) -> None:
        pass

    def setLEDDisplayMode(self, led_table: List[int]) -> None:
        pass

    def setLEDDisplayMode(self, mode: LEDDisplayMode) -> None:
        pass

    def printConfig(self) -> None:
        pass

def createUnitreeLidarReader() -> UnitreeLidarReader:
    pass



