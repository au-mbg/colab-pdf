"""Quarto render subprocess call."""

import pathlib
import subprocess


def render_notebook(output_dir: pathlib.Path, notebook_stem: str) -> None:
    """Run `quarto render <notebook>.ipynb --to typst` in output_dir.

    Raises:
        subprocess.CalledProcessError: If Quarto exits with a non-zero status.
    """
    render_cmd = f"quarto render {notebook_stem}.ipynb --to typst"
    result = subprocess.run(
        render_cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=str(output_dir),
    )

    if result.returncode != 0:
        print("❌ Render failed!")
        print(f"   STDOUT: {result.stdout}")
        print(f"   STDERR: {result.stderr}")
        raise subprocess.CalledProcessError(
            result.returncode, render_cmd, result.stdout, result.stderr
        )
