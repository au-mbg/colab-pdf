"""Notebook preparation before rendering."""

import re

import nbformat
import requests


def validate_image_urls(notebook: nbformat.NotebookNode) -> None:
    """Raise if any image URL in markdown cells returns a non-200 status.

    Raises:
        Exception: Listing all unreachable URLs.
    """
    bad_urls = [
        url
        for cell in notebook.cells
        if cell.get("cell_type") == "markdown"
        for url in re.findall(r"!\[.*?\]\((https?://.*?)\)", cell["source"])
        if requests.head(url, timeout=5).status_code != 200
    ]
    if bad_urls:
        raise Exception(f"Bad Image URLs: {','.join(bad_urls)}")


def prepare_notebook(notebook: nbformat.NotebookNode) -> nbformat.NotebookNode:
    """Strip notebook2pdf cells and normalise the notebook structure.

    Returns:
        A new NotebookNode ready to be written to disk.
    """
    cells = [cell for cell in notebook.cells if "--Colab2PDF" not in cell.source]
    prepared = nbformat.v4.new_notebook(cells=cells or [nbformat.v4.new_code_cell("#")])
    nbformat.validator.normalize(prepared)
    return prepared
