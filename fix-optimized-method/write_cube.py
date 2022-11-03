from collections import abc

import numpy as np


def write_cube(
    path: str,
    voxel_grid: np.ndarray,
    atomic_coordinates: np.ndarray,
    elements: abc.Collection[str],
    origin: np.ndarray,
    resolution: np.ndarray,
) -> None:
    """
    Write a ``.cube`` file.

    Parameters:
        path:
            The path to the file.
        voxel_grid:
            The voxel values to be written to the cube file.
        atomic_coordinates:
            An N by 3 position matrix written to the cube file.
        elements:
            For each atom, its elemental symbol.
        origin:
            The origin field for the cube file.
        resolution:
            An array of size 3, holding length of voxels in each
            dimension.

    """

    origin_x, origin_y, origin_z = origin
    res_x, res_y, res_z = resolution
    nvox_x, nvox_y, nvox_z = voxel_grid.shape
    with open(path, "w") as cube:
        lines = [
            " title",
            " title2",
            (
                f"{len(elements): >5} {origin_x: >11.6f} "
                f"{origin_y: >11.6f} {origin_z: >11.6f}"
            ),
            f"{nvox_x: >5} {res_x: >11.6f} {0.: >11.6f} {0.: >11.6f}",
            f"{nvox_y: >5} {0.: >11.6f} {res_y: >11.6f} {0.: >11.6f}",
            f"{nvox_z: >5} {0.: >11.6f} {0.: >11.6f} {res_z: >11.6f}",
        ]
        for element, [x, y, z] in zip(elements, atomic_coordinates):
            lines.append(
                f"{element: >5} {0.: >11.6f} "
                f"{x: >11.6f} {y: >11.6f} {z: >11.6f}"
            )

        ncols = 6
        for i in range(nvox_x):
            for j in range(nvox_y):
                line = []
                for k in range(nvox_z):
                    line.append(f"{voxel_grid[i, j, k]: >12.5E}")
                    if len(line) == ncols:
                        lines.append(_pad_left(" ".join(line)))
                        line = []
                lines.append(_pad_left(" ".join(line)))
                line = []
        content = "\n".join(lines)
        cube.write(f"{content}\n")


def _pad_left(s: str) -> str:
    return f" {s}"
