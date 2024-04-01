from __future__ import annotations

from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from code_butler.cli.application import Application


@click.command(short_help="Show the location of the config file")
@click.pass_obj
def find(app: Application) -> None:
    """Show the location of the config file."""
    app.console.print(app.config_file.path)
