import pytest
import trimesh

import gzpy

from examples.load_samples import fishing_boat, sailboat

@pytest.mark.parametrize("model", [fishing_boat()[0], sailboat()[0]])
def test_validate_mesh(model: trimesh.Trimesh):
    output = gzpy.core.validate_mesh(model)

    # assert correct data type
    assert isinstance(output, tuple)
    for item in output:
        assert isinstance(item, bool)
    
    # assert correct length
    assert len(output) == 2

@pytest.mark.parametrize(
    "file_path",
    [
        "examples/sample_data/fishing_boat/boat_model.obj",
        "examples/sample_data/sailboat-game-asset/MergedFull.obj"
    ]
)
def test_load_mesh(file_path: str):
    mesh = gzpy.core.load_mesh(file_path)

    # assert correct data type
    assert isinstance(mesh, trimesh.Trimesh)

    # assert mesh is not empty
    assert mesh.vertices.shape[0] > 0
    assert mesh.faces.shape[0] > 0