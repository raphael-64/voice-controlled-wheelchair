import sys
import socket
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets  # Include QtWidgets

# Networking setup for LiDAR
LIDAR_IP = '192.168.137.38'  # Replace with your Raspberry Pi's IP
LIDAR_PORT = 65433

class LidarVisualizer:
    def __init__(self):
        # Update QApplication reference
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('Real-Time LiDAR Visualization')
        self.plot = self.win.addPlot()
        self.plot.setXRange(-10, 10)
        self.plot.setYRange(-10, 10)
        self.scatter = pg.ScatterPlotItem(size=5, brush=pg.mkBrush(255, 255, 255, 120))
        self.plot.addItem(self.scatter)

        # Set up the socket connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(f"Connecting to LiDAR server at {LIDAR_IP}:{LIDAR_PORT}...")
            self.client.connect((LIDAR_IP, LIDAR_PORT))
            print(f"Connected to LiDAR server at {LIDAR_IP}:{LIDAR_PORT}")
        except Exception as e:
            print(f"Failed to connect: {e}")
            sys.exit(1)

        # Start a timer to update the plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Update every 50 milliseconds

    def update(self):
        try:
            # Adjust buffer size as needed
            data = self.client.recv(4096).decode('utf-8').strip()
            if data:
                # Parse the data (format: "angle,distance;angle,distance;...")
                points = [tuple(map(float, p.split(','))) for p in data.split(';') if p]
                # Convert polar coordinates to Cartesian coordinates
                x = [p[1] * np.cos(np.radians(p[0])) for p in points]
                y = [p[1] * np.sin(np.radians(p[0])) for p in points]
                spots = [{'pos': (x[i], y[i])} for i in range(len(x))]
                self.scatter.setData(spots)
        except Exception as e:
            print(f"An error occurred during update: {e}")

    def run(self):
        QtGui.QGApplication.instance().exec_()

if __name__ == '__main__':
    visualizer = LidarVisualizer()
    visualizer.run()
