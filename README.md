# notebook-pdf

Convert Jupyter and Google Colab notebooks to PDF via [Quarto](https://quarto.org) and Typst. Works both in Colab and in a local Jupyter environment.

## Installation

In a notebook cell:

```python
%pip install -q "notebook_pdf @ git+https://github.com/au-mbg/notebook-pdf.git"
```

Or pin to a specific release using the pre-built wheel:

```python
%pip install -q "https://github.com/au-mbg/notebook-pdf/releases/latest/download/notebook_pdf-latest-py3-none-any.whl"
```

## Usage

### Google Colab

Add a cell at the end of your notebook to trigger conversion and download the PDF:

```python
#| include: false
%pip install -q "notebook_pdf @ git+https://github.com/au-mbg/notebook-pdf.git"
from notebook_pdf import notebook2pdf
notebook2pdf()
```

The default retrieval method is `"drive"`, which requires the notebook to be saved to Google Drive. If it is not, you can fall back to blocking retrieval instead:

```python
notebook2pdf(retrieval_method="blocking")
```

Note that blocking retrieval relies on an undocumented Colab API and can sometimes hang with no way to recover other than interrupting the kernel.

### Local Jupyter

```python
from notebook_pdf import notebook2pdf
notebook2pdf()
```

The notebook path is detected automatically. If detection fails, pass the path explicitly:

```python
notebook2pdf(path="my_notebook.ipynb")
```

The PDF is written to the same directory as the notebook. The source file is never modified.

### IPython magic

After importing the package the `%notebook2pdf` magic is registered automatically:

```
%notebook2pdf
%notebook2pdf custom_output_name.pdf
```

## Example

The example notebook below demonstrates a simple workflow in Google Colab, including a matplotlib plot and the conversion cell.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/au-mbg/notebook-pdf/blob/main/examples/test_notebook.ipynb)

