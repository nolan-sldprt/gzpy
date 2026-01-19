import pytest
import numpy as np
import trimesh

import gzpy

from examples.load_samples import fishing_boat, sailboat

@pytest.mark.parametrize(
    "model, expected_count",
    [
        (fishing_boat()[0], 143),
        (fishing_boat()[0], 450),
        (fishing_boat()[0], 1000),
        (sailboat()[0], 143),
        (sailboat()[0], 450),
        (sailboat()[0], 1000)
    ]
)
def test_sampling(model: trimesh.Trimesh, expected_count: int):
    points = gzpy.sampling.sample_volume_points(mesh=model, n_points=expected_count)

    _check_points_count(points, expected_count)
    _check_points_in_mesh(model, points)

def _check_points_count(points: np.ndarray, expected_count: int) -> bool:
    assert points.shape[0] == expected_count
    assert points.shape[1] == 3

def _check_points_in_mesh(mesh: trimesh.Trimesh, points: np.ndarray) -> bool:
    contained = mesh.contains(points)

    # assert all points are inside the mesh
    assert np.all(contained)
