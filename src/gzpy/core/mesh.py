import numpy as np
import trimesh

def load_mesh(file: str) -> trimesh.Trimesh:
    mesh = trimesh.load(file)

    if not isinstance(mesh, trimesh.Trimesh):
        # if a trimesh.Scene is returned, merge it into one mesh
        mesh = trimesh.util.concatenate(mesh.dump())

    T = np.array([
        [1, 0, 0, 0],
        [0, 0, -1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
    mesh.apply_transform(T)

    return mesh

def repair_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """
    Repair the mesh to remove degenerate faces, duplicate faces, and unreferenced vertices.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to repair.

    Returns
    -------
    trimesh.Trimesh
        The repaired mesh.
    """

    count_nan = np.sum(np.isnan(mesh.vertices))
    count_inf = np.sum(np.isinf(mesh.vertices))
    count_zero_area_faces = np.sum(mesh.area_faces == 0)

    # make a copy of the mesh to not modify the original
    repaired_mesh = mesh.copy()
    # repair the mesh using trimesh operations
    # repaired_mesh.fill_holes()
    repaired_mesh.process()
    # required_mesh = trimesh.Trimesh(*pymeshfix.clean_from_arrays(repaired_mesh.vertices, repaired_mesh.faces))
    repaired_mesh.remove_degenerate_faces()
    repaired_mesh.remove_duplicate_faces()
    repaired_mesh.remove_unreferenced_vertices()


    repaired_count_nan = np.sum(np.isnan(repaired_mesh.vertices))
    repaired_count_inf = np.sum(np.isinf(repaired_mesh.vertices))
    repaired_count_zero_area_faces = np.sum(repaired_mesh.area_faces == 0)

    print(f"{count_nan - repaired_count_nan} NaN vertices repaired. {repaired_count_nan} remaining.")
    print(f"{count_inf - repaired_count_inf} Inf vertices repaired. {repaired_count_inf} remaining.")
    print(f"{count_zero_area_faces - repaired_count_zero_area_faces} zero area faces repaired. {repaired_count_zero_area_faces} remaining.")

    return repaired_mesh