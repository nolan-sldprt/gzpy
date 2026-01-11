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
        points: NDArray[np.float32] | None = None
    ) -> NDArray[np.float32]:
    """
    Generate the GZ-curve for a vessel's mesh.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh of the vessel.
    n_points : int
        Number of sampling points to compute.
    mass : float
        Mass of the vessel.
    density : float
        Density of the fluid the vessel is in.
    COM : NDArray[np.float32]
        3D location of the vessel's Center of Mass.
    angles : NDArray[np.float32]
        Array of angles for which to compute the righting moment.
    points : NDArray[np.float32] or None, optional
        The sampled points of the mesh. If provided, the `mesh` and `n_points` arguments
        are ignored.
        Defaults to `None`.

    Returns
    -------
    NDArray[np.float32]
        Array of the vessel's righting arm (in metres) corresponding to the supplied `angles`.
    """

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

        cob = center_of_buoyancy(transformed_points, z_level)

        # TODO: ensure this is the correct sign usage
        # FIXME: I think this only works if `angle` is wrapped within [-180,180) or [-pi, pi)
        gz[i] = np.sign(angle) * (cob[0] - COM[0])

    return gz

def center_of_buoyancy(points: NDArray[np.float32], z_level: float) -> NDArray[np.float32]:
    """
    Compute the center of buoyancy (COB) for a set of submerged 3D points.

    Parameters
    ----------
    points : NDArray[np.float32]
        Array of sampled 3D points.
    z_level : float
        The z-level representing the waterline.

    Returns
    -------
    NDArray[np.float32]
        The Center of Buoyancy (COB) coordinate.
    """

    submerged_points = points[points[:, 2] <= z_level]

    cob = np.mean(submerged_points, axis=0)

    return cob

def sample_volume_points(mesh: trimesh.Trimesh, n_points: int) -> NDArray[np.float32]:
    """
    Sample points uniformly from the volume of a 3D mesh.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to sample.
    n_points : int
        Number of points to sample within the mesh.

    Returns
    -------
    NDArray[np.float32]
        Array of sampled points of shape (n_points, 3).
    """

    # get the bounds of the mesh (m)
    bounds: list[list[float], list[float]] = mesh.bounds # [[minx, miny, minz], [maxx, maxy, maxz]]
    # create an empty list to store the points
    points: list = []

    # sample the points
    with tqdm(total=n_points, desc=f'Generating {n_points} sampling points') as pbar:
        while len(points) < n_points:
            # attempt to sample `n_points` points within the mesh
            # trimesh often returns <`n_points` which necessitates the loop
            batch = np.random.uniform(bounds[0], bounds[1], size=(n_points, 3))
            mask = mesh.contains(batch)
            points.extend(batch[mask])

            # update the progress bar
            pbar.n = min(len(points), n_points)
            pbar.refresh()

        # crop to contain only `n_points` sampled points
        points = np.array(points[:n_points])

    return points

def locate_waterline(sampled_points: NDArray[np.float32], mass: float, volume: float, density: float) -> float:
    """
    Locate the waterline z-level given a set of 3D points, mass, volume, and fluid density.

    Parameters
    ----------
    sampled_points : NDArray[np.float32]
        Array of 3D points.
    mass : float
        Mass of the vessel (kg).
    volume : float
        Volue of the vessel (m^3).
    density : float
        Density of the fluid (kg/m^3).
    
    Returns
    -------
    float
        The z-level representing the waterline.
    """

    # copy the sampled points to avoid altering the original list
    points = sampled_points.copy()
    # sort the points by increasing z-value
    points = points[np.argsort(points[:, 2])]
    
    # calculate necessary constants
    n_points = points.shape[0]
    volume_per_point = volume / n_points # (m^3 / per point)
    v_submerged = mass / density  # (m^3)

    # estimate number of submerged points needed
    n_submerged_points = int(np.floor(v_submerged / volume_per_point))

    # get the z-levels and volumes at the index of `n_submerged_points` above and below `v_submerged`
    z_lower = points[n_submerged_points, 2]
    z_upper = points[n_submerged_points + 1, 2]
    v_lower = n_submerged_points * volume_per_point
    v_upper = (n_submerged_points + 1) * volume_per_point

    # TODO: maybe an edge case if we are neutrally or negatively buoyant, should check beforehand
    is_volume_valid: bool = v_lower <= v_submerged <= v_upper
    if not is_volume_valid:
        # TODO: create a more descriptive error message
        raise ValueError('Volume calculation error.')

    # linearly interpolate to find the waterline
    z_level = z_lower + (v_submerged - v_lower) / (v_upper - v_lower) * (z_upper - z_lower)

    return z_level
