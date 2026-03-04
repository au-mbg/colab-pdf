"""Quarto installation and availability check."""

import shutil
import subprocess
import sys


def ensure_quarto() -> None:
    """Ensure Quarto is available, installing it on Linux if necessary.

    Raises:
        RuntimeError: If Quarto is not found on a non-Linux platform.
    """
    if shutil.which("quarto") is not None:
        return

    if sys.platform != "linux":
        raise RuntimeError(
            "Quarto is not installed or not on PATH. "
            "Install it from https://quarto.org/docs/get-started/ and try again."
        )

    print("📦 Installing Quarto...")
    subprocess.run(
        "wget -q 'https://quarto.org/download/latest/quarto-linux-amd64.deb' && "
        "dpkg -i quarto-linux-amd64.deb>/dev/null && "
        "rm quarto-linux-amd64.deb",
        shell=True,
        check=True,
    )
    print("✅ Quarto installation complete!")
