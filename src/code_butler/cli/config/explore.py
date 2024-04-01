from __future__ import annotations

from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from code_butler.cli.application import Application


@click.command(short_help="Open the config location in your file manager")
@click.pass_obj
def explore(app: Application) -> None:
    """Open the config location in your file manager."""
    click.launch(str(app.config_file.path), locate=True)
