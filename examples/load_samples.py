import os

import trimesh

import gzpy

def fishing_boat() -> tuple[trimesh.Trimesh, float]:
    mesh: trimesh.Trimesh = gzpy.core.load_mesh(os.path.join('examples', 'sample_data', 'fishing_boat', 'source', 'boat_model.obj'))

    mass: float = 50000.0

    return mesh, mass

def sailboat() -> tuple[trimesh.Trimesh, float]:
    mesh: trimesh.Trimesh = gzpy.core.load_mesh(os.path.join('examples', 'sample_data', 'sailboat-game-asset', 'source', 'MergedFull.obj'))

    mass: float = 5000.0

    return mesh, mass
