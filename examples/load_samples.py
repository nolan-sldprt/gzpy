import os

import trimesh

import gzpy

def fishing_boat() -> tuple[trimesh.Trimesh, float]:
    mesh = gzpy.core.load_mesh(os.path.join('examples', 'sample_data', 'fishing_boat', 'source', 'boat_model.obj'))

    mass = 50000

    return mesh, mass

def sailboat() -> tuple[trimesh.Trimesh, float]:
    # raise NotImplementedError("The sailboat mesh needs to be fixed")
    mesh = gzpy.core.load_mesh(os.path.join('examples', 'sample_data', 'sailboat-game-asset', 'source', 'MergedFull.obj'))

    mass = 5000

    return mesh, mass