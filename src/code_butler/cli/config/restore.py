from __future__ import annotations

from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from code_butler.cli.application import Application


@click.command(short_help="Restore the config file to default settings")
@click.pass_obj
def restore(app: Application):
    """Restore the config file to default settings."""
    app.config_file.restore()
    app.console.print("Settings were successfully restored.")
