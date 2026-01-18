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
def test_count_sampled_points(model: trimesh.Trimesh, expected_count: int):
    points = gzpy.sampling.sample_volume_points(mesh=model, n_points=expected_count)

    assert points.shape[0] == expected_count
    assert points.shape[1] == 3
