import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
import trimesh
from tqdm import tqdm

from gzpy.core.core import __rotation_matrix

def gz_curve(
        mesh: trimesh.Trimesh,
        n_points: int,
        mass: float,
        density: float,
        COM: NDArray[np.float32],
        angles: NDArray[np.float32],
        points: NDArray[np.float32]=None
    ) -> NDArray[np.float32]:
    
    # convert angles from degrees to radians
    angles = np.radians(angles)

    # sample points from the volume of the mesh
    if points is None:
        points = sample_volume_points(mesh, n_points)

    gz = np.zeros_like(angles)
    for i, angle in enumerate(angles):
        # get transformation matrix
        T = __rotation_matrix(-COM, angle)

        # apply transformation to sampled points
        transformed_points = trimesh.transform_points(points, T)
        # locate waterline
        z_level = locate_waterline(transformed_points, mass, mesh.volume, density)

        submerged = transformed_points[transformed_points[:, 2] <= z_level]

        cob = center_of_buoyancy(submerged, z_level)

        # test_plotting(transformed_points, z_level)

        # TODO: this somehow needs to be signed
        gz[i] = cob[0] - COM[0]

    return gz

def center_of_buoyancy(points: NDArray[np.float32], z_level: float) -> NDArray[np.float32]:
    """
    Compute the center of buoyancy (COB) for a set of submerged 3D points.

    Parameters:
        points (np.ndarray): An Nx3 array of 3D points.
        z_level (float): The z-level representing the waterline.

    Returns:
        np.ndarray: A 3-element array representing the COB coordinates.
    """
    submerged_points = points[points[:, 2] <= z_level]

    cob = np.mean(submerged_points, axis=0)

    return cob

def sample_volume_points(
        mesh: trimesh.Trimesh,
        n_points: int,
    ) -> NDArray[np.float32]:
    """
    Sample points uniformly from the volume of a 3D mesh

    Parameters:
        mesh (trimesh.Trimesh): The input 3D mesh.
        n_points (int): The number of points to sample.

    Returns:
        NDArray[np.float32] An array of sampled points of shape (n_points, 3).
    """
    # print(mesh.is_watertight)
    # print(mesh.volume)
    # mesh.fill_holes()
    # print(mesh.is_watertight)
    # print(mesh.volume)

    # points = trimesh.sample.volume_mesh(mesh, n_points)

    # get bounds in meters
    bounds: list[list[float], list[float]] = mesh.bounds # [[minx, miny, minz], [maxx, maxy, maxz]]
    points = []
    with tqdm(total=n_points, desc=f'Generating {n_points} sampling points') as pbar:
        while len(points) < n_points:
            batch = np.random.uniform(bounds[0], bounds[1], size=(n_points, 3))
            mask = mesh.contains(batch)
            points.extend(batch[mask])

            # update the progress bar
            pbar.n = min(len(points), n_points)
            pbar.refresh()
        # crop to contain only `N` sampled points
        points = np.array(points[:n_points])

    return points

def locate_waterline(points: NDArray[np.float32], mass: float, volume: float, density: float) -> float:
    """
    Locate the waterline z-level given a set of 3D points, mass, volume, and fluid density.

    Parameters:
        points (np.ndarray): An Nx3 array of 3D points.
        mass (float): The mass of the object in kg.
        volume (float): The volume of the object in m^3.
        density (float): The density of the fluid in kg/m^3.
    
    Returns:
        float: The z-level representing the waterline.
    """

    # sort the points by increasing z-value
    points = points[np.argsort(points[:, 2])]
    
    # calculate necessary constants
    n_points = points.shape[0]
    volume_per_point = volume / n_points # (m^3 / per point)

    v_submerged = mass / density  # m^3

    # TODO: double check this logic
    # estimate number of submerged points needed
    n_submerged_points = int(np.floor((mass / density) / volume_per_point))

    n_underwater = int(np.floor((mass * n_points) / (density * volume)))

    # get the z_level at that index
    z_lower = points[n_submerged_points, 2]
    z_upper = points[n_submerged_points + 1, 2]

    v_lower = n_submerged_points * volume_per_point
    v_upper = (n_submerged_points + 1) * volume_per_point

    # TODO: can you do an assertion like this? this should likely be a raised error if it fails
    # TODO: maybe an edge case if we are neutrally or negatively buoyant
    # TODO: I suppose we can check that based on mass, volume, and density beforehand to deal with it
    assert v_lower <= v_submerged <= v_upper

    z_level = z_lower + (v_submerged - v_lower) / (v_upper - v_lower) * (z_upper - z_lower)

    return z_level