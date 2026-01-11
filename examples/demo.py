import os

import gzpy
import numpy as np
import trimesh

def fishing_boat() -> tuple[trimesh.Trimesh, float]:
    mesh = gzpy.core.load_mesh(os.path.join('examples', 'sample_data', 'fishing_boat', 'source', 'boat_model.obj'))

    mass = 50000

    return mesh, mass

def sailboat() -> tuple[trimesh.Trimesh, float]:
    # raise NotImplementedError("The sailboat mesh needs to be fixed")
    mesh = gzpy.core.load_mesh(os.path.join('examples', 'sample_data', 'sailboat-game-asset', 'source', 'MergedFull.obj'))

    mass = 5000

    return mesh, mass

def main():
    print("Select the model to analyze:\n1 - Fishing Boat\n2 - Sailboat")
    mesh_choice = str(input("Model selection [1/2]: "))

    if not mesh_choice.isdigit():
        raise ValueError("Input mesh choice is not positive numeric.")
    else:
        mesh_index: int = int(mesh_choice)
    
    match mesh_index:
        case 1:
            mesh, mass = fishing_boat()
        case 2:
            mesh, mass = sailboat()
        case _:
            raise ValueError("Input mesh choice is not available option. Must be [1,2].")

    print(f'{mesh.is_volume}')
    print(f'{mesh.is_watertight}')
    mesh = gzpy.core.repair_mesh(mesh)
    print(f'{mesh.is_volume}')
    print(f'{mesh.is_watertight}')

    # points = gzpy.sampling.sample_volume_points(mesh, 1000)
    # z = gzpy.sampling.locate_waterline(points, mass, mesh.volume, gzpy.constants.DENSITY_SALTWATER)
    # cob = gzpy.sampling.center_of_buoyancy(points, z)
    # gzpy.sampling.plot_geometry(points, z, np.array([0,0,0]), cob)

    angles = np.arange(0,185,5)
    gzCURVE = gzpy.sampling.gz_curve(mesh, 1000, mass, gzpy.constants.DENSITY_SALTWATER, np.array([0,0,-1]), angles)
    gzpy.core.plot_gz_curve(angles, gzCURVE)

if __name__ == '__main__':
    main()
