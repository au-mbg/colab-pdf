"""IPython magic command registration for notebook2pdf."""

import IPython
from IPython.core.magic import Magics, line_magic, magics_class


@magics_class
class Notebook2PDFMagics(Magics):
    """IPython magic commands for PDF conversion."""

    @line_magic
    def notebook2pdf(self, line):
        """Convert current notebook to PDF.

        Usage:
            %notebook2pdf              # infer notebook name automatically
            %notebook2pdf myfile.pdf   # use a custom output name
        """
        from .notebook2pdf import notebook2pdf

        name = line.strip() if line.strip() else None
        return notebook2pdf(name=name)


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(Notebook2PDFMagics)


def register_magic():
    """Automatically register magic command when module is imported."""
    try:
        ipython = IPython.get_ipython()
        if ipython is not None:
            ipython.register_magics(Notebook2PDFMagics)
    except Exception:
        pass  # Not in an IPython environment
