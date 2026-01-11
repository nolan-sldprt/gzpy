import numpy as np
from numpy.typing import NDArray
import trimesh

def gz_curve():
    raise NotImplementedError

def center_of_buoyancy(mesh: trimesh.Trimesh, z_level: float) -> NDArray[np.float32]:
    """
    Compute the center of buoyancy (COB) for a 3D mesh.

    Parameters:
        points (np.ndarray): An Nx3 array of 3D points.
        z_level (float): The z-level representing the waterline.

    Returns:
        np.ndarray: A 3-element array representing the COB coordinates.
    """
    # TODO: cut the mesh and close it off, taking the lower than z=z_level
    cut_mesh: trimesh.Trimesh = 0

    cob = cut_mesh.center_mass

    return cob

def locate_waterline(mesh: trimesh.Trimesh, mass: float, volume: float, density: float, atol: float=1e-5) -> float:
    submerged_volume = mass / density

    # iteratively locate the waterline by bisection method
    z_lower_bound = np.min(mesh[:,:,2])
    z_upper_bound = np.max(mesh[:,:,2])
    # inital guess
    z_level = (z_lower_bound + z_upper_bound) / 2

    if submerged_volume >= volume:
        return z_upper_bound

    volume_error = np.inf # (m^3)
    while (volume_error > atol):

        # TODO: cut the mesh and close it off, taking the lower than z=z_level
        cut_mesh: trimesh.Trimesh = 0

        current_submerged_volume = cut_mesh.volume()

        if current_submerged_volume > submerged_volume:
            # waterline is too high, reduce z_upper_bound
            z_upper_bound = z_level
        elif current_submerged_volume < submerged_volume:
            # waterline is too low, increase z_lower_bound
            z_lower_bound = z_level
        else:
            # if the volumes perfectly match, z_level is the exact waterline
            break

        # update z_level and volume_error
        z_level = (z_lower_bound + z_upper_bound) / 2

        #TODO: I think this technically does an extra iteration

    return z_level
