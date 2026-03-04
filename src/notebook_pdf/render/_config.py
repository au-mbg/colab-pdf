"""Quarto configuration file generation."""

import pathlib

import yaml


def create_quarto_config(output_dir: pathlib.Path) -> None:
    """Write a _quarto.yml with Typst PDF settings into output_dir."""
    config = {
        "format": {
            "typst": {
                "margin": {
                    "left": "2cm",
                    "right": "2cm",
                    "top": "2.5cm",
                    "bottom": "2.5cm",
                }
            }
        }
    }
    with (output_dir / "_quarto.yml").open("w", encoding="utf-8") as f:
        yaml.dump(config, f)
