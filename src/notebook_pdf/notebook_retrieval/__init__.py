"""Functions for retrieving notebook content from Colab."""

from ._errors import GetIpynbTimeoutError
from ._name import get_notebook_name, get_notebook_name_local, get_notebook_raw_name
from .blocking import get_notebook_content_blocking
from .drive import get_notebook_content_from_drive
from .local import get_notebook_content_from_path
from .timeout import get_notebook_content_with_timeout

__all__ = [
    "GetIpynbTimeoutError",
    "get_notebook_name",
    "get_notebook_raw_name",
    "get_notebook_name_local",
    "get_notebook_content",
    "get_notebook_content_blocking",
    "get_notebook_content_with_timeout",
    "get_notebook_content_from_drive",
    "get_notebook_content_from_path",
]


def get_notebook_content(method: str = "timeout", **kwargs):
    """Retrieve notebook content using the specified method.

    Args:
        method: One of 'timeout', 'blocking', 'drive', or 'local'.
                'local' requires a ``path`` keyword argument.
        **kwargs: Additional arguments passed to the specific retrieval method.

    Returns:
        nbformat.NotebookNode

    Raises:
        ValueError: If method is not recognised.
    """
    if method == "timeout":
        return get_notebook_content_with_timeout(**kwargs)
    elif method == "blocking":
        return get_notebook_content_blocking(**kwargs)
    elif method == "drive":
        return get_notebook_content_from_drive(**kwargs)
    elif method == "local":
        return get_notebook_content_from_path(**kwargs)
    else:
        raise ValueError(
            f"Unknown method '{method}'. "
            f"Choose from: 'timeout', 'blocking', 'drive', or 'local'"
        )
