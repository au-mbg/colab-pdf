"""Utility for retrieving the current notebook name."""

import json
import os
import pathlib
import urllib


def _fetch_notebook_name() -> str:
    """Return the raw URL-decoded notebook name as reported by the Colab sessions API."""
    import requests

    response = requests.get(
        f"http://{os.environ['COLAB_JUPYTER_IP']}:{os.environ['KMP_TARGET_PORT']}/api/sessions"
    )
    return urllib.parse.unquote(response.json()[0]["name"])


def get_notebook_name() -> pathlib.Path:
    """Retrieve the current notebook name from Colab, sanitised for local filesystem use."""
    import werkzeug.utils

    return pathlib.Path(werkzeug.utils.secure_filename(_fetch_notebook_name()))


def get_notebook_raw_name() -> pathlib.Path:
    """Retrieve the current notebook name from Colab without sanitisation.

    Use this when looking up the file on Google Drive, where the filename
    preserves spaces and special characters exactly as Colab stores it.
    """
    return pathlib.Path(_fetch_notebook_name())


def get_notebook_name_local() -> pathlib.Path:
    """Infer the current notebook path outside of Colab.

    Tries the following strategies in order:

    1. ``__vsc_ipynb_file__`` — injected by VS Code's Jupyter extension.
    2. ``JPY_SESSION_NAME`` — set by JupyterHub / some JupyterLab setups.
    3. Jupyter server sessions API — parses server info files in the Jupyter
       runtime directory (classic Notebook / JupyterLab).

    Returns:
        Absolute path to the current .ipynb file.

    Raises:
        RuntimeError: If the notebook path cannot be determined automatically.
    """
    # Strategy 1: VS Code injects __vsc_ipynb_file__ into the kernel namespace
    try:
        import IPython
        ipython = IPython.get_ipython()
        if ipython is not None:
            vsc_file = ipython.user_ns.get("__vsc_ipynb_file__")
            if vsc_file:
                return pathlib.Path(vsc_file).resolve()
    except Exception:
        pass

    # Strategy 2: environment variable set by JupyterHub / JupyterLab
    session_name = os.environ.get("JPY_SESSION_NAME")
    if session_name:
        return pathlib.Path(session_name).resolve()

    # Strategy 3: match kernel ID against running servers via runtime info files
    try:
        import ipykernel
        import requests as _requests
        from jupyter_core.paths import jupyter_runtime_dir

        connection_file = pathlib.Path(ipykernel.get_connection_file())
        kernel_id = connection_file.stem.replace("kernel-", "")
        runtime_dir = pathlib.Path(jupyter_runtime_dir())

        for server_file in [
            *runtime_dir.glob("nbserver-*.json"),
            *runtime_dir.glob("jpserver-*.json"),
        ]:
            try:
                info = json.loads(server_file.read_text())
                base_url = info.get("url", "").rstrip("/")
                token = info.get("token", "")
                root_dir = info.get("root_dir", "")
                headers = {"Authorization": f"token {token}"} if token else {}

                sessions = _requests.get(
                    f"{base_url}/api/sessions", headers=headers, timeout=3
                ).json()
                for session in sessions:
                    if session.get("kernel", {}).get("id") == kernel_id:
                        nb_path = session["notebook"]["path"]
                        return (pathlib.Path(root_dir) / nb_path).resolve()
            except Exception:
                continue
    except Exception:
        pass

    raise RuntimeError(
        "Could not automatically determine the notebook path. "
        "Pass the path explicitly: notebook2pdf(path='my_notebook.ipynb')"
    )

