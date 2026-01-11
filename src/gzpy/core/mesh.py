import numpy as np
import trimesh

def load_mesh(file: str) -> trimesh.Trimesh:
    """
    Load a mesh from a file.

    Parameters
    ----------
    file : str
        The location of the file to be loaded.
    
    Returns
    -------
    trimesh.Trimesh
        The mesh loaded from the file.
    """

    mesh = trimesh.load(file)

    # if a trimesh.Scene is returned, merge it into one mesh
    if not isinstance(mesh, trimesh.Trimesh):
        mesh = trimesh.util.concatenate(mesh.dump())

    # apply the default transformation for an `.obj` file to meet `gzpy`'s coordinate conventions
    T = np.array([
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
    mesh.apply_transform(T)

    return mesh
