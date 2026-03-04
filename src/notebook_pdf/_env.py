"""Environment detection helpers."""


def is_colab() -> bool:
    """Return True if running inside Google Colab."""
    try:
        import google.colab  # noqa: F401
        return True
    except ImportError:
        return False


def is_ipython() -> bool:
    """Return True if running inside an IPython kernel."""
    try:
        import IPython
        return IPython.get_ipython() is not None
    except ImportError:
        return False
