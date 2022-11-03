"""
Write the curl of the electrostatic potential to a cube file.

"""

import argparse
import pathlib

import matplotlib.pyplot as plt
from write_cube import write_cube

import streusel


def _get_command_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Write the curl of the electrostatic potential to a cube file."
        ),
    )
    parser.add_argument(
        "cube_file",
        type=pathlib.Path,
        help="A .cube file holding the electrostatic potential.",
    )
    parser.add_argument(
        "output_folder",
        help="The path to the folder into which the output should be written.",
        type=pathlib.Path,
    )
    return parser.parse_args()


def main() -> None:
    cli_args = _get_command_line_arguments()
    cli_args.output_folder.mkdir(parents=True, exist_ok=True)

    atom = streusel.Molecule(cli_args.cube_file)
    atom.get_efield()
    atom.sample_efield_optimized()

    for x in range(75, 125):
        plt.imshow(atom.efield[:, :, x], cmap="viridis")
        plt.colorbar()
        plt.savefig(cli_args.output_folder / f"efield_{x}.png")

        plt.imshow(atom.optimized_method_curl[:, :, x], cmap="viridis")
        plt.colorbar()
        plt.savefig(cli_args.output_folder / f"curl_{x}.png")

    write_cube(
        cli_args.output_folder / "curl.cube",
        atom.optimized_method_curl,
        atom.coords,
        atom.atoms.symbols,
        atom.origin,
        atom.res,
    )


if __name__ == "__main__":
    main()
