from __future__ import annotations

from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from code_butler.cli.application import Application


@click.command(short_help="Edit the config file with your default editor")
@click.pass_obj
def edit(app: Application):
    """Edit the config file with your default editor."""
    click.edit(filename=str(app.config_file.path))
