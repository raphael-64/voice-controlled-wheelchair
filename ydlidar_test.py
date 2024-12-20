# This script uses the YDLIDAR SDK (https://github.com/YDLIDAR/YDLidar-SDK)
# Licensed under the MIT License

import os
import ydlidar
import time
import sys
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

RMAX = 8.0


fig = plt.figure()
fig.canvas.manager.set_window_title('YDLidar LIDAR Monitor')
lidar_polar = plt.subplot(polar=True)
lidar_polar.autoscale_view(True,True,True)
lidar_polar.set_rmax(RMAX)
lidar_polar.grid(True)
ports = ydlidar.lidarPortList();
port = "/dev/ttyUSB0";
for key, value in ports.items():
    port = value;
    
#laser = ydlidar.CYdLidar();
#laser.setlidaropt(ydlidar.LidarPropSerialPort, port);
#laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
#laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE);
#laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL);
#laser.setlidaropt(ydlidar.LidarPropScanFrequency, 8.0);
#laser.setlidaropt(ydlidar.LidarPropSampleRate, 4);
#laser.setlidaropt(ydlidar.LidarPropSingleChannel, False);
#scan = ydlidar.LaserScan()


if __name__ == "__main__":
    ydlidar.os_init();
    ports = ydlidar.lidarPortList();
    port = "/dev/ttyUSB0";
    for key, value in ports.items():
        port = value;
        print(port);
    laser = ydlidar.CYdLidar();
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port);
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200);
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE);
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL);
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 8.0);
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 4);
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True);
    laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0);
    laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0);
    laser.setlidaropt(ydlidar.LidarPropMaxRange, 16.0);
    laser.setlidaropt(ydlidar.LidarPropMinRange, 0.08);
    laser.setlidaropt(ydlidar.LidarPropIntenstiy, False);
    scan = ydlidar.LaserScan()

def animate(num):
    
    r = laser.doProcessSimple(scan);
    if r:
        angle = []
        ran = []
        intensity = []
        for point in scan.points:
            angle.append(point.angle);
            ran.append(point.range);
            intensity.append(point.intensity);
        lidar_polar.clear()
        lidar_polar.scatter(angle, ran, c=intensity, cmap='hsv', alpha=0.95)

ret = laser.initialize();
if ret:
    ret = laser.turnOn();
    if ret:
        ani = animation.FuncAnimation(fig, animate, interval=50)
        plt.show()
    laser.turnOff();
laser.disconnecting();
plt.close();
