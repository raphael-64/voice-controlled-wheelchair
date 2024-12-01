import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Generate dummy LiDAR data
def generate_dummy_data():
    # Simulate 360 degrees of LiDAR data
    angles = np.linspace(0, 360, num=360)
    distances = [random.uniform(1, 10) for _ in range(360)]  # Random distances
    return list(zip(angles, distances))

# Visualization setup
def visualize_dummy_lidar():
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    sc = ax.scatter([], [])
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    try:
        while True:
            # Get dummy data
            lidar_data = generate_dummy_data()

            # Convert polar to Cartesian coordinates
            x = [d[1] * np.cos(np.radians(d[0])) for d in lidar_data]
            y = [d[1] * np.sin(np.radians(d[0])) for d in lidar_data]

            # Update scatter plot
            sc.set_offsets(np.c_[x, y])
            plt.draw()
            plt.pause(0.1)  # Pause to refresh the plot

    except KeyboardInterrupt:
        print("Visualization stopped.")
    finally:
        plt.close()

if __name__ == "__main__":
    visualize_dummy_lidar()
