import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

def plot_gz_curve(angles: NDArray[np.float32], gz: NDArray[np.float32]) -> None:
    """
    Plot the GZ-curve.

    Parameters
    ----------
    angles :  NDArray[np.float32]
        Array of angles to plot.
    gz : NDArray[np.float32]
        Array of righting arms (m), corresponding the the `angles`.
    
    Returns
    -------
    None
    """

    # validate the input data
    if len(angles.shape) > 1:
        raise ValueError(f'`angles` array must be 1D, not {len(angles.shape)}D')
    
    if len(gz.shape) > 1:
        raise ValueError(f'`gz` array must be 1D, not {len(gz.shape)}D')
    
    if gz.shape != angles.shape:
        raise ValueError(f'`angles` and `gz` must be the same shape. `angles`: {angles.shape}, and `gz`: {gz.shape}.')

    # open a figure
    plt.figure()

    # plot the GZ-curve
    plt.plot(angles, gz)
    # set x-limits
    plt.xlim(angles.min(), angles.max())
    # plot a horizontal line at zero-righting arm
    plt.hlines(0, xmin=angles.min(), xmax=angles.max(), colors='k')
    # label the axes
    plt.xlabel('angle (\N{DEGREE SIGN})')
    plt.ylabel('righting arm (m)')

    # show the plot to the user
    plt.show()
