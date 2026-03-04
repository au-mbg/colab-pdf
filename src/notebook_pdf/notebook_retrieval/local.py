"""Local filesystem notebook content retrieval."""

import pathlib

import nbformat


def get_notebook_content_from_path(path: pathlib.Path) -> nbformat.NotebookNode:
    """Read a notebook from a local .ipynb file.

    Args:
        path: Path to the .ipynb file.

    Returns:
        nbformat.NotebookNode

    Raises:
        FileNotFoundError: If the path does not exist.
    """
    path = pathlib.Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Notebook not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return nbformat.read(f, as_version=4)
