import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

def plot_geometry(points: NDArray[np.float32], z: float=None, COM: NDArray[np.float32]=None, COB: NDArray[np.float32]=None) -> None:
    """
    Plot the sampled points that approximate a vessel.

    If provided, the: waterline, COM, and COB can also be plotted.

    Parameters
    ----------
    points : NDArray[np.float32]
        Array of sampled points within a vessel.
    z : float or None, optional
        Height of the waterline.
        Defaults to `None`.
    COM : NDArray[np.float32] or None, optional
        3D coordinate of the Center of Mass.
        Defaults to `None`.
    COB : NDArray[np.float32] or None, optional
        3D coordinate of the Center of Buoyancy.
        Defaults to `None`.

    Returns
    -------
    None
    """

    # scatter plot in 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, c="blue", label='sampling points')

    if z is not None:
        x = np.array([points[:,0].min(), points[:,0].max()])
        y = np.array([points[:,1].min(), points[:,1].max()])
        X, Y = np.meshgrid(x, y)
        Z = z*np.ones_like(X)
        ax.plot_surface(X,Y,Z, alpha=0.8, label='waterline')

    if COM is not None:
        ax.scatter(*COM.tolist(), color='red', label='COM')
    
    if COB is not None:
        ax.scatter(*COB.tolist(), color='green', label='COB')

    # get the limits of the axes
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d()
    ])
    spans = limits[:,1] - limits[:,0]
    centers = np.mean(limits, axis=1)
    radius = 0.5 * max(spans)
    # set the axes to have equal scales
    ax.set_xlim3d(centers[0] - radius, centers[0] + radius)
    ax.set_ylim3d(centers[1] - radius, centers[1] + radius)
    ax.set_zlim3d(centers[2] - radius, centers[2] + radius)

    # label the axes
    ax.set_xlabel("$x$ (m)")
    ax.set_ylabel("$y$ (m)")
    ax.set_zlabel("$z$ (m)")

    plt.legend(draggable=True)

    # show the plot to the user
    plt.show()
