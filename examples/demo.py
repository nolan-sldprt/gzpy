import numpy as np

import gzpy
from load_samples import fishing_boat, sailboat

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

    print(f"Watertight and Volume: ({gzpy.core.validate_mesh(mesh)})")

    n_points: int = 1000
    points = gzpy.sampling.sample_volume_points(mesh, n_points)
    
    z = gzpy.sampling.locate_waterline(points, mass, mesh.volume, gzpy.constants.DENSITY_SALTWATER)
    cob = gzpy.sampling.center_of_buoyancy(points, z)
    gzpy.sampling.plot_geometry(points, z, np.array([0,0,0]), cob)

    angles = np.arange(0,185,5)
    gz = gzpy.sampling.gz_curve(mesh, n_points, mass, gzpy.constants.DENSITY_SALTWATER, np.array([0,0,-1]), angles, points=points)
    gzpy.core.plot_gz_curve(angles, gz, show=True)

if __name__ == '__main__':
    main()
