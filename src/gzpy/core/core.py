import numpy as np
from numpy.typing import NDArray

def __rotation_matrix(translation: NDArray[np.float32], angle: NDArray[np.float32]) -> NDArray[np.float32]:
    """
    Create a 4x4 transformation matrix for given translation and roll angle.

    Parameters
    ----------
        translation : NDArray[np.float32]
            A 3-element array representing translation in x, y, z.
        angle : NDArray[np.float32]
            A 3-element array representing Euler angles (roll, pitch, yaw) in radians. # TODO: correct this

    Returns
    -------
        np.ndarray: A 4x4 transformation matrix.
    """
    # TODO: verify this implementation
    ry = angle
    rx, rz = 0, 0
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)

    R = np.array([
        [cy * cz, -cy * sz, sy],
        [sx * sy * cz + cx * sz, -sx * sy * sz + cx * cz, -sx * cy],
        [-cx * sy * cz + sx * sz, cx * sy * sz + sx * cz, cx * cy]
    ])

    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = translation

    return T