"""PDF generation utilities for Colab and local Jupyter notebooks."""

from .magic import register_magic
from .notebook2pdf import notebook2pdf, notebook2pdf_widget
from .notebook_retrieval import (
    GetIpynbTimeoutError,
    get_notebook_content,
    get_notebook_name,
)

# Auto-register magic on import
register_magic()

__all__ = [
    'notebook2pdf',
    'notebook2pdf_widget',
    'get_notebook_content',
    'get_notebook_name',
    'GetIpynbTimeoutError',
]
