from __future__ import annotations

from typing import TYPE_CHECKING

import click
from rich.syntax import Syntax

if TYPE_CHECKING:
    from code_butler.cli.application import Application


@click.command(short_help="Show the contents of the config file")
@click.pass_obj
def show(app: Application):
    """Show the contents of the config file."""
    if not app.config_file.path.is_file():  # no cov
        app.console.print(
            "No config file found! Please try `code-butler config restore`."
        )
    else:
        text = app.config_file.read()
        app.console.print(Syntax(text.rstrip(), "toml", background_color="default"))
