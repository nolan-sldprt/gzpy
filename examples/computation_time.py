import time

import matplotlib.pyplot as plt
import numpy as np

import gzpy
from load_samples import fishing_boat

def main():
    mesh, mass = fishing_boat()
    angles = np.arange(0,185,5)

    gz_curve_fig, gz_curve_ax = plt.subplots()
    gz_curve_ax.hlines(0, angles.min(), angles.max(), color='k', label='waterline')
    
    time_fig, time_ax = plt.subplots()

    n_points = np.array([50, 100, 250, 500, 750, 1000, 1500, 2000, 3000])
    time_points_generation = np.zeros_like(n_points)
    time_gz_curve = np.zeros_like(n_points)
    sampling_gz_curves = np.zeros((n_points.shape[0], angles.shape[0]))
    
    for i, n in enumerate(n_points):
        t_start = time.time()
        sampled_points = gzpy.sampling.sample_volume_points(mesh, n)
        t_stop = time.time()
        time_points_generation[i] = t_stop - t_start

        t_start = time.time()
        sampling_gz_curves[i,:] = gzpy.sampling.gz_curve(mesh, n, mass, gzpy.constants.DENSITY_SALTWATER, np.array([0,0,0]), angles, points=sampled_points)
        t_stop = time.time()
        time_gz_curve[i] = t_stop - t_start

        gz_curve_ax.plot(angles, sampling_gz_curves[i,:], label=f'n={int(n)}')

    gz_curve_ax.set_xlabel('roll angle (degrees)')
    gz_curve_ax.set_ylabel('righting arm (m)')
    gz_curve_ax.set_xlim([angles.min(), angles.max()])
    gz_curve_ax.legend(draggable=True)

    time_ax.plot(n_points, time_points_generation, label='points_generation')
    time_ax.plot(n_points, time_gz_curve, label='gz_curve')

    time_ax.set_xlabel('number of sampled points')
    time_ax.set_ylabel('time (s)')
    time_ax.set_xlim([n_points.min(), n_points.max()])
    time_ax.legend(draggable=True)

    plt.show()

if __name__ == '__main__':
    main()