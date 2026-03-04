"""Main entry point for notebook-to-PDF conversion."""

import datetime
import locale
import pathlib
import warnings

import IPython
import IPython.display
import ipywidgets
import nbformat

from ._env import is_colab
from .notebook_retrieval import (
    get_notebook_content,
    get_notebook_name,
    get_notebook_name_local,
)
from .render import (
    create_quarto_config,
    ensure_quarto,
    prepare_notebook,
    render_notebook,
    validate_image_urls,
)


def _notebook2pdf_colab(name: str | None, retrieval_method: str, **kwargs) -> str:
    """Colab-specific PDF conversion: retrieve, render, and trigger browser download.

    Returns:
        Path to the generated PDF file.
    """
    import google.colab

    notebook_name = get_notebook_name() if name is None else pathlib.Path(name)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_dir = pathlib.Path("/content/pdfs") / f"{timestamp}_{notebook_name.stem}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"📥 Loading notebook content (method: {retrieval_method})...")
    notebook = get_notebook_content(method=retrieval_method, **kwargs)

    print("🔍 Validating images...")
    validate_image_urls(notebook)

    print("📝 Preparing notebook...")
    prepared = prepare_notebook(notebook)
    nbformat.write(prepared, (output_dir / f"{notebook_name.stem}.ipynb").open("w", encoding="utf-8"))

    create_quarto_config(output_dir)
    print("🔨 Rendering PDF with Typst...")
    render_notebook(output_dir, notebook_name.stem)
    print("   ✓ Render successful")

    pdf_path = output_dir / f"{notebook_name.stem}.pdf"
    print("⬇️  Downloading PDF...")
    google.colab.files.download(str(pdf_path))
    print(f"✅ Done! PDF saved as: {notebook_name.stem}.pdf")

    return str(pdf_path)


def _notebook2pdf_local(path: pathlib.Path | str | None, **kwargs) -> str:
    """Local PDF conversion: render in a temp dir, copy PDF next to source, show FileLink.

    Returns:
        Path to the generated PDF file.
    """
    import shutil
    import tempfile

    if path is None:
        print("🔍 Detecting notebook path...")
        path = get_notebook_name_local()
    path = pathlib.Path(path).resolve()

    notebook_stem = path.stem

    print(f"📥 Loading notebook from: {path}")
    notebook = get_notebook_content(method="local", path=path)

    print("🔍 Validating images...")
    validate_image_urls(notebook)

    print("📝 Preparing notebook...")
    prepared = prepare_notebook(notebook)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = pathlib.Path(tmp)
        nbformat.write(prepared, (tmp_dir / f"{notebook_stem}.ipynb").open("w", encoding="utf-8"))
        create_quarto_config(tmp_dir)
        print("🔨 Rendering PDF with Typst...")
        render_notebook(tmp_dir, notebook_stem)
        print("   ✓ Render successful")

        # Copy rendered PDF to the source notebook's directory
        pdf_path = path.parent / f"{notebook_stem}.pdf"
        shutil.copy2(tmp_dir / f"{notebook_stem}.pdf", pdf_path)

    print(f"✅ Done! PDF saved as: {pdf_path}")
    if IPython.get_ipython() is not None:
        IPython.display.display(IPython.display.FileLink(str(pdf_path)))

    return str(pdf_path)


def notebook2pdf(
    name: str | None = None,
    path: str | pathlib.Path | None = None,
    retrieval_method: str = "drive",
    **kwargs,
) -> str | None:
    """Convert the current notebook to PDF and deliver it.

    In Colab, the PDF is rendered in ``/content/pdfs/`` and automatically
    downloaded to the browser.  Outside Colab, the PDF is written next to the
    source notebook and a clickable ``FileLink`` is displayed.

    Args:
        name: (Colab only) Custom stem for the output filename.
        path: (Local only) Path to the ``.ipynb`` file.  If omitted, the path
              is inferred from the running kernel via the Jupyter sessions API.
        retrieval_method: (Colab only) How to fetch the notebook content.
                          One of ``'drive'`` (default), ``'timeout'``, or
                          ``'blocking'``.
        **kwargs: Additional arguments forwarded to the retrieval function.

    Returns:
        Absolute path to the generated PDF, or ``None`` if conversion failed.
    """
    warnings.filterwarnings("ignore", category=nbformat.validator.MissingIDFieldWarning)
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    if IPython.get_ipython() is not None:
        IPython.get_ipython().run_line_magic("matplotlib", "inline")

    print("🚀 Starting PDF conversion...")
    ensure_quarto()

    if is_colab():
        return _notebook2pdf_colab(name=name, retrieval_method=retrieval_method, **kwargs)
    else:
        return _notebook2pdf_local(path=path, **kwargs)


def notebook2pdf_widget() -> None:
    """Display an interactive widget to convert and download the current notebook as PDF."""

    def convert(b):
        try:
            status.value = "🔄 Converting"
            b.disabled = True
            pdf_path = notebook2pdf()
            if pdf_path:
                status.value = f"✅ Downloaded: {pathlib.Path(pdf_path).name}"
        except Exception as e:
            status.value = f"❌ {e}"
        finally:
            b.disabled = False

    button = ipywidgets.widgets.Button(description="⬇️ Download")
    status = ipywidgets.widgets.Label()
    button.on_click(lambda b: convert(b))
    IPython.display.display(ipywidgets.widgets.HBox([button, status]))
